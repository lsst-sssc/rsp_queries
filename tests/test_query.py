from sso_query.query import make_query

class TestQuery:
    def test_defaults(self):
        expected_query = f"""e, q, a FROM dp03_catalogs_10yr.MPCORB as mpc
        WHERE mpc.q < 1.3 AND mpc.e < 1.0 AND mpc.a < 10.0;"""


        query = make_query()

        assert expected_query == query

    def test_neos(self):
        expected_query = f"""e, q, a FROM dp03_catalogs_10yr.MPCORB as mpc
        WHERE mpc.q < 1.3 AND mpc.e < 1.0 AND mpc.a > 4.0;"""

        query = make_query(1.3, class_type = "neos")

        assert expected_query == query

        # q < 1.3 au (a > 4, e < 1)

    def test_centaurs(self):
        expected_query = f"""a FROM dp03_catalogs_10yr.MPCORB as mpc
        WHERE mpc.a > 5.5 AND mpc.a < 30.1;"""

        query = make_query(class_type = "centaurs")

        assert expected_query == query

        # 5.5 au < a < 30.1 au

    def test_mbas(self):
        expected_query = f"""a, q FROM dp03_catalogs_10yr.MPCORB as mpc
        WHERE mpc.a > 2.0 AND mpc.a < 3.2 AND mpc.q > 1.66;"""

        query = make_query(class_type = "mbas")

        assert expected_query == query
        
        # 2.0 au < a < 3.2 au, q > 1.66 au

    def test_lpcs(self):
        expected_query = f"""a FROM dp03_catalogs_10yr.MPCORB as mpc
        WHERE mpc.a > 50;"""

        query = make_query(class_type = "lpcs")

        assert expected_query == query
        
        # a > 50 au

    def test_tnos(self):
        expected_query = f"""a FROM dp03_catalogs_10yr.MPCORB as mpc
        WHERE mpc.a > 30.1 AND mpc.a < 50;"""

        query = make_query(class_type = "tnos")

        assert expected_query == query
        
        # 30.1 au < a < 50 au

    def test_jtrojans(self):
        expected_query = f"""a, e FROM dp03_catalogs_10yr.MPCORB as mpc
        WHERE mpc.a > 4.8 AND mpc.a < 5.4 AND e < 0.3;"""

        query = make_query(class_type = "jtrojans")

        assert expected_query == query
        
        # 4.8 au < a < 5.4 au, e < 0.3

    def test_ntrojans(self):
        expected_query = f"""a FROM dp03_catalogs_10yr.MPCORB as mpc
        WHERE mpc.a > 29.8 AND mpc.a < 30.4;"""

        query = make_query(class_type = "ntrojans")

        assert expected_query == query
        
        # 29.8 au < a < 30.4 au
