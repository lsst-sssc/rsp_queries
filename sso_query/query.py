
# MPCORB 10-year data table
# ordered in terms of specificity - narrow cases first

def make_query(q_cutoff_min = None, q_cutoff = None, e_cutoff_min = None, e_cutoff = None, a_cutoff = None, a_cutoff_min = None): 
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


