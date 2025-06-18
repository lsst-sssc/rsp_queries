
# MPCORB 10-year data table
# ordered in terms of specificity - narrow cases first, broader cases last

def make_query(q_cutoff = 1.0, e_cutoff = 0.5, a_cutoff = 5.0, a_cutoff_min = 5.0): #q_cutoff=1.3, e_cutoff=1.0, a_cutoff=10.0, a_cutoffmin=5.5
    # centaurs
    if(a_cutoff >= 30.1 and a_cutoff_min <= 5.5):
        query = f"""SELECT a FROM dp03_catalogs_10yr.MPCORB as mpc
            WHERE mpc.a > {a_cutoff_min} AND mpc.a < {a_cutoff};"""
        return query
        # 5.5 au < a < 30.1 au
    
    # mbas
    if(a_cutoff >= 3.2 and a_cutoff_min <= 2.0 and q_cutoff >= 1.66):
        query = f"""SELECT a, q FROM dp03_catalogs_10yr.MPCORB as mpc
            WHERE mpc.a > {a_cutoff_min} AND mpc.a < {a_cutoff} AND mpc.q > {q_cutoff};"""
        return query
        # 2.0 au < a < 3.2 au, q > 1.66 au

    # lpcs
    if(a_cutoff_min >= 50):
        query = f"""SELECT a FROM dp03_catalogs_10yr.MPCORB as mpc
            WHERE mpc.a > {a_cutoff_min};"""
        return query
        # a > 50 au

    # tnos
    if(a_cutoff <= 50 and a_cutoff_min >= 30.1):
        query = f"""SELECT a FROM dp03_catalogs_10yr.MPCORB as mpc
            WHERE mpc.a > {a_cutoff_min} AND mpc.a < {a_cutoff};"""
        return query
        # 30.1 au < a < 50 au


    # jtrojans
    if(a_cutoff_min >= 4.8 and a_cutoff <= 5.4 and e_cutoff <= 0.3):
        query = f"""SELECT a, e FROM dp03_catalogs_10yr.MPCORB as mpc
            WHERE mpc.a > {a_cutoff_min} AND mpc.a < {a_cutoff} AND mpc.e < {e_cutoff};"""
        return query
        # 4.8 au < a < 5.4 au, e < 0.3


    # ntrojans
    if(a_cutoff_min >= 29.8 and a_cutoff <= 30.4):
        query = f"""SELECT a FROM dp03_catalogs_10yr.MPCORB as mpc
            WHERE mpc.a > {a_cutoff_min} AND mpc.a < {a_cutoff};"""
        return query
        # 29.8 au < a < 30.4 au
        

        # neos
    if(q_cutoff <= 1.3 and a_cutoff >= 4 and e_cutoff <= 1):
        query = f"""SELECT e, q, a FROM dp03_catalogs_10yr.MPCORB as mpc
            WHERE mpc.q < {q_cutoff} AND mpc.e < {e_cutoff} AND mpc.a > {a_cutoff};"""
        return query
        # q < 1.3, e < 1, a > 4.0


    return query

