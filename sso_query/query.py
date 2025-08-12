from astropy.table import Table
from IPython.display import display
from lsst.rsp import get_tap_service
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np
import pandas as pd

service = get_tap_service("ssotap")
assert service is not None

#################### Global ####################
ORBITAL_CLASS_CUTOFFS = {
    "LPC": {"a_min": 50.0},
    "TNO": {"a_min": 30.1, "a_max": 50.0},
    "Ntrojan": {"a_min": 29.8, "a_max": 30.4},
    "NEO": {"q_max": 1.3, "a_max": 4.0, "e_max": 1.0},
    "MBA": {"q_min": 1.66, "a_min": 2.0, "a_max": 3.2},
    "Centaur": {"a_min": 5.5, "a_max": 30.1},
    "Jtrojan": {"a_min": 4.8, "a_max": 5.4, "e_max": 0.3},
    "JFC": {"tj_min": 2.0, "tj_max": 3.0}
}
################################################

def make_query(catalog:str, class_name:str = None, cutoffs:dict = None, join:str = None, limit:int = None):
    """
    Creates an MPCORB table query from the catalog based on either a class_name or cutoffs dict.
    Creates a query from MPCORB 10-year table using the specificed catalog and class name OR cutoffs. Can join the MPCORB table with DiaSource or SSObject.
    Args:
        catalog (str): Name of RSP catalog to query.
        class_name = None (str) (optional): Name of orbital class.
        cutoffs = None (dict) (optional): Dictionaryof  orbital constraints (keys, str) and desired/input values (values, floats). 
        join = None (str) (optional): Table to join with MPCORB table. 
            DiaSource, SSObject
        limit (int) (optional): Row limit on query.
    Returns:
        query (str): Query string for the specified constraints.
        class_name (str): Name of orbital class. Useful if orbital cutoff parameters provided. 
    """

    ### Classification ###

    # Errors #
    if (class_name is None and cutoffs is None): # Class name and cutoffs not provided
        raise ValueError("Please provide a class name ('class_name') OR desired orbital parameters ('cutoffs').")
    if (class_name is not None and cutoffs is not None): # Both class name and cutoffs provided
        raise ValueError("Provide exactly one of: 'class_name', 'cutoffs'.")

    default_cutoffs = {'q_min': None, 'q_max': None, 'e_min': None, 'e_max': None, 'a_min': None, 'a_max': None, 'tj_min': None, 'tj_max': None}

    if catalog == "dp03_catalogs_10yr":
        service = get_tap_service("ssotap") # 'tap' for DP03
    elif catalog == "dp1":
        service = get_tap_service("tap") # 'tap' for DP1
    else:
        raise ValueError("Please enter a valid catalog.")

    assert service is not None

    # Classification #
    if cutoffs is not None: # given parameters, find object type #
        cutoffs = {**default_cutoffs, **cutoffs} # user inputs cutoffs overlay default cutoffs
        for class_type, cutoff_dict in ORBITAL_CLASS_CUTOFFS.items(): # each "value" is a dictionary
            match = True
            for parameter, value in cutoff_dict.items(): # Ex: parameter = a_min, value = 50.0
                current_param_check = cutoffs.get(parameter) # cutoffs is user inputs, Ex: parameter = a_min, value = user input int
                if current_param_check is None: # if parameter not defined by user
                    match = False
                    break
                # know parameter is defined, checking compatability with known constraints
                if parameter[-3:] == "min": #if parameter.endswith("min")
                    if current_param_check < value: # passes if >=
                        match = False
                        break
                else: # if not min
                    if current_param_check > value: #passes if <=
                        match = False
                        break
            if match is True: #breaks if all conditions match a 
                class_name = class_type
                break

    elif class_name is not None: # given a type, need to find parameters #
        if class_name in ORBITAL_CLASS_CUTOFFS:
            cutoffs = ORBITAL_CLASS_CUTOFFS[class_name]
        else:
            raise ValueError("Invalid class_name.")
            
    cutoffs = {**default_cutoffs, **cutoffs}

    
    ### Join ###
    select_fields = ["mpc.incl", "mpc.q", "mpc.e", "mpc.ssObjectID", "mpc.mpcDesignation"]
    join_clause = ""

    if join:
        # DiaSource join
        if join == "DiaSource":
            join_clause = f"""
    INNER JOIN {catalog}.DiaSource AS dias ON mpc.ssObjectId = dias.ssObjectId"""
            try:
                sso_results = service.search(f"SELECT column_name from TAP_SCHEMA.columns WHERE table_name = '{catalog}.DiaSource'")
                sso_table = sso_results.to_table().to_pandas()
                available_fields = sso_table['column_name'].tolist()

                if catalog == "dp03_catalogs_10yr":
                    desired_fields = ["dias.magTrueVband", "dias.band"]
                elif catalog == "dp1":
                    desired_fields = ["dias.apFlux", "dias.apFlux_flag", "dias.apFluxErr", "dias.band"]
    
                present_fields = [field for field in desired_fields if field.split(".")[1] in available_fields]
                select_fields += present_fields

                print(f"Querying {catalog}.DiaSource for: {present_fields}")
                
            except Exception as e:
                print(f"{catalog} query failed, no schema of interest in catalog: {e}")

        # SSObject join
        elif join == "SSObject":
            join_clause = f"""
    INNER JOIN {catalog}.SSObject AS sso ON mpc.ssObjectId = sso.ssObjectId"""
            try:
                sso_results = service.search(f"SELECT column_name from TAP_SCHEMA.columns WHERE table_name = '{catalog}.SSObject'")
                sso_table = sso_results.to_table().to_pandas()
                available_fields = sso_table['column_name'].tolist()

                if catalog == "dp03_catalogs_10yr":
                    desired_fields = ["sso.g_H", "sso.r_H", "sso.i_H", "sso.discoverySubmissionDate", "sso.numObs"]
                elif catalog == "dp1":
                    desired_fields = ["sso.discoverySubmissionDate", "sso.numObs"]
    
                present_fields = [field for field in desired_fields if field.split(".")[1] in available_fields]
                select_fields += present_fields
    
                if "g_H" in available_fields and "r_H" in available_fields:
                    select_fields.append("(sso.g_H - sso.r_H) AS g_r_color")
                if "r_H" in available_fields and "i_H" in available_fields:
                    select_fields.append("(sso.r_H - sso.i_H) AS r_i_color")
                    
                print(f"Querying {catalog}.SSObject for: {present_fields}")
    
            except Exception as e:
                print(f"{catalog} query failed, no schema of interest in catalog: {e}")

    ### Cutoff conditions ###
    conditions = []

    if cutoffs['q_min'] is not None:
        conditions.append(f"mpc.q > {cutoffs['q_min']}")
    if cutoffs['q_max'] is not None:
        conditions.append(f"mpc.q < {cutoffs['q_max']}")
    if cutoffs['e_min'] is not None:
        conditions.append(f"mpc.e > {cutoffs['e_min']}")
    if cutoffs['e_max'] is not None:
        conditions.append(f"mpc.e < {cutoffs['e_max']}")
    if cutoffs['a_min'] is not None:
        conditions.append(f"mpc.q/(1-mpc.e) > {cutoffs['a_min']}")
    if cutoffs['a_max'] is not None:
        conditions.append(f"mpc.q/(1-mpc.e) < {cutoffs['a_max']}")
    if cutoffs['tj_min'] is not None and cutoffs['tj_max'] is not None:
        conditions.append(f"(mpc.q * (1 - mpc.e)) / (5.204 * (1 + mpc.e)) >= 0")
        conditions.append(f"(5.204 * (1 - mpc.e)) / mpc.q + 2 * COS(RADIANS(mpc.incl)) * SQRT((mpc.q * (1 - mpc.e)) / (5.204 * (1 + mpc.e))) BETWEEN {cutoffs['tj_min']} AND {cutoffs['tj_max']}")


    ### Writing Query ###
    query_start = f"SELECT {', '.join(select_fields)} FROM {catalog}.MPCORB AS mpc{join_clause}"
    query_WHERE = f"""
    WHERE"""
    query = query_start + query_WHERE + " " + " AND ".join(conditions)
    if limit is not None:
        query_limit = f"""
    LIMIT """ + str(limit)
        query = query + query_limit
    query = query + ";"

    return query, class_name



