
# MPCORB 10-year data table
from lsst.rsp import get_tap_service
import matplotlib.pyplot as plt
import pandas as pd

#################### Global ####################
OBJECT_TYPE_CUTOFFS = {
    "LPC": {"a_cutoff_min": 50},
    "Centaur": {"a_cutoff_min": 5.5, "a_cutoff": 30.1},
    "TNO": {"a_cutoff_min": 30.1, "a_cutoff": 50},
    "Ntrojan": {"a_cutoff_min": 29.8, "a_cutoff": 30.4},
    "NEO": {"q_cutoff": 1.3, "a_cutoff": 4.0, "e_cutoff": 1.0},
    "MBA": {"q_cutoff_min": 1.66, "a_cutoff_min": 2.0, "a_cutoff": 3.2},
    "Jtrojan": {"a_cutoff_min": 4.8, "a_cutoff": 5.4, "e_cutoff": 0.3},
}
################################################

##### Making query functions #####
def make_query_general(object_type = None, q_cutoff_min = None, q_cutoff = None, e_cutoff_min = None, e_cutoff = None, a_cutoff = None, a_cutoff_min = None, join = None):
    """
    Main query creation function. Returns query and object_type if relevant. 
    Args:
        object_type: String representing the type of object query looks for. 
        q_cutoff_min: Float representing the minimum distance at perihelion, in au.
        q_cutoff: Float representing the max distance at perihelion, in au. 
        e_cutoff_min: Float representing the minimum orbital eccentricity.
        e_cutoff: Float representing the max orbital eccentricity. 
        a_cutoff_min: Float representing the minimum semi-major axis of the orbit, in au.
        a_cutoff: Float representing the max semi-major axis of the orbit, in au.
        join: String representing which dataset to 'join' statement to MPCOrbit dataset. Defualt none. 
    Returns:
        query: String representing a valid query for an object type. 
        object_type: String representing the type of object query looks for. 
    """
        
    if object_type is None: # if no object type assigned, need to get the object type and use the cutoffs given 
        query = make_query(q_cutoff_min, q_cutoff, e_cutoff_min, e_cutoff, a_cutoff, a_cutoff_min, join)
        input_params = {
        "q_cutoff_min": q_cutoff_min, 
        "q_cutoff": q_cutoff, 
        "a_cutoff_min": a_cutoff_min, 
        "a_cutoff": a_cutoff, 
        "e_cutoff_min": e_cutoff_min, 
        "e_cutoff": e_cutoff}
        object_type = type_classification(input_params = input_params)
        return query, object_type

    elif object_type in OBJECT_TYPE_CUTOFFS: #if object type is a valid type, need to get the cutoffs for that object type 
        params = type_classification(object_type = object_type)  # returns dictionary of cutoff parameters
        query = make_query(**params, join=join)  # unpack all cutoffs
        return query, object_type
    else:
        raise ValueError('Please enter a valid object type.')

def make_query(q_cutoff_min = None, q_cutoff = None, e_cutoff_min = None, e_cutoff = None, a_cutoff = None, a_cutoff_min = None, join = None): 
    """
    Function creates a string query that can be passed to SSOtap. 
    Args:
        q_cutoff_min: Float representing the minimum distance at perihelion, in au.
        q_cutoff: Float representing the max distance at perihelion, in au. 
        e_cutoff_min: Float representing the minimum orbital eccentricity.
        e_cutoff: Float representing the max orbital eccentricity. 
        a_cutoff_min: Float representing the minimum semi-major axis of the orbit, in au.
        a_cutoff: Float representing the max semi-major axis of the orbit, in au.
        join: String representing which dataset to 'join' statement to MPCOrbit dataset. Defualt none. 
    Returns:
        query: String representing query that can be passed to SSOtap.
    """
    query_start = f"""SELECT mpc.incl, mpc.q, mpc.e, mpc.ssObjectID, dias.magTrueVband, dias.band FROM dp03_catalogs_10yr.MPCORB as mpc"""

    query = query_start

    if join is not None:
        if join == "Diasource":
            query += f"""
    INNER JOIN dp03_catalogs_10yr.DiaSource AS dias ON mpc.ssObjectId = dias.ssObjectId"""

    # WHERE clause
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
        conditions.append(f"mpc.q/(1-mpc.e) > {a_cutoff_min}")
    if a_cutoff is not None:
        conditions.append(f"mpc.q/(1-mpc.e) < {a_cutoff}")

    query += f"""
    WHERE"""
    query = query + " " + " AND ".join(conditions)
    query = query + ";"

    return query

def type_classification(object_type = None, input_params = None):
    """
    Function determines object type based on parameters or parameter based on object type. 
    This function's return objects depend on whether object_type is None:
    
        1. If object_type is NOT PROVIDED, the function returns object_type.
        2. If object_type is PROVIDED, the function returns orbital parameters (a, q, e) associated with that object type. 
        
    Args: (all optional)
        object_type (str): String representing object type. 
        input_params: Dictionary containing each parameter (key) with user-input floats (value).
    Returns:
        if object_type is NOT PROVIDED: 
            object_type (str): String representing the type of object query looks for.
        if object_type is PROVIDED:
            params (dictionary of floats): Dictionary of floats corresponding to parameters of the specific object type. 
    """
    if object_type is None:
        object_type = type_from_params(input_params = input_params)
        return object_type
    else:
        params = params_from_type(object_type)
        return params


