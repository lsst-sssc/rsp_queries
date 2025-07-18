import os
import io
from pathlib import Path
from urllib.parse import urlparse

import requests
import numpy as np
import astropy.units as u
from astropy.io import fits
from astropy.time import Time
from astropy.table import Table, Row
from astropy.coordinates import SkyCoord
from pyvo.dal.adhoc import DatalinkResults, SodaQuery

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
        if isinstance(t_min, Time):
            time_min = t_min
        else:
            # Try and turn the passed `t_min` into a Time object. MJD input and TAI timescale assumed.
            time_min = Time(t_min, format='mjd', scale='tai')
        time_clause = f"AND t_min > {time_min.tai.mjd}"
    if t_max is not None:
        if isinstance(t_max, Time):
            time_max = t_max
        else:
            # Try and turn the passed `t_max` into a Time object. MJD input and TAI timescale assumed.
            time_max = Time(t_max, format='mjd', scale='tai')
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

def get_image_cutout(image_result: Row, center: SkyCoord, radius: u.Unit) -> fits.HDUList | None:
    """Produces a FITS image cutout from the image result given in <image_result> at
    the specified <center> with square edges equal to 2 x <radius>.
    The `center` is not checked to see whether it's within the `image_result['s_region']`
    POLYGON bounds (but potentially could be..)


    Args:
        image_result (Row): A Row from a Table of results representing the image to cutout from
        center (SkyCoord): Astropy SkyCoord of center of cutout
        radius (u.Unit; transformable to degrees): radius of cutout. The resulting
        cutout is always a square, with an edge size that is the same as the circle's
        diameter.

    Returns:
        fits.HDUList: a FITS HDUList of the image cutout (or None in case of error)
    """
    hdulist = None
    # Retrieve datalink. XXX same code as above, refactor
    datalink_url = image_result['access_url']
    dl_result = DatalinkResults.from_result_url(datalink_url, session=get_pyvo_auth())
    if dl_result.status[0] == 'OK':
        # Make SODA query object from the 'cutout-sync' service definition
        sq = SodaQuery.from_resource(dl_result,
                                     dl_result.get_adhocservice_by_id("cutout-sync"),
                                     session=get_pyvo_auth())
        # Set circle query property (which actually returns a square <sigh/shrug>...)
        sq.circle = (center.ra.deg, center.dec.deg, radius.to(u.deg).value)
        cutout_bytes = sq.execute_stream().read()
        if len(cutout_bytes) > 0: # Also check if integer multiple of 2880 bytes?
            hdulist = fits.open(io.BytesIO(cutout_bytes))
    return hdulist

def display_image(datalink_url: str, backend: str = 'firefly'):
    """Download and display the image pointed at `datalink_url` e.g. from the
    'access_url' of a results table row:
        display_image(results[0]['access_url'])

    Args:
        datalink_url (str): A DataLink URL to the image
        backend (str): The backend to use for the `afwDisplay` display (Optional: 'firefly' (default) or 'matplotlib')

    Returns:
        d: Display object (either a `afwDisplay` or a `pyds9.DS9` object)
    """
    # XXX Should be refactored into image fetching and image displaying methods
    dl_result = DatalinkResults.from_result_url(datalink_url, session=get_pyvo_auth())
    dl_record = dl_result.getrecord(0)
    image_url = dl_record.get('access_url', None)
    try:
        import lsst.afw.display as afwDisplay
        from lsst.afw.image import ExposureF
        afwDisplay.setDefaultBackend(backend)
        afw_display = afwDisplay.Display(frame=1)
        visit_image = ExposureF(image_url)
        afw_display.image(visit_image)
        afw_display.setMaskTransparency(100)
        display = afw_display
    except ImportError:
        import pyds9
        from astropy.io import fits
        d = pyds9.DS9()
        visit_image = fits.open(image_url)
        d.set_pyfits(visit_image)
        d.set('scale zscale')
        d.set('zoom to fit')
        display = d
    return d
