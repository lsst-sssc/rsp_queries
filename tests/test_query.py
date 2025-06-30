from sso_query.query import make_query

class TestQuery:
    def test_lpcs(self):
        expected_query = f"""SELECT mpc.ssObjectId, mpc.mpcDesignation, mpc.e, mpc.q, mpc.incl FROM dp03_catalogs_10yr.MPCORB as mpc WHERE mpc.q/(1.0-mpc.e) >= 50.0 ORDER by mpc.mpcDesignation"""

        query = make_query('LPCs')

        assert expected_query == query


    def test_centaurs(self):
        expected_query = f"""SELECT mpc.ssObjectId, mpc.mpcDesignation, mpc.e, mpc.q, mpc.incl FROM dp03_catalogs_10yr.MPCORB as mpc WHERE mpc.q/(1.0-mpc.e) >= 5.5 AND mpc.q/(1.0-mpc.e) <= 30.1 ORDER by mpc.mpcDesignation"""

        query = make_query('Centaurs')

        assert expected_query == query
        

    def test_tnos(self):
        expected_query = f"""SELECT mpc.ssObjectId, mpc.mpcDesignation, mpc.e, mpc.q, mpc.incl FROM dp03_catalogs_10yr.MPCORB as mpc WHERE mpc.q/(1.0-mpc.e) >= 30.1 AND mpc.q/(1.0-mpc.e) <= 50.0 ORDER by mpc.mpcDesignation"""

        query = make_query('TNOs')

        assert expected_query == query


    def test_neptuniantrojans(self):
        expected_query = f"""SELECT mpc.ssObjectId, mpc.mpcDesignation, mpc.e, mpc.q, mpc.incl FROM dp03_catalogs_10yr.MPCORB as mpc WHERE mpc.q/(1.0-mpc.e) >= 29.8 AND mpc.q/(1.0-mpc.e) <= 30.4 ORDER by mpc.mpcDesignation"""

        query = make_query('Neptunian Trojans')

        assert expected_query == query


    def test_jupitertrojans(self):
        expected_query = f"""SELECT mpc.ssObjectId, mpc.mpcDesignation, mpc.e, mpc.q, mpc.incl FROM dp03_catalogs_10yr.MPCORB as mpc WHERE mpc.e <= 0.3 AND mpc.q/(1.0-mpc.e) >= 4.8 AND mpc.q/(1.0-mpc.e) <= 5.4 ORDER by mpc.mpcDesignation"""

        query = make_query('Jupiter Trojans')

        assert expected_query == query

        
    def test_mbas(self):
        expected_query = f"""SELECT mpc.ssObjectId, mpc.mpcDesignation, mpc.e, mpc.q, mpc.incl FROM dp03_catalogs_10yr.MPCORB as mpc WHERE mpc.q >= 1.66 AND mpc.q/(1.0-mpc.e) >= 2.0 AND mpc.q/(1.0-mpc.e) <= 3.2 ORDER by mpc.mpcDesignation"""

        query = make_query('MBAs')

        assert expected_query == query

    
    def test_neos(self):
        expected_query = f"""SELECT mpc.ssObjectId, mpc.mpcDesignation, mpc.e, mpc.q, mpc.incl FROM dp03_catalogs_10yr.MPCORB as mpc WHERE mpc.q <= 1.3 AND mpc.e <= 1.0 AND mpc.q/(1.0-mpc.e) >= 4.0 ORDER by mpc.mpcDesignation"""

        query = make_query('NEOs')

        assert expected_query == query
