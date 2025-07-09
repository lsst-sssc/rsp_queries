import pytest
from astropy.time import Time
from astropy.coordinates import SkyCoord

from sso_query.query_images import check_rsp_access, build_query, make_query

def test_check_access(monkeypatch: pytest.MonkeyPatch) -> None:
    # Monkeypatch any potentially set environment variables (doesn't affect
    # the users"s environment)
    monkeypatch.setenv("EXTERNAL_INSTANCE_URL", "https://shout.at.cloud.com/")
    monkeypatch.setenv("ACCESS_TOKEN", "gt-letmein")
    monkeypatch.setenv("TAP_ROUTE", "/api/tap")

    assert check_rsp_access() == True

def test_check_access_tap_url(monkeypatch: pytest.MonkeyPatch) -> None:
    # Monkeypatch any potentially set environment variables (doesn't affect
    # the users"s environment)
    monkeypatch.setenv("EXTERNAL_TAP_URL", "https://shout.at.cloud.com/api/tap")
    monkeypatch.setenv("ACCESS_TOKEN", "gt-letmein")

    assert check_rsp_access() == True

def test_check_no_access(monkeypatch: pytest.MonkeyPatch) -> None:
    # Monkeypatch any potentially set environment variables (doesn't affect
    # the users"s environment)
    monkeypatch.setenv("EXTERNAL_INSTANCE_URL", "https://shout.at.cloud.com/")
    monkeypatch.setenv("ACCESS_TOKEN", "")
    monkeypatch.setenv("TAP_ROUTE", "/api/tap")

    assert check_rsp_access() == False

@pytest.fixture
def setup_base_query():
    expected_query = "SELECT lsst_visit, lsst_detector, lsst_tract, lsst_patch, lsst_band,"\
            "s_ra, s_dec, t_min, t_max, s_region, access_url\n" \
        "FROM ivoa.ObsCore\n" \
        "WHERE calib_level = 2\n" \
        "AND CONTAINS(POINT('ICRS', 37.86,6.98), s_region) = 1\n"

    return expected_query

@pytest.fixture
def setup_band_query(setup_base_query):
    """Fixture which returns a callable to create resource with arguments."""
    def _setup_band_query(band=None):
        expected_query = setup_base_query
        if band == 'r':
            expected_query += "AND (lsst_band = 'r')\n"
        else:
            expected_query += "AND (lsst_band = 'g' OR lsst_band = 'r' OR lsst_band = 'i')\n"
        return expected_query
    return _setup_band_query

@pytest.fixture
def setup_time_query(setup_band_query):
    expected_query = setup_band_query()
    expected_query += "AND t_min > 60646.04 AND t_max < 60646.09\nORDER BY t_min ASC\n"

    return expected_query

@pytest.fixture
def center():
    return SkyCoord(37.86, 6.98, unit='deg')


def test_default_build_query(setup_band_query, center):

    query = build_query(center)

    assert query == setup_band_query()

def test_build_query_no_bands(setup_base_query, center):

    query = build_query(center, bands=None)

    assert query == setup_base_query

def test_build_query_empty_bands(setup_base_query, center):

    query = build_query(center, bands=[])

    assert query == setup_base_query

def test_build_query_specific_band(setup_band_query, center):

    query = build_query(center, bands=['r'])

    r_query = setup_band_query('r')
    assert query == r_query

def test_build_query_specific_band_str(setup_band_query, center):

    query = build_query(center, bands='r')

    r_query = setup_band_query('r')
    assert query == r_query

def test_build_query_mjd_floats(setup_time_query, center):

    query = build_query(center, t_min=60646.04, t_max=60646.09)

    assert query == setup_time_query

def test_build_query_mjd_times(setup_time_query, center):

    query = build_query(center, t_min=Time(60646.04, format='mjd', scale='tai'),
                         t_max=Time(60646.09, format='mjd', scale='tai'))

    assert query == setup_time_query

def test_build_query_mjd_times_utc(setup_time_query, center):
    TAI_UTC = 37/86400.0 # No. of leapseconds + offset between UTC and TAI in days (https://www.nist.gov/pml/time-and-frequency-division/time-realization/leap-seconds)

    query = build_query(center, t_min=Time(60646.04-TAI_UTC, format='mjd', scale='utc'),
                         t_max=Time(60646.09-TAI_UTC, format='mjd', scale='utc'))

    assert query == setup_time_query

def test_build_query_mjd_floats_tmin_only(setup_time_query, center):

    query = build_query(center, t_min=60646.04)

    assert query == setup_time_query.replace(' AND t_max < 60646.09', '')

def test_build_query_mjd_floats_tmax_only(setup_time_query, center):

    query = build_query(center, t_max=60646.09)

    assert query == setup_time_query.replace('AND t_min > 60646.04', '')


def test_make_query_check_no_access(monkeypatch: pytest.MonkeyPatch, center) -> None:
    # Monkeypatch any potentially set environment variables (doesn't affect
    # the users"s environment)
    monkeypatch.setenv("EXTERNAL_INSTANCE_URL", "https://shout.at.cloud.com/")
    monkeypatch.setenv("ACCESS_TOKEN", "")
    monkeypatch.setenv("TAP_ROUTE", "/api/tap")

    assert make_query(center) == None
