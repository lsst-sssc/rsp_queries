from astropy.time import Time
from astropy.table import Table
from astropy.coordinates import SkyCoord
from lsst.rsp import get_tap_service
from lsst.rsp.utils import get_service_url, get_access_token

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
        print("Executing the following query:\n", query)
        service = get_tap_service("tap")
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
