import pytest
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
    monkeypatch.setenv("TAP_ROUTE", "/api/tap")

    assert check_rsp_access() == False

@pytest.fixture
def setup_base_query():
    expected_query = "SELECT lsst_visit, lsst_detector, lsst_tract, lsst_patch, lsst_band,"\
            "s_ra, s_dec, t_min, t_max, s_region\n" \
        "FROM ivoa.ObsCore\n" \
        "WHERE calib_level = 2\n" \
        "AND (lsst_band = 'g' OR lsst_band = 'r' OR lsst_band = 'i')\n"\
        "AND CONTAINS(POINT('ICRS', 37.86,6.98), s_region) = 1\n"

    yield expected_query

@pytest.fixture
def center():
    yield SkyCoord(37.86, 6.98, unit='deg')

def test_build_query(setup_base_query, center):

    query = build_query(center)

    assert query == setup_base_query

def test_build_query_no_bands(setup_base_query, center):

    query = build_query(center, bands=None)

    assert query == setup_base_query[0:setup_base_query.rfind('\n', 0, -2)]

def test_build_query_empty_bands(setup_base_query, center):

    query = build_query(center, bands=[])

    assert query == setup_base_query[0:setup_base_query.rfind('\n', 0, -2)]
