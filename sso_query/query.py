
# MPCORB 10-year data table
# ordered in terms of specificity - narrow cases first

def make_query(q_cutoff_min = None, q_cutoff = None, e_cutoff_min = None, e_cutoff = None, a_cutoff = None, a_cutoff_min = None): 
    """
    Function creates a string query that can be passed to SSOtap. 
    Args:
        q_cutoff_min: Float representing the minimum distance at perihelion, in au.
        q_cutoff: Float representing the max distance at perihelion, in au. 
        e_cutoff_min: Float representing the minimum orbital eccentricity.
        e_cutoff: Float representing the max orbital eccentricity. 
        a_cutoff_min: Float representing the minimum semi-major axis of the orbit, in au.
        a_cutoff: Float representing the max semi-major axis of the orbit, in au.
    Returns:
        query: String representing query that can be passed to SSOtap.
        
    """
    query_start = f"""SELECT q/(1-e) as a, q, e FROM dp03_catalogs_10yr.MPCORB as mpc
            WHERE"""
    conditions = []

    if q_cutoff_min is not None:
        conditions.append(f"mpc.q > {q_cutoff_min}")
    if q_cutoff is not None:
        conditions.append(f"mpc.q < {q_cutoff}")
    if e_cutoff_min is not None:
        conditions.append(f"mpc.e > {e_cutoff_min}")
    if e_cutoff is not None:
        conditions.append(f"mpc.e < {e_cutoff}")
    if a_cutoff_min is not None:
        conditions.append(f"mpc.a > {a_cutoff_min}")
    if a_cutoff is not None:
        conditions.append(f"mpc.a < {a_cutoff}")

    query = query_start + " " + " AND ".join(conditions)
    query = query + ";"

    return query

def run_query(query_string)


