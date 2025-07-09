from sso_query.query import make_query

# Class 1: TestQuery_DP01 - tests for catalog DP01. Type-join table is DiaSource, param-join table is ssObject.
# Class 2: TestQuery_DP1 - tests for catalog DP1. Type-join table is ssObject, param-join table is DiaSource.



class TestQuery_DP01:
    ############### TYPE GIVEN, NO JOIN ###############
    def test_neo_type_no_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID, mpc.mpcDesignation FROM dp03_catalogs_10yr.MPCORB AS mpc
    WHERE mpc.q < 1.3 AND mpc.e < 1.0 AND mpc.q/(1-mpc.e) < 4.0;"""

        query, class_name = make_query("dp03_catalogs_10yr", class_name = "NEO")
        assert expected_query == query

    def test_MBA_type_no_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID, mpc.mpcDesignation FROM dp03_catalogs_10yr.MPCORB AS mpc
    WHERE mpc.q > 1.66 AND mpc.q/(1-mpc.e) > 2.0 AND mpc.q/(1-mpc.e) < 3.2;"""

        query, class_name = make_query("dp03_catalogs_10yr", class_name = "MBA")
        assert expected_query == query

    def test_jfc_type_no_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID, mpc.mpcDesignation FROM dp03_catalogs_10yr.MPCORB AS mpc
    WHERE (mpc.q * (1 - mpc.e)) / (5.204 * (1 + mpc.e)) >= 0 AND (5.204 * (1 - mpc.e)) / mpc.q + 2 * COS(RADIANS(mpc.incl)) * SQRT((mpc.q * (1 - mpc.e)) / (5.204 * (1 + mpc.e))) BETWEEN 2.0 AND 3.0;"""

        query, class_name = make_query("dp03_catalogs_10yr", class_name = "JFC")
        assert expected_query == query

    def test_lpc_type_no_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID, mpc.mpcDesignation FROM dp03_catalogs_10yr.MPCORB AS mpc
    WHERE mpc.q/(1-mpc.e) > 50.0;"""

        query, class_name = make_query("dp03_catalogs_10yr", class_name = "LPC")
        assert expected_query == query
    
    def test_centaurs_type_no_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID, mpc.mpcDesignation FROM dp03_catalogs_10yr.MPCORB AS mpc
    WHERE mpc.q/(1-mpc.e) > 5.5 AND mpc.q/(1-mpc.e) < 30.1;"""

        query, class_name = make_query("dp03_catalogs_10yr", class_name = "Centaur")
        assert expected_query == query

    def test_tno_type_no_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID, mpc.mpcDesignation FROM dp03_catalogs_10yr.MPCORB AS mpc
    WHERE mpc.q/(1-mpc.e) > 30.1 AND mpc.q/(1-mpc.e) < 50.0;"""

        query, class_name = make_query("dp03_catalogs_10yr", class_name = "TNO")
        assert expected_query == query

    def test_jtrojan_type_no_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID, mpc.mpcDesignation FROM dp03_catalogs_10yr.MPCORB AS mpc
    WHERE mpc.e < 0.3 AND mpc.q/(1-mpc.e) > 4.8 AND mpc.q/(1-mpc.e) < 5.4;"""

        query, class_name = make_query("dp03_catalogs_10yr", class_name = "Jtrojan")
        assert expected_query == query

    def test_ntrojan_type_no_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID, mpc.mpcDesignation FROM dp03_catalogs_10yr.MPCORB AS mpc
    WHERE mpc.q/(1-mpc.e) > 29.8 AND mpc.q/(1-mpc.e) < 30.4;"""

        query, class_name = make_query("dp03_catalogs_10yr", class_name = "Ntrojan")
        assert expected_query == query




    ############### PARAMS GIVEN, NO JOIN ###############
    def test_neos_params_no_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID, mpc.mpcDesignation FROM dp03_catalogs_10yr.MPCORB AS mpc
    WHERE mpc.q < 1.3 AND mpc.e < 1.0 AND mpc.q/(1-mpc.e) < 4.0;"""
        expected_class_name = "NEO"

        cutoffs = {"q_max": 1.3, "a_max": 4.0, "e_max": 1.0}
        query, class_name = make_query("dp03_catalogs_10yr", class_name = None, cutoffs = cutoffs, join = None)

        assert expected_query == query
        assert expected_class_name == class_name

    def test_MBA_params_no_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID, mpc.mpcDesignation FROM dp03_catalogs_10yr.MPCORB AS mpc
    WHERE mpc.q > 1.66 AND mpc.q/(1-mpc.e) > 2.0 AND mpc.q/(1-mpc.e) < 3.2;"""
        expected_class_name = "MBA"

        cutoffs = {"q_min": 1.66, "a_min": 2.0, "a_max": 3.2}

        query, class_name = make_query("dp03_catalogs_10yr", class_name = None, cutoffs = cutoffs, join = None)
        assert expected_query == query
        assert expected_class_name == class_name

    def test_jfc_params_no_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID, mpc.mpcDesignation FROM dp03_catalogs_10yr.MPCORB AS mpc
    WHERE (mpc.q * (1 - mpc.e)) / (5.204 * (1 + mpc.e)) >= 0 AND (5.204 * (1 - mpc.e)) / mpc.q + 2 * COS(RADIANS(mpc.incl)) * SQRT((mpc.q * (1 - mpc.e)) / (5.204 * (1 + mpc.e))) BETWEEN 2.0 AND 3.0;"""
        expected_class_name = "JFC"

        cutoffs = {"tj_min": 2.0, "tj_max": 3.0}

        query, class_name = make_query("dp03_catalogs_10yr", class_name = None, cutoffs = cutoffs, join = None)
        assert expected_query == query
        assert expected_class_name == class_name

    def test_lpc_params_no_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID, mpc.mpcDesignation FROM dp03_catalogs_10yr.MPCORB AS mpc
    WHERE mpc.q/(1-mpc.e) > 50.0;"""
        expected_class_name = "LPC"

        cutoffs = {"a_min": 50.0}

        query, class_name = make_query("dp03_catalogs_10yr", class_name = None, cutoffs = cutoffs, join = None)
        assert expected_query == query
        assert expected_class_name == class_name
        
    def test_centaurs_params_no_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID, mpc.mpcDesignation FROM dp03_catalogs_10yr.MPCORB AS mpc
    WHERE mpc.q/(1-mpc.e) > 5.5 AND mpc.q/(1-mpc.e) < 30.1;"""
        expected_class_name = "Centaur"

        cutoffs = {"a_min": 5.5, "a_max": 30.1}

        query, class_name = make_query("dp03_catalogs_10yr", class_name = None, cutoffs = cutoffs, join = None)

        assert expected_query == query
        assert expected_class_name == class_name
        
    def test_tno_params_no_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID, mpc.mpcDesignation FROM dp03_catalogs_10yr.MPCORB AS mpc
    WHERE mpc.q/(1-mpc.e) > 30.1 AND mpc.q/(1-mpc.e) < 50.0;"""
        expected_class_name = "TNO"

        cutoffs = {"a_min": 30.1, "a_max": 50.0}

        query, class_name = make_query("dp03_catalogs_10yr", class_name = None, cutoffs = cutoffs, join = None)

        assert expected_query == query
        assert expected_class_name == class_name

    def test_jtrojans_params_no_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID, mpc.mpcDesignation FROM dp03_catalogs_10yr.MPCORB AS mpc
    WHERE mpc.e < 0.3 AND mpc.q/(1-mpc.e) > 4.8 AND mpc.q/(1-mpc.e) < 5.4;"""
        expected_class_name = "Jtrojan"

        cutoffs = {"a_min": 4.8, "a_max": 5.4, "e_max": 0.3}

        query, class_name = make_query("dp03_catalogs_10yr", class_name = None, cutoffs = cutoffs, join = None)
        assert expected_query == query
        assert expected_class_name == class_name

    def test_ntrojans_params_no_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID, mpc.mpcDesignation FROM dp03_catalogs_10yr.MPCORB AS mpc
    WHERE mpc.q/(1-mpc.e) > 29.8 AND mpc.q/(1-mpc.e) < 30.4;"""
        expected_class_name = "Ntrojan"

        cutoffs = {"a_min": 29.8, "a_max": 30.4}

        query, class_name = make_query("dp03_catalogs_10yr", class_name = None, cutoffs = cutoffs, join = None)
        assert expected_query == query
        assert expected_class_name == class_name



    ############### TYPE GIVEN, JOIN: DiaSource ###############
    def test_neo_type_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID, mpc.mpcDesignation, dias.magTrueVband, dias.band FROM dp03_catalogs_10yr.MPCORB AS mpc
    INNER JOIN dp03_catalogs_10yr.DiaSource AS dias ON mpc.ssObjectId = dias.ssObjectId
    WHERE mpc.q < 1.3 AND mpc.e < 1.0 AND mpc.q/(1-mpc.e) < 4.0;"""

        query, class_name = make_query("dp03_catalogs_10yr", class_name = "NEO", join = 'DiaSource')
        assert expected_query == query

    def test_MBA_type_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID, mpc.mpcDesignation, dias.magTrueVband, dias.band FROM dp03_catalogs_10yr.MPCORB AS mpc
    INNER JOIN dp03_catalogs_10yr.DiaSource AS dias ON mpc.ssObjectId = dias.ssObjectId
    WHERE mpc.q > 1.66 AND mpc.q/(1-mpc.e) > 2.0 AND mpc.q/(1-mpc.e) < 3.2;"""
        
        query, class_name = make_query("dp03_catalogs_10yr", class_name = "MBA", join = 'DiaSource')
        assert expected_query == query

    def test_jfc_type_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID, mpc.mpcDesignation, dias.magTrueVband, dias.band FROM dp03_catalogs_10yr.MPCORB AS mpc
    INNER JOIN dp03_catalogs_10yr.DiaSource AS dias ON mpc.ssObjectId = dias.ssObjectId
    WHERE (mpc.q * (1 - mpc.e)) / (5.204 * (1 + mpc.e)) >= 0 AND (5.204 * (1 - mpc.e)) / mpc.q + 2 * COS(RADIANS(mpc.incl)) * SQRT((mpc.q * (1 - mpc.e)) / (5.204 * (1 + mpc.e))) BETWEEN 2.0 AND 3.0;"""

        query, class_name = make_query("dp03_catalogs_10yr", class_name = "JFC", join = 'DiaSource')
        assert expected_query == query

    def test_lpc_type_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID, mpc.mpcDesignation, dias.magTrueVband, dias.band FROM dp03_catalogs_10yr.MPCORB AS mpc
    INNER JOIN dp03_catalogs_10yr.DiaSource AS dias ON mpc.ssObjectId = dias.ssObjectId
    WHERE mpc.q/(1-mpc.e) > 50.0;"""

        query, class_name = make_query("dp03_catalogs_10yr", class_name = "LPC", join = 'DiaSource')
        assert expected_query == query

    def test_centaur_type_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID, mpc.mpcDesignation, dias.magTrueVband, dias.band FROM dp03_catalogs_10yr.MPCORB AS mpc
    INNER JOIN dp03_catalogs_10yr.DiaSource AS dias ON mpc.ssObjectId = dias.ssObjectId
    WHERE mpc.q/(1-mpc.e) > 5.5 AND mpc.q/(1-mpc.e) < 30.1;"""

        query, class_name = make_query("dp03_catalogs_10yr", class_name = "Centaur", join = 'DiaSource')
        assert expected_query == query

    def test_tno_type_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID, mpc.mpcDesignation, dias.magTrueVband, dias.band FROM dp03_catalogs_10yr.MPCORB AS mpc
    INNER JOIN dp03_catalogs_10yr.DiaSource AS dias ON mpc.ssObjectId = dias.ssObjectId
    WHERE mpc.q/(1-mpc.e) > 30.1 AND mpc.q/(1-mpc.e) < 50.0;"""

        query, class_name = make_query("dp03_catalogs_10yr", class_name = "TNO", join = 'DiaSource')
        assert expected_query == query

    def test_jtrojan_type_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID, mpc.mpcDesignation, dias.magTrueVband, dias.band FROM dp03_catalogs_10yr.MPCORB AS mpc
    INNER JOIN dp03_catalogs_10yr.DiaSource AS dias ON mpc.ssObjectId = dias.ssObjectId
    WHERE mpc.e < 0.3 AND mpc.q/(1-mpc.e) > 4.8 AND mpc.q/(1-mpc.e) < 5.4;"""

        query, class_name = make_query("dp03_catalogs_10yr", class_name = "Jtrojan", join = 'DiaSource')
        assert expected_query == query

    def test_ntrojan_type_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID, mpc.mpcDesignation, dias.magTrueVband, dias.band FROM dp03_catalogs_10yr.MPCORB AS mpc
    INNER JOIN dp03_catalogs_10yr.DiaSource AS dias ON mpc.ssObjectId = dias.ssObjectId
    WHERE mpc.q/(1-mpc.e) > 29.8 AND mpc.q/(1-mpc.e) < 30.4;"""

        query, class_name = make_query("dp03_catalogs_10yr", class_name = "Ntrojan", join = 'DiaSource')
        assert expected_query == query




    ############### PARAMS GIVEN, JOIN: SSObject ###############
    def test_neos_params_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID, mpc.mpcDesignation, sso.g_H, sso.r_H, sso.i_H, sso.discoverySubmissionDate, sso.numObs, (sso.g_H - sso.r_H) AS g_r_color, (sso.r_H - sso.i_H) AS r_i_color FROM dp03_catalogs_10yr.MPCORB AS mpc
    INNER JOIN dp03_catalogs_10yr.SSObject AS sso ON mpc.ssObjectId = sso.ssObjectId
    WHERE mpc.q < 1.3 AND mpc.e < 1.0 AND mpc.q/(1-mpc.e) < 4.0;"""
    
        expected_class_name = "NEO"

        cutoffs = {"q_max": 1.3, "a_max": 4.0, "e_max": 1.0}
        query, class_name = make_query("dp03_catalogs_10yr", class_name = None, cutoffs = cutoffs, join = 'SSObject')

        assert expected_query == query
        assert expected_class_name == class_name

    def test_MBA_params_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID, mpc.mpcDesignation, sso.g_H, sso.r_H, sso.i_H, sso.discoverySubmissionDate, sso.numObs, (sso.g_H - sso.r_H) AS g_r_color, (sso.r_H - sso.i_H) AS r_i_color FROM dp03_catalogs_10yr.MPCORB AS mpc
    INNER JOIN dp03_catalogs_10yr.SSObject AS sso ON mpc.ssObjectId = sso.ssObjectId
    WHERE mpc.q > 1.66 AND mpc.q/(1-mpc.e) > 2.0 AND mpc.q/(1-mpc.e) < 3.2;"""
        expected_class_name = "MBA"

        cutoffs = {"q_min": 1.66, "a_min": 2.0, "a_max": 3.2}
        query, class_name = make_query("dp03_catalogs_10yr", class_name = None, cutoffs = cutoffs, join = 'SSObject')
        
        assert expected_query == query
        assert expected_class_name == class_name
        
    def test_jfc_param_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID, mpc.mpcDesignation, sso.g_H, sso.r_H, sso.i_H, sso.discoverySubmissionDate, sso.numObs, (sso.g_H - sso.r_H) AS g_r_color, (sso.r_H - sso.i_H) AS r_i_color FROM dp03_catalogs_10yr.MPCORB AS mpc
    INNER JOIN dp03_catalogs_10yr.SSObject AS sso ON mpc.ssObjectId = sso.ssObjectId
    WHERE (mpc.q * (1 - mpc.e)) / (5.204 * (1 + mpc.e)) >= 0 AND (5.204 * (1 - mpc.e)) / mpc.q + 2 * COS(RADIANS(mpc.incl)) * SQRT((mpc.q * (1 - mpc.e)) / (5.204 * (1 + mpc.e))) BETWEEN 2.0 AND 3.0;"""

        expected_class_name = "JFC"

        cutoffs = {"tj_min": 2.0, "tj_max": 3.0}
        query, class_name = make_query("dp03_catalogs_10yr", class_name = None, cutoffs = cutoffs, join = 'SSObject')

        assert expected_query == query
        assert expected_class_name == class_name

    def test_lpc_params_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID, mpc.mpcDesignation, sso.g_H, sso.r_H, sso.i_H, sso.discoverySubmissionDate, sso.numObs, (sso.g_H - sso.r_H) AS g_r_color, (sso.r_H - sso.i_H) AS r_i_color FROM dp03_catalogs_10yr.MPCORB AS mpc
    INNER JOIN dp03_catalogs_10yr.SSObject AS sso ON mpc.ssObjectId = sso.ssObjectId
    WHERE mpc.q/(1-mpc.e) > 50.0;"""
        expected_class_name = "LPC"

        cutoffs = {"a_min": 50.0}
        query, class_name = make_query("dp03_catalogs_10yr", class_name = None, cutoffs = cutoffs, join = 'SSObject')
        
        assert expected_query == query
        assert expected_class_name == class_name
        
    def test_centaurs_params_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID, mpc.mpcDesignation, sso.g_H, sso.r_H, sso.i_H, sso.discoverySubmissionDate, sso.numObs, (sso.g_H - sso.r_H) AS g_r_color, (sso.r_H - sso.i_H) AS r_i_color FROM dp03_catalogs_10yr.MPCORB AS mpc
    INNER JOIN dp03_catalogs_10yr.SSObject AS sso ON mpc.ssObjectId = sso.ssObjectId
    WHERE mpc.q/(1-mpc.e) > 5.5 AND mpc.q/(1-mpc.e) < 30.1;"""
        expected_class_name = "Centaur"

        cutoffs = {"a_min": 5.5, "a_max": 30.1}
        query, class_name = make_query("dp03_catalogs_10yr", class_name = None, cutoffs = cutoffs, join = 'SSObject')

        assert expected_query == query
        assert expected_class_name == class_name

    def test_tno_params_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID, mpc.mpcDesignation, sso.g_H, sso.r_H, sso.i_H, sso.discoverySubmissionDate, sso.numObs, (sso.g_H - sso.r_H) AS g_r_color, (sso.r_H - sso.i_H) AS r_i_color FROM dp03_catalogs_10yr.MPCORB AS mpc
    INNER JOIN dp03_catalogs_10yr.SSObject AS sso ON mpc.ssObjectId = sso.ssObjectId
    WHERE mpc.q/(1-mpc.e) > 30.1 AND mpc.q/(1-mpc.e) < 50.0;"""
        expected_class_name = "TNO"

        cutoffs = {"a_min": 30.1, "a_max": 50.0}
        query, class_name = make_query("dp03_catalogs_10yr", class_name = None, cutoffs = cutoffs, join = 'SSObject')

        assert expected_query == query
        assert expected_class_name == class_name

    def test_jtrojans_params_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID, mpc.mpcDesignation, sso.g_H, sso.r_H, sso.i_H, sso.discoverySubmissionDate, sso.numObs, (sso.g_H - sso.r_H) AS g_r_color, (sso.r_H - sso.i_H) AS r_i_color FROM dp03_catalogs_10yr.MPCORB AS mpc
    INNER JOIN dp03_catalogs_10yr.SSObject AS sso ON mpc.ssObjectId = sso.ssObjectId
    WHERE mpc.e < 0.3 AND mpc.q/(1-mpc.e) > 4.8 AND mpc.q/(1-mpc.e) < 5.4;"""
        expected_class_name = "Jtrojan"

        cutoffs = {"a_min": 4.8, "a_max": 5.4, "e_max": 0.3}
        query, class_name = make_query("dp03_catalogs_10yr", class_name = None, cutoffs = cutoffs, join = 'SSObject')
        
        assert expected_query == query
        assert expected_class_name == class_name

    def test_ntrojans_params_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID, mpc.mpcDesignation, sso.g_H, sso.r_H, sso.i_H, sso.discoverySubmissionDate, sso.numObs, (sso.g_H - sso.r_H) AS g_r_color, (sso.r_H - sso.i_H) AS r_i_color FROM dp03_catalogs_10yr.MPCORB AS mpc
    INNER JOIN dp03_catalogs_10yr.SSObject AS sso ON mpc.ssObjectId = sso.ssObjectId
    WHERE mpc.q/(1-mpc.e) > 29.8 AND mpc.q/(1-mpc.e) < 30.4;"""
        expected_class_name = "Ntrojan"

        cutoffs = {"a_min": 29.8, "a_max": 30.4}
        query, class_name = make_query("dp03_catalogs_10yr", class_name = None, cutoffs = cutoffs, join = 'SSObject')
        
        assert expected_query == query
        assert expected_class_name == class_name




