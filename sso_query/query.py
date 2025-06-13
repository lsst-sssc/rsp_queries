


def make_query(q_cutoff=1.3, e_cutoff=1.0, a_cutoff=10.0):
    query = f"""SELECT foo FROM bar 
        WHERE q < {q_cutoff} AND e < {e_cutoff} AND a < {a_cutoff};"""

    return query

# testing edits
# test 2 -- will it be easier?