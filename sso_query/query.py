
# MPCORB 10-year data table
# ordered in terms of specificity - narrow cases first

def make_query(q_cutoff = 1.0, e_cutoff = 0.5, a_cutoff = 5.0, a_cutoff_min = 5.0): #q_cutoff=1.3, e_cutoff=1.0, a_cutoff=10.0, a_cutoffmin=5.5
    query_start = f"""SELECT a, q, e FROM dp03_catalogs_10yr.MPCORB as mpc
            WHERE """
    
    # centaurs
    if(a_cutoff >= 30.1 and a_cutoff_min <= 5.5):
        query = query_start + f"mpc.a > {a_cutoff_min} AND mpc.a < {a_cutoff};"
        # 5.5 au < a < 30.1 au
    
    # mbas
    elif(a_cutoff >= 3.2 and a_cutoff_min <= 2.0 and q_cutoff >= 1.66):
        query = query_start + f"mpc.a > {a_cutoff_min} AND mpc.a < {a_cutoff} AND mpc.q > {q_cutoff};"
        # 2.0 au < a < 3.2 au, q > 1.66 au

    # lpcs
    elif(a_cutoff_min >= 50):
        query = query_start + f"mpc.a > {a_cutoff_min};"
        # a > 50 au

    # tnos
    elif(a_cutoff <= 50 and a_cutoff_min >= 30.1):
        query = query_start + f"mpc.a > {a_cutoff_min} AND mpc.a < {a_cutoff};"
        # 30.1 au < a < 50 au


    # jtrojans
    elif(a_cutoff_min >= 4.8 and a_cutoff <= 5.4 and e_cutoff <= 0.3):
        query = query_start + f"mpc.a > {a_cutoff_min} AND mpc.a < {a_cutoff} AND mpc.e < {e_cutoff};"
        # 4.8 au < a < 5.4 au, e < 0.3


    # ntrojans
    elif(a_cutoff_min >= 29.8 and a_cutoff <= 30.4):
        query = query_start + f"mpc.a > {a_cutoff_min} AND mpc.a < {a_cutoff};"
        # 29.8 au < a < 30.4 au
        

        # neos
    elif(q_cutoff <= 1.3 and a_cutoff >= 4 and e_cutoff <= 1):
        query = query_start + f"mpc.q < {q_cutoff} AND mpc.e < {e_cutoff} AND mpc.a > {a_cutoff};"
        # q < 1.3, e < 1, a > 4.0

    return query


