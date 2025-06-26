
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

def run_query(query_string, to_pandas = False):
    """
    Function runs SSOtap using query_string. Default returns data in the form of an AstroPy Table.
    Args:
        query_string: String representing query to pass to SSOtap.
        return_item: String representing the type of dataframe to return with queried data. 
        to_pandas: Boolean representing whether or not to convert job results to pandas table. Default is an AstroPy table.
    """
    # getting the Rubin tap service client 
    service = get_tap_service("ssotap")
    assert service is not None
    
    # running the job
    job = service.submit_job(query_string)
    job.run()
    job.wait(phases=['COMPLETED', 'ERROR'])
    print('Job phase is', job.phase)
    if to_pandas is False: #AstroPy table
        unique_objects = job.fetch_result().to_table()
        print(unique_objects[0:5]) # print first few rows 
    else: #pandas table
        unique_objects = job.fetch_result().to_table().to_pandas()
        print(unique_objects.head(5)) # print first five rows
    assert job.phase == 'COMPLETED'

    return unique_objects


