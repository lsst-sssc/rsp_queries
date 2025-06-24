def make_query(q_min=None, q_max=None, e_min=None, e_max=None, a_min=None, a_max=None):
    start_query = f"""SELECT mpc.ssObjectId, mpc.mpcDesignation, mpc.e, mpc.q, mpc.incl FROM dp03_catalogs_10yr.MPCORB as mpc WHERE """

    # LPCs: a >= 50.0
    if (a_min is not None and a_min >=50.0):
        query = start_query + f"mpc.q/(1.0-mpc.e) >= {a_min} ORDER by mpc.mpcDesignation"

    # Centaurs: 5.5 < a < 30.1
    if (a_min is not None and a_min >= 5.5 and
        a_max is not None and a_max <= 30.1):
        query = start_query + f"mpc.q/(1.0-mpc.e) >= {a_min} AND mpc.q/(1.0-mpc.e) <= {a_max} ORDER by mpc.mpcDesignation"
    
    # TNOs: 30.1 < a < 50
    if (a_min is not None and a_min >= 30.1 and
        a_max is not None and a_max <= 50.0):
        query = start_query + f"mpc.q/(1.0-mpc.e) >= {a_min} AND mpc.q/(1.0-mpc.e) <= {a_max} ORDER by mpc.mpcDesignation" 

    # Neptunian Trojans: 29.8 < a < 30.4
    if (a_min is not None and a_min >= 29.8 and
        a_max is not None and a_max <= 30.4):
        query = start_query + f"mpc.q/(1.0-mpc.e) >= {a_min} AND mpc.q/(1.0-mpc.e) <= {a_max} ORDER by mpc.mpcDesignation" 

    # Jupiter Trojans: e < 0.3, 4.8 < a < 5.4
    if (e_max is not None and e_max <= 0.3 and
        a_min is not None and a_min >= 4.8 and
        a_max is not None and a_max <= 5.4):
        query = start_query + f"mpc.e <= {e_max} AND mpc.q/(1.0-mpc.e) >= {a_min} AND mpc.q/(1.0-mpc.e) <= {a_max} ORDER by mpc.mpcDesignation"
    
    # MBAs: q > 1.66, 2.0 < a < 3.2
    if (q_min is not None and q_min >= 1.66 and 
        a_min is not None and a_min >= 2.0 and 
        a_max is not None and a_max <= 3.2):
        query = start_query + f"mpc.q >= {q_min} AND mpc.q/(1.0-mpc.e) >= {a_min} AND mpc.q/(1.0-mpc.e) <= {a_max} ORDER by mpc.mpcDesignation"
    
    # NEOs: q < 1.3, e < 1.0, a > 4.0
    elif (q_max is not None and q_max <= 1.3 and 
          e_max is not None and e_max <= 1.0 and 
          a_min is not None and a_min >= 4.0):
        query = start_query + f"mpc.q <= {q_max} AND mpc.e <= {e_max} AND mpc.q/(1.0-mpc.e) >= {a_min} ORDER by mpc.mpcDesignation"
        
    return query
