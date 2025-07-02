from astropy.coordinates import SkyCoord
from lsst.rsp.utils import get_service_url, get_access_token

def check_rsp_access():
    """Check whether RSP access is going to work"""

    access_good = False
    url = get_service_url("tap")
    # If running inside the RSP or `EXTERNAL_INSTANCE_URL` is set in the environment
    # then the url should start with 'https://'
    print("URL=",url)
    if url.startswith('https://'):
        access_good = True
        token = get_access_token()
        print("Token=", token)
        # Check for token set
        if token.startswith('gt-') is False:
            access_good = False
    return access_good

def build_query(center: SkyCoord, bands: list = ['g', 'r', 'i'], calib_level=2) -> str:
    """Build the query for the ivoa.ObsCore
    """

    query = "SELECT lsst_visit, lsst_detector, lsst_tract, lsst_patch, lsst_band," \
            "s_ra, s_dec, t_min, t_max, s_region\n" \
            "FROM ivoa.ObsCore\n"\
            f"WHERE calib_level = {calib_level}"
    bands_clause = "\n"
    if bands and len(bands) > 0:
        bands_clause = " OR ".join([f"lsst_band = '{band}'" for band in bands])
        bands_clause = f"\nAND ({bands_clause})\n"
    query += bands_clause
    coordinate_clause = f"AND CONTAINS(POINT('ICRS', {center.ra.deg},{center.dec.deg}), s_region) = 1\n"
    query += coordinate_clause

    return query

def make_query():
    if check_rsp_access():
        query = build_query()
    pass