def type_from_params(input_params):
    """
    Function returns object type based on input parameters.
    Args:
        input_params: Dictionary containing each parameter (key) with user-input floats (value).
    Returns:
        object_type (str): String representing the type of object query looks for. 
    """
    # need to check if input parameters match anything in the OBJECT_TYPE_CUTOFFS dictionary
    for obj_type, cutoff_dict in OBJECT_TYPE_CUTOFFS.items(): # each "value" is also a dictionary
        match = True
        for parameter, value in cutoff_dict.items(): # param = a_cutoff_min, value = 50
            current_param_check = input_params.get(parameter)
            if current_param_check is None: # checking if parameter has value in user inputs
                match = False
                break
                # now, need to check if input parameter matches criteria value
                # if min
            if parameter[-3:] == "min": #if parameter.endswith("min"):
                if current_param_check < value: # passes if >=
                    match = False
                    break
            else: # if not min
                if current_param_check > value: #passes if <=
                    match = False
                    break
            if match is True:
                return obj_type

def params_from_type(object_type):
    """
    Function returns parameters based on object type. 
    Args: 
        object_type (str): String representing object type. 
    Returns:
        params (dictionary of floats): Dictionary of floats corresponding to parameters of the specific object type. 
    """
    if object_type in OBJECT_TYPE_CUTOFFS:
        params = OBJECT_TYPE_CUTOFFS[object_type]
        return params
    else:
        raise ValueError("Invalid object_type.")

###########################

##### Running the query #####
def run_query(query_string, to_pandas = False):
    """
    Function runs SSOtap using query_string. Default returns data in the form of an AstroPy Table.
    Args:
        query_string: String representing query to pass to SSOtap.
        return_item: String representing the type of dataframe to return with queried data. 
        to_pandas: Boolean representing whether or not to convert job results to pandas table. Default is an AstroPy table.
    Returns: 
        unique_objects: Data table with the job results. 
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

##### Post-run data wrangling #####
def calc_semimajor_axis(q, e):
    """
    Given a perihelion distance and orbital eccentricity,
    calculate the semi-major axis of the orbit.
    Args: 
        q: ndarray
            Distance at perihelion, in au.
        e: ndarray
            Orbital eccentricity.

    Returns:
        a: ndarray
            Semi-major axis of the orbit, in au.
            q = a(1-e), so a = q/(1-e)
    """

    return q / (1.0 - e)

def plot_data(data_table):
    """
    Function that creates  a vs. e, a vs. i plots using the returned data table from the original query.
    Args:
        data_table: Astropy table from query. 
    """
    if "object_type" not in data_table.columns:
        raise KeyError("object_type not a column.")
    object_type = data_table['object_type'][0]
    
    # Orbital parameter plot (a vs e)
    fig, ax = plt.subplots()
    # plt.xlim([0., 4.])
    # plt.ylim([0., 1.])
    ax.set_xscale('log')
    ax.scatter(data_table["a"], data_table["e"], s=0.1) # a vs. e
    ax.set_xlabel('semimajor axis (au)')
    ax.set_ylabel('eccentricity')
    ax.set_title("a vs. e (" + object_type + ")")
    ax.minorticks_on()
    ax.grid()
    plt.show()

    # Orbital parameter plot (a vs i)
    fig, ax = plt.subplots()
    # plt.xlim([0., 4.])
    # plt.ylim([0., 1.])
    ax.set_xscale('log')
    ax.scatter(data_table["a"], data_table["incl"], s=0.1) # a vs. i
    ax.set_xlabel('semimajor axis (au)')
    ax.set_ylabel('inclination (deg)')
    ax.set_title("a vs. i (" + object_type + ")")
    ax.minorticks_on()
    ax.grid()
    plt.show()

def type_counts(data_table):
    """
    Function returns the number of counts per unique object_type. 
    Args:
        data_table: Table of data with 'object_type' parameter. Can be pandas table or query result table. 
    Returns:
        counts: Pandas series containing counts of each unique value in 'object_type'. 
    """
    if isinstance(x, pd.DataFrame): #checks if the data table passed to counts is pandas
        counts = data_table['object_type'].value_counts()
    else:
        df = data_table.to_pandas()
        counts = df['object_type'].value_counts()
    print(counts)
    return counts
    


# def type_classification(row): #no JFCs returned because it's the same criteria as the TNOs
#     """
#     Function takes one row in datatable, classifies row based on a, q, e parameters.
#     Args:
#         row: Row in pandas dataframe. 
#     """
#     if (2.0 < row['a'] < 3.2) and (row['q'] > 1.66):
#         return "MBA"
#     elif (row['q'] < 1.3) and (row['a'] < 4) and (row['e'] < 1):
#         return "NEO"
#     elif 30.1 < row['a'] < 50:
#         return "TNO"
#     elif 5.5 < row['a'] < 30.1:
#         return "Centaur"
#     elif row['a'] > 50:
#         return "LPC"
        

# next steps: Nora doing SSObject
# Joined with DiaSource -> every observation for each object -> SSObject ID link?
# How many observations for each object? In what filters?
# What is the average magnitude range? Does any object have an unusually large range?


    



