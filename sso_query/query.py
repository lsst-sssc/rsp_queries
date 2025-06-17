
# pretty sure we're using the MPCORB 10 year data table, going with that first

def make_query(q_cutoff=1.3, e_cutoff=1.0, a_cutoff=10.0):
    query = f"""e, q, a FROM dp03_catalogs_10yr.MPCORB as mpc "
        WHERE mpc.q < {q_cutoff} AND mpc.e < {e_cutoff} AND mpc.a < {a_cutoff};"""

    return query

    # query takes the e, q, a columns from the MPCORB 10 year catalog, with the cutoff values

