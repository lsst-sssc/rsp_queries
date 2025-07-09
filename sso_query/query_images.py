import os
from pathlib import Path
from urllib.parse import urlparse

import requests
import numpy as np
from astropy.time import Time
from astropy.table import Table
from astropy.coordinates import SkyCoord
from pyvo.dal.adhoc import DatalinkResults

from lsst.rsp import get_tap_service
from lsst.rsp.utils import get_service_url, get_access_token, get_pyvo_auth, format_bytes

def check_rsp_access(dbg=False):
    """Check whether RSP access is going to work"""

    access_good = False
    url = get_service_url("tap")
    # If running inside the RSP or `EXTERNAL_INSTANCE_URL` is set in the environment
    # then the url should start with 'https://'
    if dbg: print("URL=",url)
    if url.startswith('https://'):
        access_good = True
        token = get_access_token()
        if dbg: print("Token=", token)
        # Check for token set
        if token.startswith('gt-') is False:
            access_good = False
    return access_good

def build_query(center: SkyCoord, bands: list = ['g', 'r', 'i'], t_min: float | Time | None = None,
                 t_max: float | Time | None = None, calib_level=2) -> str:
    """Build the ADQL query to search ivoa.ObsCore for images

    Args:
        center (SkyCoord): Astropy SkyCoord of center to search
        bands (list, optional): List of bands to search. Defaults to ['g', 'r', 'i'].
        t_min (float, Time; optional): minimum time of images; either a MJD in TAI float or a Time object
        t_max (float, Time; optional): maximum time of images; either a MJD in TAI float or a Time object
        calib_level (int, optional): calibration level of images to return. Defaults to 2 (visit_image)

    Returns:
        str: ADQL query string for RSP
    """

    query = "SELECT lsst_visit, lsst_detector, lsst_tract, lsst_patch, lsst_band," \
            "s_ra, s_dec, t_min, t_max, s_region, access_url\n" \
            "FROM ivoa.ObsCore\n"\
            f"WHERE calib_level = {calib_level}\n"
    coordinate_clause = f"AND CONTAINS(POINT('ICRS', {center.ra.deg},{center.dec.deg}), s_region) = 1\n"
    query += coordinate_clause
    bands_clause = ""
    if bands and len(bands) > 0:
        bands_clause = " OR ".join([f"lsst_band = '{band}'" for band in bands])
        bands_clause = f"AND ({bands_clause})\n"
    query += bands_clause
    time_clause = ""
    if t_min is not None:
        if isinstance(t_min, float):
            # Try and turn the float into a Time object. MJD input and TAI timescale assumed.
            time_min = Time(t_min, format='mjd', scale='tai')
        else:
            time_min = t_min
        time_clause = f"AND t_min > {time_min.tai.mjd}"
    if t_max is not None:
        if isinstance(t_max, float):
            # Try and turn the float into a Time object. MJD input and TAI timescale assumed.
            time_max = Time(t_max, format='mjd', scale='tai')
        else:
            time_max = t_max
        time_clause += f" AND t_max < {time_max.tai.mjd}"
    if time_clause != "":
        time_clause += "\nORDER BY t_min ASC\n"
    query += time_clause

    return query

def make_query(center: SkyCoord, bands: list = ['g', 'r', 'i'], t_min: float | Time | None = None,
                 t_max: float | Time | None = None, calib_level=2) -> Table | None:
    """Builds and executes a query for the RSP to find matching images

    Args:
        center (SkyCoord): Astropy SkyCoord of center to search
        bands (list, optional): List of bands to search. Defaults to ['g', 'r', 'i'].
        t_min (float, Time; optional): minimum time of images; either a MJD in TAI float or a Time object
        t_max (float, Time; optional): maximum time of images; either a MJD in TAI float or a Time object
        calib_level (int, optional): calibration level of images to return. Defaults to 2 (visit_image)
    Returns:
        Table | None: Astropy Table of results or None in the case of errors
    """
    results = None
    if check_rsp_access():
        query = build_query(center, bands, t_min, t_max, calib_level)
        print(f"Executing the following query:\n{query}")
        service = get_tap_service("tap")
        assert service is not None
        job = service.submit_job(query)
        job.run()
        job.wait(phases=['COMPLETED', 'ERROR'])
        print('Job phase is', job.phase)
        if job.phase == 'ERROR':
            job.raise_if_error()
        assert job.phase == 'COMPLETED'
        results = job.fetch_result().to_table()
        print(f"Found {len(results)} results")
        job.delete()
    else:
        results = None

    return results

def parse_dp_url(url:str) -> str:
    """Parses a Rubin data product filename from a DatalinkRecord URL

    Args:
        url (str): URL to be parsed

    Returns:
        str: filename
    """
    filename = ''
    parsed_url = urlparse(url)
    if parsed_url.path:
        filename = parsed_url.path.split('/')[-1]

    return filename

def download_data(results: Table, output_directory:str | Path, actually_download: bool = False) -> list:
    """Downloads data from the links in the passed <results> Table (or slice/subset) to <output_directory>.
      With [actually_download] = False (default), the number and size of the resulting files is
      printed; set `actually_download=True to download the data.

    Args:
        results (Table): Table of image results from e.g. make_query(); must contain a 'access_url' column
        output_directory (str | Path): Path to save the files to (will be created if it doesn't exist)
        actually_download (bool, optional): Whether to actually download the files. Defaults to False.

    Returns:
        list: A list of the downloaded filepaths
    """

    dl_files = []
    if 'access_url' in results.colnames:
        total_size = np.int64(0)
        data_urls = []
        # Walk through the results table first to get URLs and size
        for datalink_url in results['access_url']:
            dl_result = DatalinkResults.from_result_url(datalink_url, session=get_pyvo_auth())
            dl_record = dl_result.getrecord(0)
            image_url = dl_record.get('access_url', None)
            size_in_bytes = dl_record.get('content_length', 0)
            if image_url and size_in_bytes:
                data_urls.append(image_url)
                total_size += size_in_bytes
        print(f"Found {len(data_urls)} files with total size {format_bytes(total_size)}")
        if actually_download is True:
            os.makedirs(output_directory, exist_ok=True)
            for frame_url in data_urls:
                filename = parse_dp_url(frame_url)
                print(filename)
                if filename:
                    filepath = os.path.join(output_directory, filename)
                    with open(filepath, 'wb') as f:
                        f.write(requests.get(frame_url).content)
                    dl_files.append(filepath)
        else:
            print("set actually_download=True to actually download the data")
    else:
        print("No 'access_url' column found in results table")

    return dl_files