from sso_query.query import make_query

class TestQuery:
    def test_defaults(self):
        expected_query = f"""e, q, a FROM dp03_catalogs_10yr.MPCORB as mpc "
        WHERE mpc.q < 1.3 AND mpc.e < 1.0 AND mpc.a < 10.0;"""


        query = make_query()

        assert expected_query == query

    def test_neos(self):
        expected_query = f"""e, q, a FROM dp03_catalogs_10yr.MPCORB as mpc "
        WHERE mpc.q < 1.3 AND mpc.e < 1.0 AND mpc.a < 10.0;"""

        query = make_query(1.3)

        assert expected_query == query