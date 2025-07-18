from astropy.table import Table
from IPython.display import display
from lsst.rsp import get_tap_service
import matplotlib.pyplot as plt
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

def make_query(catalog, class_name = None, cutoffs = None, join = None):
    """
    Creates an MPCORB table query from the catalog based on either a class_name or cutoffs dict.
    Creates a query from MPCORB 10-year table using the specificed catalog and class name OR cutoffs. Can join the MPCORB table with DiaSource or SSObject.
    Args:
        catalog (str): Name of RSP catalog to query.
        class_name = None (str) (optional): Name of orbital class.
        cutoffs = None (dict) (optional): Dictionaryof  orbital constraints (keys, str) and desired/input values (values, floats). 
        join = None (str) (optional): Table to join with MPCORB table. 
            DiaSource, SSObject
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

    # Adding selected fields from join table #
    if join is not None:
        if catalog == "dp03_catalogs_10yr":
            service = get_tap_service("ssotap") # 'tap' for DP03
        elif catalog == "dp1":
            service = get_tap_service("tap") # 'tap' for DP1
        else:
            raise ValueError("Please enter a valid catalog.")

        assert service is not None
        
        # DiaSource join
        if join == "DiaSource":
            join_clause = f"""
    INNER JOIN {catalog}.DiaSource AS dias ON mpc.ssObjectId = dias.ssObjectId"""
            try:
                #sso_results = service.search(f"SELECT column_name FROM TAP_SCHEMA.columns WHERE table_name = '{catalog}.DiaSource'")
                sso_results = service.search(f"""SELECT "column_name" FROM TAP_SCHEMA.columns WHERE "table_name" = '{catalog}.DiaSource'""")
                sso_table = sso_results.to_table()
                sso_table.rename_column('"column_name"', "column_name")
                
                available_fields = sso_table["column_name"].tolist()                        
                desired_fields = ["dias.magTrueVband", "dias.band"]
                
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
                sso_results = service.search(f"""SELECT "column_name" FROM TAP_SCHEMA.columns WHERE "table_name" = '{catalog}.SSObject'""")
                sso_table = sso_results.to_table()
                sso_table.rename_column('"column_name"', "column_name")
                
                available_fields = sso_table["column_name"].tolist()            
                desired_fields = ["sso.g_H", "sso.r_H", "sso.i_H", "sso.discoverySubmissionDate", "sso.numObs"]

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
        raise ValueError("Result table is empty or None. Check input cutoffs.")


    # turning results into pandas table
    # adding 'a' and 'class_name' columns
    table = pd.DataFrame(result)
    a = calc_semimajor_axis(table['q'], table['e'])
    table['a'] = a
    table['class_name'] = class_name

    if to_pandas is False: #AstroPy table
        table = Table.from_pandas(table)
        print(table[0:5]) # print first few rows 
    else: #pandas table
        display(table) # show first five rows
    
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


def plots(df):

    if type(df) != pd.DataFrame:
        df = df.to_pandas()

    a_min, a_max = np.percentile(df['a'], [0.5, 99.5])
    e_min, e_max = np.percentile(df['e'], [0.5, 99.5])
    i_min, i_max = np.percentile(df['incl'], [0.5, 99.5])

    df_trimmed = df[(df['a'] >= a_min) & (df['a'] <= a_max) & (df['e'] >= e_min) & (df['e'] <= e_max) & (df['incl'] >= i_min) & (df['incl'] <= i_max)]

    # Plot a vs. e
    if 'a' in df.columns and 'e' in df.columns:
        plt.figure(figsize=(7, 5))
        plt.scatter(df_trimmed['a'], df_trimmed['e'], s=0.1, alpha=0.5)
        plt.xlabel('Semi-major Axis (AU)')
        plt.ylabel('Eccentricity')
        plt.title('a vs. e')
        plt.show()

    # Plot a vs. incl
    if 'a' in df.columns and 'incl' in df.columns:
        plt.figure(figsize=(7, 5))
        plt.scatter(df_trimmed['a'], df_trimmed['incl'], s=0.1, alpha=0.5)
        plt.xlabel('Semi-major Axis (AU)')
        plt.ylabel('Inclination')
        plt.title('a vs. i')
        plt.show()

    # Plot color
    if 'g_r_color' in df.columns and 'r_i_color' in df.columns:
        plt.figure(figsize=(7, 5))
        plt.scatter(df['g_r_color'], df['r_i_color'], s=1, alpha=0.5, c='steelblue')
        plt.xlabel("g‒r")
        plt.ylabel("r‒i")
        plt.title("g‒r vs. r‒i")
        plt.grid(True, ls="--", lw=0.5)
        plt.tight_layout()
        plt.show()


    if 'discoverySubmissionDate' in df.columns and 'numObs' in df.columns:
        df['discoverySubmissionDate'] = pd.to_datetime(df['discoverySubmissionDate'], errors='coerce')
        discovery_cutoff = pd.Timestamp("2020-01-01")
        df['is_new'] = df['discoverySubmissionDate'] >= discovery_cutoff

        plt.style.use("seaborn-v0_8-colorblind")
        color_map = {True: "C1", False: "C0"}

        # Plot a vs. e
        if 'a' in df.columns and 'e' in df.columns and 'incl' in df.columns:
            # Plot a vs. e
            fig, axs = plt.subplots(1, 2, figsize=(12, 5))
            for is_new, group in df.groupby("is_new"):
                axs[0].scatter(group["a"], group["e"], label="New" if is_new else "Known", alpha=0.6, s=15, c=color_map[is_new])
            axs[0].set_xlabel("Semi-Major Axis (a) [AU]")
            axs[0].set_ylabel("Eccentricity (e)")
            axs[0].set_title("Semi-Major Axis vs. Eccentricity")
            axs[0].legend()
            
            # Plot a vs. incl
            for is_new, group in df.groupby("is_new"):
                axs[1].scatter(group["a"], group["incl"], label="New" if is_new else "Known", alpha=0.6, s=15, c=color_map[is_new])
            axs[1].set_xlabel("Semi-Major Axis (a) [AU]")
            axs[1].set_ylabel("Inclination (i) [deg]")
            axs[1].set_title("Semi-Major Axis vs. Inclination")
            axs[1].legend()

            plt.suptitle("New vs. Known Objects")
            plt.tight_layout(rect=[0, 0, 1, 0.95])
            plt.show()
             

        # Number of Observations Histogram
        fig, ax = plt.subplots(figsize=(8, 6))
        for is_new, group in df.groupby("is_new"):
            ax.hist(group["numObs"], bins=30, alpha=0.7, label="New" if is_new else "Known", color=color_map[is_new])
        ax.set_xlabel("Number of Observations")
        ax.set_ylabel("Count")
        ax.set_title("Observation Count Distribution")
        ax.legend()
        plt.tight_layout()
        plt.show()


