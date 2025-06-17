
# pretty sure we're using the MPCORB 10 year data table, going with that first

def make_query(q_cutoff=1.3, e_cutoff=1.0, a_cutoff=10.0, a_cutoffmin=5.5, class_type = "default"):
    if(class_type == "default"):
        query = f"""SELECT e, q, a FROM dp03_catalogs_10yr.MPCORB as mpc
            WHERE mpc.q < {q_cutoff} AND mpc.e < {e_cutoff} AND mpc.a < {a_cutoff};"""
        return query
        
    elif(class_type == "neos"):
        query = f"""SELECT e, q, a FROM dp03_catalogs_10yr.MPCORB as mpc
        WHERE mpc.q < {q_cutoff} AND mpc.e < {e_cutoff} AND mpc.a > {a_cutoff};"""
        
    elif(class_type == "centaurs"):
        query = f"""SELECT a FROM dp03_catalogs_10yr.MPCORB as mpc
            WHERE mpc.a > {a_cutoffmin} AND mpc.a < {a_cutoff};"""

    elif(class_type == "mbas"):
        query = f"""SELECT a, q FROM dp03_catalogs_10yr.MPCORB as mpc
        WHERE mpc.a > {a_cutoffmin} AND mpc.a < {a_cutoff} AND mpc.q > {q_cutoff};"""

    elif(class_type == "lpcs"):
        query = f"""SELECT a FROM dp03_catalogs_10yr.MPCORB as mpc
            WHERE mpc.a > {a_cutoff};"""

    elif(class_type == "tnos"):
        query = f"""SELECT e, q, a FROM dp03_catalogs_10yr.MPCORB as mpc
            WHERE mpc.a > {a_cutoffmin} AND mpc.a < {a_cutoff};"""

    elif(class_type == "jtrojans"):
        query = f"""SELECT a, e FROM dp03_catalogs_10yr.MPCORB as mpc
            WHERE mpc.a > {a_cutoffmin} AND mpc.a < {a_cutoff} AND mpc.e < {e_cutoff};"""

    elif(class_type == "ntrojans"):
        query = f"""SELECT a FROM dp03_catalogs_10yr.MPCORB as mpc
            WHERE mpc.a > {a_cutoffmin} AND mpc.a < {a_cutoff};"""

    return query