def run_query(query_string, class_name, catalog = "dp1", to_pandas = False):
    """
    Function runs SSOtap using query_string. Default returns data in the form of an AstroPy Table. Returns with 'a' and 'class_name' columns.
    Args:
        query_string (str): String representing query to pass to SSOtap.
        class_name (str): Name of class of objects within query. 
        catalog = "dp1" (str)(optional): String representing which catalog is being queried. 
        to_pandas = False (bool) (optional): Boolean representing whether or not to convert job results to pandas table. Default is an AstroPy table.
    Returns: 
        unique_objects: Data table with the job results. 
    """
    
    # getting the Rubin tap service client 
    if catalog == "dp03_catalogs_10yr":
        service = get_tap_service("ssotap") # 'tap' for DP03
    elif catalog == "dp1":
        service = get_tap_service("tap") # 'tap' for DP1
    else:
        raise ValueError("Please enter a valid catalog.")

    assert service is not None

    # running the job
    job = service.submit_job(query_string)
    job.run()
    job.wait(phases=['COMPLETED', 'ERROR'])
    print('Job phase is', job.phase)
    if job.phase == 'ERROR':
        job.raise_if_error()

    assert job.phase == 'COMPLETED'
    result = job.fetch_result()

    # Errors for table #
    # Check if table has no values or is None
    if result is None or len(result) == 0:
        print("ValueError: Results table is empty or None. Check input cutoffs.")
        return result


    # turning results into pandas table
    # adding 'a' and 'class_name' columns
    table = pd.DataFrame(result)
    a = calc_semimajor_axis(table['q'], table['e'])
    table['a'] = a
    table['class_name'] = class_name

    if to_pandas is False: #AstroPy table
        table = Table.from_pandas(table)
        print(table[0:20]) # print first 20 rows 
    else: #pandas table
        display(table.head(20))  # Show just the first 20 rows
    
    return table


def calc_semimajor_axis(q, e):
    """
    Given a perihelion distance and orbital eccentricity,
    calculate the semi-major axis of the orbit.
    Args: 
        q (ndarray): Distance at perihelion, in au.
        e (ndarray): Orbital eccentricity.

    Returns:
        a (ndarray): Semi-major axis of the orbit, in au. Dervied from: q = a(1-e), so a = q/(1-e)
    """
    
    return q / (1.0 - e)

def calc_magnitude(apFlux):
    """
    Given a difference image flux, calculates the magnitude. 
    Args:
        apFlux (ndarray): Flux. 
    Returns:
        mags (ndarray): Converted magnitudes.
    """
    return -2.5 * np.log10(apFlux) + 31.4