class TestQuery_DP1:
    ############### type given, no join ###############
    def test_DP1_neo_type_no_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID, mpc.mpcDesignation FROM dp1_catalogs_10yr.MPCORB AS mpc
    WHERE mpc.q < 1.3 AND mpc.e < 1.0 AND mpc.q/(1-mpc.e) < 4.0;"""

        query, class_name = make_query("dp1_catalogs_10yr", class_name = "NEO")
        assert expected_query == query

    def test_DP1_MBA_type_no_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID, mpc.mpcDesignation FROM dp03_catalogs_10yr.MPCORB AS mpc
    WHERE mpc.q > 1.66 AND mpc.q/(1-mpc.e) > 2.0 AND mpc.q/(1-mpc.e) < 3.2;"""

        query, class_name = make_query("dp03_catalogs_10yr", class_name = "MBA")
        assert expected_query == query

    def test_DP1_jfc_type_no_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID, mpc.mpcDesignation FROM dp03_catalogs_10yr.MPCORB AS mpc
    WHERE (mpc.q * (1 - mpc.e)) / (5.204 * (1 + mpc.e)) >= 0 AND (5.204 * (1 - mpc.e)) / mpc.q + 2 * COS(RADIANS(mpc.incl)) * SQRT((mpc.q * (1 - mpc.e)) / (5.204 * (1 + mpc.e))) BETWEEN 2.0 AND 3.0;"""

        query, class_name = make_query("dp03_catalogs_10yr", class_name = "JFC")
        assert expected_query == query

    def test_DP1_lpc_type_no_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID, mpc.mpcDesignation FROM dp03_catalogs_10yr.MPCORB AS mpc
    WHERE mpc.q/(1-mpc.e) > 50.0;"""

        query, class_name = make_query("dp03_catalogs_10yr", class_name = "LPC")
        assert expected_query == query
    
    def test_DP1_centaurs_type_no_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID, mpc.mpcDesignation FROM dp03_catalogs_10yr.MPCORB AS mpc
    WHERE mpc.q/(1-mpc.e) > 5.5 AND mpc.q/(1-mpc.e) < 30.1;"""

        query, class_name = make_query("dp03_catalogs_10yr", class_name = "Centaur")
        assert expected_query == query

    def test_DP1_tno_type_no_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID, mpc.mpcDesignation FROM dp03_catalogs_10yr.MPCORB AS mpc
    WHERE mpc.q/(1-mpc.e) > 30.1 AND mpc.q/(1-mpc.e) < 50.0;"""

        query, class_name = make_query("dp03_catalogs_10yr", class_name = "TNO")
        assert expected_query == query

    def test_DP1_jtrojan_type_no_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID, mpc.mpcDesignation FROM dp03_catalogs_10yr.MPCORB AS mpc
    WHERE mpc.e < 0.3 AND mpc.q/(1-mpc.e) > 4.8 AND mpc.q/(1-mpc.e) < 5.4;"""

        query, class_name = make_query("dp03_catalogs_10yr", class_name = "Jtrojan")
        assert expected_query == query

    def test_DP1_ntrojan_type_no_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID, mpc.mpcDesignation FROM dp03_catalogs_10yr.MPCORB AS mpc
    WHERE mpc.q/(1-mpc.e) > 29.8 AND mpc.q/(1-mpc.e) < 30.4;"""

        query, class_name = make_query("dp03_catalogs_10yr", class_name = "Ntrojan")
        assert expected_query == query