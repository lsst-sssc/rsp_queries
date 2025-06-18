from sso_query.query import make_query

class TestQuery:
    # def test_defaults(self):
    #     expected_query = f"""SELECT e, q, a FROM dp03_catalogs_10yr.MPCORB as mpc
    #     WHERE mpc.q < 1.3 AND mpc.e < 1.0 AND mpc.a < 10.0;"""


    #     query = make_query()

    #     assert expected_query == query

    def test_neos(self):
        expected_query = f"""SELECT a, q, e FROM dp03_catalogs_10yr.MPCORB as mpc
            WHERE mpc.q < 1.3 AND mpc.e < 1.0 AND mpc.a > 4.0;"""

        query = make_query(q_cutoff=1.3, a_cutoff=4.0, e_cutoff = 1.0)

        assert expected_query == query

        # q < 1.3 au (a > 4, e < 1)

    def test_centaurs(self):
        expected_query = f"""SELECT a, q, e FROM dp03_catalogs_10yr.MPCORB as mpc
            WHERE mpc.a > 5.5 AND mpc.a < 30.1;"""

        query = make_query(a_cutoff = 30.1, a_cutoff_min = 5.5)

        assert expected_query == query

        # 5.5 au < a < 30.1 au

    def test_mbas(self):
        expected_query = f"""SELECT a, q, e FROM dp03_catalogs_10yr.MPCORB as mpc
            WHERE mpc.a > 2.0 AND mpc.a < 3.2 AND mpc.q > 1.66;"""

        query = make_query(a_cutoff = 3.2, a_cutoff_min = 2.0, q_cutoff = 1.66)

        assert expected_query == query
        
        # 2.0 au < a < 3.2 au, q > 1.66 au

    def test_lpcs(self):
        expected_query = f"""SELECT a, q, e FROM dp03_catalogs_10yr.MPCORB as mpc
            WHERE mpc.a > 50;"""

        query = make_query(a_cutoff_min = 50)

        assert expected_query == query
        
        # a > 50 au

    def test_tnos(self):
        expected_query = f"""SELECT a, q, e FROM dp03_catalogs_10yr.MPCORB as mpc
            WHERE mpc.a > 30.1 AND mpc.a < 50;"""

        query = make_query(a_cutoff_min = 30.1, a_cutoff = 50)

        assert expected_query == query
        
        # 30.1 au < a < 50 au

    def test_jtrojans(self):
        expected_query = f"""SELECT a, q, e FROM dp03_catalogs_10yr.MPCORB as mpc
            WHERE mpc.a > 4.8 AND mpc.a < 5.4 AND mpc.e < 0.3;"""

        query = make_query(a_cutoff_min = 4.8, a_cutoff = 5.4, e_cutoff = 0.3)

        assert expected_query == query
        
        # 4.8 au < a < 5.4 au, e < 0.3

    def test_ntrojans(self):
        expected_query = f"""SELECT a, q, e FROM dp03_catalogs_10yr.MPCORB as mpc
            WHERE mpc.a > 29.8 AND mpc.a < 30.4;"""

        query = make_query(a_cutoff_min = 29.8, a_cutoff = 30.4)

        assert expected_query == query
        
        # 29.8 au < a < 30.4 au
