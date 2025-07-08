from sso_query.query import make_query_general

class TestQuery:

    ############### type given, no join ###############
    def test_neo_type_no_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID FROM dp03_catalogs_10yr.MPCORB as mpc
    WHERE mpc.q < 1.3 AND mpc.e < 1.0 AND mpc.q/(1-mpc.e) < 4.0;"""

        query, object_type = make_query_general(object_type = "NEO")
        assert expected_query == query

    def test_MBA_type_no_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID FROM dp03_catalogs_10yr.MPCORB as mpc
    WHERE mpc.q > 1.66 AND mpc.q/(1-mpc.e) > 2.0 AND mpc.q/(1-mpc.e) < 3.2;"""

        query, object_type = make_query_general(object_type = "MBA")
        assert expected_query == query

    def test_jfc_type_no_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID FROM dp03_catalogs_10yr.MPCORB as mpc
    WHERE (mpc.q * (1 - mpc.e)) / (5.204 * (1 + mpc.e)) >= 0 AND (5.204 * (1 - mpc.e)) / mpc.q + 2 * COS(RADIANS(mpc.incl)) * SQRT((mpc.q * (1 - mpc.e)) / (5.204 * (1 + mpc.e))) BETWEEN 2.0 AND 3.0;"""

        query, object_type = make_query_general(object_type = "JFC")
        assert expected_query == query

    def test_lpc_type_no_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID FROM dp03_catalogs_10yr.MPCORB as mpc
    WHERE mpc.q/(1-mpc.e) > 50;"""

        query, object_type = make_query_general(object_type = "LPC")
        assert expected_query == query
    
    def test_centaurs_type_no_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID FROM dp03_catalogs_10yr.MPCORB as mpc
    WHERE mpc.q/(1-mpc.e) > 5.5 AND mpc.q/(1-mpc.e) < 30.1;"""

        query, object_type = make_query_general(object_type = "Centaur")
        assert expected_query == query

    def test_tno_type_no_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID FROM dp03_catalogs_10yr.MPCORB as mpc
    WHERE mpc.q/(1-mpc.e) > 30.1 AND mpc.q/(1-mpc.e) < 50;"""

        query, object_type = make_query_general(object_type = "TNO")
        assert expected_query == query

    def test_jtrojan_type_no_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID FROM dp03_catalogs_10yr.MPCORB as mpc
    WHERE mpc.e < 0.3 AND mpc.q/(1-mpc.e) > 4.8 AND mpc.q/(1-mpc.e) < 5.4;"""

        query, object_type = make_query_general(object_type = "Jtrojan")
        assert expected_query == query

    def test_ntrojan_type_no_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID FROM dp03_catalogs_10yr.MPCORB as mpc
    WHERE mpc.q/(1-mpc.e) > 29.8 AND mpc.q/(1-mpc.e) < 30.4;"""

        query, object_type = make_query_general(object_type = "Ntrojan")
        assert expected_query == query

    
    ############### params given, no join ###############
    def test_neos_params_no_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID FROM dp03_catalogs_10yr.MPCORB as mpc
    WHERE mpc.q < 1.3 AND mpc.e < 1.0 AND mpc.q/(1-mpc.e) < 4.0;"""
        expected_object_type = "NEO"

        query, object_type = make_query_general(q_cutoff=1.3, a_cutoff=4.0, e_cutoff = 1.0)

        assert expected_query == query
        assert expected_object_type == object_type
        
    def test_MBA_params_no_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID FROM dp03_catalogs_10yr.MPCORB as mpc
    WHERE mpc.q > 1.66 AND mpc.q/(1-mpc.e) > 2.0 AND mpc.q/(1-mpc.e) < 3.2;"""
        expected_object_type = "MBA"

        query, object_type = make_query_general(a_cutoff = 3.2, a_cutoff_min = 2.0, q_cutoff_min = 1.66)
        assert expected_query == query
        assert expected_object_type == object_type

    def test_jfc_params_no_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID FROM dp03_catalogs_10yr.MPCORB as mpc
    WHERE (mpc.q * (1 - mpc.e)) / (5.204 * (1 + mpc.e)) >= 0 AND (5.204 * (1 - mpc.e)) / mpc.q + 2 * COS(RADIANS(mpc.incl)) * SQRT((mpc.q * (1 - mpc.e)) / (5.204 * (1 + mpc.e))) BETWEEN 2.0 AND 3.0;"""
        expected_object_type = "JFC"

        query, object_type = make_query_general(t_cutoff_min = 2.0, t_cutoff = 3.0)
        assert expected_query == query
        assert expected_object_type == object_type

    def test_lpc_params_no_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID FROM dp03_catalogs_10yr.MPCORB as mpc
    WHERE mpc.q/(1-mpc.e) > 50;"""
        expected_object_type = "LPC"

        query, object_type = make_query_general(a_cutoff_min = 50)
        assert expected_query == query
        assert expected_object_type == object_type
        
    def test_centaurs_params_no_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID FROM dp03_catalogs_10yr.MPCORB as mpc
    WHERE mpc.q/(1-mpc.e) > 5.5 AND mpc.q/(1-mpc.e) < 30.1;"""
        expected_object_type = "Centaur"

        query, object_type = make_query_general(a_cutoff = 30.1, a_cutoff_min = 5.5)

        assert expected_query == query
        assert expected_object_type == object_type
        
    def test_tno_params_no_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID FROM dp03_catalogs_10yr.MPCORB as mpc
    WHERE mpc.q/(1-mpc.e) > 30.1 AND mpc.q/(1-mpc.e) < 50;"""
        expected_object_type = "TNO"

        query, object_type = make_query_general(a_cutoff_min = 30.1, a_cutoff = 50)

        assert expected_query == query
        assert expected_object_type == object_type

    def test_jtrojans_params_no_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID FROM dp03_catalogs_10yr.MPCORB as mpc
    WHERE mpc.e < 0.3 AND mpc.q/(1-mpc.e) > 4.8 AND mpc.q/(1-mpc.e) < 5.4;"""
        expected_object_type = "Jtrojan"

        query, object_type = make_query_general(a_cutoff_min = 4.8, a_cutoff = 5.4, e_cutoff = 0.3)
        assert expected_query == query
        assert expected_object_type == object_type

    def test_ntrojans_params_no_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID FROM dp03_catalogs_10yr.MPCORB as mpc
    WHERE mpc.q/(1-mpc.e) > 29.8 AND mpc.q/(1-mpc.e) < 30.4;"""
        expected_object_type = "Ntrojan"

        query, object_type = make_query_general(a_cutoff_min = 29.8, a_cutoff = 30.4)
        assert expected_query == query
        assert expected_object_type == object_type

    
    ############### TYPE GIVEN, JOIN ###############
    def test_neo_type_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID, dias.magTrueVband, dias.band FROM dp03_catalogs_10yr.MPCORB as mpc
    INNER JOIN dp03_catalogs_10yr.DiaSource AS dias ON mpc.ssObjectId = dias.ssObjectId
    WHERE mpc.q < 1.3 AND mpc.e < 1.0 AND mpc.q/(1-mpc.e) < 4.0;"""

        query, object_type = make_query_general(object_type = "NEO", join = 'Diasource')
        assert expected_query == query

    def test_MBA_type_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID, dias.magTrueVband, dias.band FROM dp03_catalogs_10yr.MPCORB as mpc
    INNER JOIN dp03_catalogs_10yr.DiaSource AS dias ON mpc.ssObjectId = dias.ssObjectId
    WHERE mpc.q > 1.66 AND mpc.q/(1-mpc.e) > 2.0 AND mpc.q/(1-mpc.e) < 3.2;"""
        
        query, object_type = make_query_general(object_type = "MBA", join = 'Diasource')
        assert expected_query == query

    def test_jfc_type_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID, dias.magTrueVband, dias.band FROM dp03_catalogs_10yr.MPCORB as mpc
    INNER JOIN dp03_catalogs_10yr.DiaSource AS dias ON mpc.ssObjectId = dias.ssObjectId
    WHERE (mpc.q * (1 - mpc.e)) / (5.204 * (1 + mpc.e)) >= 0 AND (5.204 * (1 - mpc.e)) / mpc.q + 2 * COS(RADIANS(mpc.incl)) * SQRT((mpc.q * (1 - mpc.e)) / (5.204 * (1 + mpc.e))) BETWEEN 2.0 AND 3.0;"""

        query, object_type = make_query_general(object_type = "JFC", join = 'Diasource')
        assert expected_query == query

    def test_lpc_type_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID, dias.magTrueVband, dias.band FROM dp03_catalogs_10yr.MPCORB as mpc
    INNER JOIN dp03_catalogs_10yr.DiaSource AS dias ON mpc.ssObjectId = dias.ssObjectId
    WHERE mpc.q/(1-mpc.e) > 50;"""

        query, object_type = make_query_general(object_type = "LPC", join = 'Diasource')
        assert expected_query == query

    def test_centaur_type_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID, dias.magTrueVband, dias.band FROM dp03_catalogs_10yr.MPCORB as mpc
    INNER JOIN dp03_catalogs_10yr.DiaSource AS dias ON mpc.ssObjectId = dias.ssObjectId
    WHERE mpc.q/(1-mpc.e) > 5.5 AND mpc.q/(1-mpc.e) < 30.1;"""

        query, object_type = make_query_general(object_type = "Centaur", join = 'Diasource')
        assert expected_query == query

    def test_tno_type_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID, dias.magTrueVband, dias.band FROM dp03_catalogs_10yr.MPCORB as mpc
    INNER JOIN dp03_catalogs_10yr.DiaSource AS dias ON mpc.ssObjectId = dias.ssObjectId
    WHERE mpc.q/(1-mpc.e) > 30.1 AND mpc.q/(1-mpc.e) < 50;"""

        query, object_type = make_query_general(object_type = "TNO", join = 'Diasource')
        assert expected_query == query

    def test_jtrojan_type_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID, dias.magTrueVband, dias.band FROM dp03_catalogs_10yr.MPCORB as mpc
    INNER JOIN dp03_catalogs_10yr.DiaSource AS dias ON mpc.ssObjectId = dias.ssObjectId
    WHERE mpc.e < 0.3 AND mpc.q/(1-mpc.e) > 4.8 AND mpc.q/(1-mpc.e) < 5.4;"""

        query, object_type = make_query_general(object_type = "Jtrojan", join = 'Diasource')
        assert expected_query == query

    def test_ntrojan_type_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID, dias.magTrueVband, dias.band FROM dp03_catalogs_10yr.MPCORB as mpc
    INNER JOIN dp03_catalogs_10yr.DiaSource AS dias ON mpc.ssObjectId = dias.ssObjectId
    WHERE mpc.q/(1-mpc.e) > 29.8 AND mpc.q/(1-mpc.e) < 30.4;"""

        query, object_type = make_query_general(object_type = "Ntrojan", join = 'Diasource')
        assert expected_query == query


    ############### PARAMS GIVEN, JOIN ###############
    def test_neos_params_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID, dias.magTrueVband, dias.band FROM dp03_catalogs_10yr.MPCORB as mpc
    INNER JOIN dp03_catalogs_10yr.DiaSource AS dias ON mpc.ssObjectId = dias.ssObjectId
    WHERE mpc.q < 1.3 AND mpc.e < 1.0 AND mpc.q/(1-mpc.e) < 4.0;"""
        expected_object_type = "NEO"

        query, object_type = make_query_general(q_cutoff=1.3, a_cutoff=4.0, e_cutoff = 1.0, join = 'Diasource')

        assert expected_query == query
        assert expected_object_type == object_type

        # q < 1.3 au (a > 4, e < 1)
        
    def test_MBA_params_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID, dias.magTrueVband, dias.band FROM dp03_catalogs_10yr.MPCORB as mpc
    INNER JOIN dp03_catalogs_10yr.DiaSource AS dias ON mpc.ssObjectId = dias.ssObjectId
    WHERE mpc.q > 1.66 AND mpc.q/(1-mpc.e) > 2.0 AND mpc.q/(1-mpc.e) < 3.2;"""
        expected_object_type = "MBA"

        query, object_type = make_query_general(a_cutoff = 3.2, a_cutoff_min = 2.0, q_cutoff_min = 1.66, join = 'Diasource')
        assert expected_query == query
        assert expected_object_type == object_type
        
    def test_jfc_param_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID, dias.magTrueVband, dias.band FROM dp03_catalogs_10yr.MPCORB as mpc
    INNER JOIN dp03_catalogs_10yr.DiaSource AS dias ON mpc.ssObjectId = dias.ssObjectId
    WHERE (mpc.q * (1 - mpc.e)) / (5.204 * (1 + mpc.e)) >= 0 AND (5.204 * (1 - mpc.e)) / mpc.q + 2 * COS(RADIANS(mpc.incl)) * SQRT((mpc.q * (1 - mpc.e)) / (5.204 * (1 + mpc.e))) BETWEEN 2.0 AND 3.0;"""

        expected_object_type = "JFC"

        query, object_type = make_query_general(t_cutoff_min = 2.0, t_cutoff = 3.0, join = 'Diasource')

        assert expected_query == query
        assert expected_object_type == object_type

    ####################
    def test_lpc_params_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID, dias.magTrueVband, dias.band FROM dp03_catalogs_10yr.MPCORB as mpc
    INNER JOIN dp03_catalogs_10yr.DiaSource AS dias ON mpc.ssObjectId = dias.ssObjectId
    WHERE mpc.q/(1-mpc.e) > 50;"""
        expected_object_type = "LPC"

        query, object_type = make_query_general(a_cutoff_min = 50, join = 'Diasource')
        assert expected_query == query
        assert expected_object_type == object_type
        
    def test_centaurs_params_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID, dias.magTrueVband, dias.band FROM dp03_catalogs_10yr.MPCORB as mpc
    INNER JOIN dp03_catalogs_10yr.DiaSource AS dias ON mpc.ssObjectId = dias.ssObjectId
    WHERE mpc.q/(1-mpc.e) > 5.5 AND mpc.q/(1-mpc.e) < 30.1;"""
        expected_object_type = "Centaur"

        query, object_type = make_query_general(a_cutoff = 30.1, a_cutoff_min = 5.5, join = 'Diasource')

        assert expected_query == query
        assert expected_object_type == object_type

        
    def test_tno_params_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID, dias.magTrueVband, dias.band FROM dp03_catalogs_10yr.MPCORB as mpc
    INNER JOIN dp03_catalogs_10yr.DiaSource AS dias ON mpc.ssObjectId = dias.ssObjectId
    WHERE mpc.q/(1-mpc.e) > 30.1 AND mpc.q/(1-mpc.e) < 50;"""
        expected_object_type = "TNO"

        query, object_type = make_query_general(a_cutoff_min = 30.1, a_cutoff = 50, join = 'Diasource')

        assert expected_query == query
        assert expected_object_type == object_type

        # 5.5 au < a < 30.1 au

    def test_jtrojans_params_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID, dias.magTrueVband, dias.band FROM dp03_catalogs_10yr.MPCORB as mpc
    INNER JOIN dp03_catalogs_10yr.DiaSource AS dias ON mpc.ssObjectId = dias.ssObjectId
    WHERE mpc.e < 0.3 AND mpc.q/(1-mpc.e) > 4.8 AND mpc.q/(1-mpc.e) < 5.4;"""
        expected_object_type = "Jtrojan"

        query, object_type = make_query_general(a_cutoff_min = 4.8, a_cutoff = 5.4, e_cutoff = 0.3, join = 'Diasource')
        assert expected_query == query
        assert expected_object_type == object_type

    def test_ntrojans_params_join(self):
        expected_query = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID, dias.magTrueVband, dias.band FROM dp03_catalogs_10yr.MPCORB as mpc
    INNER JOIN dp03_catalogs_10yr.DiaSource AS dias ON mpc.ssObjectId = dias.ssObjectId
    WHERE mpc.q/(1-mpc.e) > 29.8 AND mpc.q/(1-mpc.e) < 30.4;"""
        expected_object_type = "Ntrojan"

        query, object_type = make_query_general(a_cutoff_min = 29.8, a_cutoff = 30.4, join = 'Diasource')
        assert expected_query == query
        assert expected_object_type == object_type

    
    def test_join_SSObject_neos(self):
        expected_query = f"""SELECT mpc.ssObjectId, mpc.mpcDesignation, mpc.e, mpc.q, mpc.incl, sso.g_H, sso.r_H, sso.i_H, sso.discoverySubmissionDate, sso.numObs, (sso.g_H - sso.r_H) AS g_r_color, (sso.r_H - sso.i_H) AS r_i_color FROM dp03_catalogs_10yr.MPCORB as mpc INNER JOIN dp03_catalogs_10yr.SSObject as sso ON mpc.ssObjectId = sso.ssObjectId WHERE mpc.q <= 1.3 AND mpc.e <= 1.0 AND mpc.q / (1 - mpc.e) <= 4.0 ORDER by mpc.mpcDesignation"""
        
        query_cutoffs = make_query('dp03_catalogs_10yr', cutoffs={'q_max': 1.3, 'e_max': 1.0, 'a_max': 4.0}, join_SSObject=True)
        query_class = make_query('dp03_catalogs_10yr', 'neos', join_SSObject=True)

        assert expected_query == query_cutoffs 
        assert expected_query == query_class
