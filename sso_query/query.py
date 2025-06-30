def classification(class_name):
    """
    Finds dynamical contraints of the orbital group given.
    
    Args:
        class_name: Name of an orbital group/class (str).
    Returns:
        cutoffs: Dictionary of dynamical constraints of the orbital group. 
    """
    valid_classes = ['lpcs', 'centaurs', 'tnos', 'neptunian trojans', 'jupiter trojans', 'mbas', 'neos']
    if class_name.lower() not in valid_classes:
        raise ValueError(f"Unknown orbital class: {class_name}")
    
    cutoffs = {'q_min': None, 'q_max': None, 'e_min': None, 'e_max': None, 'a_min': None, 'a_max': None}

    # LPCs: a >= 50.0
    if class_name.lower() == 'lpcs':
        cutoffs['a_min'] = 50.0

    # Centaurs: 5.5 < a < 30.1
    elif class_name.lower() == 'centaurs':
        cutoffs['a_min'] = 5.5
        cutoffs['a_max'] = 30.1

    # TNOs: 30.1 < a < 50
    elif class_name.lower() == 'tnos':
        cutoffs['a_min'] = 30.1
        cutoffs['a_max'] = 50.0

    # Neptunian Trojans: 29.8 < a < 30.4
    elif class_name.lower() == 'neptunian trojans':
        cutoffs['a_min'] = 29.8
        cutoffs['a_max'] = 30.4
    
    # Jupiter Trojans: e < 0.3, 4.8 < a < 5.4
    elif class_name.lower() == 'jupiter trojans':
        cutoffs['e_max'] = 0.3
        cutoffs['a_min'] = 4.8
        cutoffs['a_max'] = 5.4

    # MBAs: q > 1.66, 2.0 < a < 3.2
    elif class_name.lower() == 'mbas':
        cutoffs['q_min'] = 1.66
        cutoffs['a_min'] = 2.0
        cutoffs['a_max'] = 3.2

    # NEOs: q < 1.3, e < 1.0, a > 4.0
    elif class_name.lower() == 'neos':
        cutoffs['q_max'] = 1.3
        cutoffs['e_max'] = 1.0
        cutoffs['a_min'] = 4.0

    return cutoffs


def make_query(class_name, join_SSObject=False):
    """
    Creates a query based on the dynamical constraints of the orbital group.
    
    Args:
        class_name: Name of an orbital group/class (str).
        join_SSObject (bool): Whether to join MPCORB and SSObject catalogs for query.
    Returns:
        query_end: Query string for objects of the given orbital group.
    """
    table_ref = "dp03_catalogs_10yr.MPCORB as mpc"
    join_clause = ""
    select_fields = ["mpc.ssObjectId", "mpc.mpcDesignation", "mpc.e", "mpc.q", "mpc.incl"]
    
    if join_SSObject:
        join_clause = " INNER JOIN dp03_catalogs_10yr.SSObject as sso ON mpc.ssObjectId = sso.ssObjectId"
        select_fields += ["sso.g_H", "sso.r_H", "sso.i_H", "(sso.g_H - sso.r_H) AS g_r_color", "(sso.r_H - sso.i_H) AS r_i_color"]

    start_query = f"""SELECT {', '.join(select_fields)} FROM {table_ref}{join_clause} WHERE """
    cutoffs = classification(class_name)
    conditions = []
    
    if cutoffs['q_min'] is not None:
        conditions.append(f"mpc.q >= {cutoffs['q_min']}")
    if cutoffs['q_max'] is not None:
        conditions.append(f"mpc.q <= {cutoffs['q_max']}")
    if cutoffs['e_min'] is not None:
        conditions.append(f"mpc.e >= {cutoffs['e_min']}")
    if cutoffs['e_max'] is not None:
        conditions.append(f"mpc.e <= {cutoffs['e_max']}")
    if cutoffs['a_min'] is not None:
        conditions.append(f"mpc.q/(1.0-mpc.e) >= {cutoffs['a_min']}")
    if cutoffs['a_max'] is not None:
        conditions.append(f"mpc.q/(1.0-mpc.e) <= {cutoffs['a_max']}")
    
    where_clause = " AND ".join(conditions)
    query_end = f"{start_query}{where_clause} ORDER BY mpc.mpcDesignation"
    return query_end


from astropy.table import Table
from IPython.display import display
from lsst.rsp import get_tap_service
import matplotlib.pyplot as plt
import numpy as np

service = get_tap_service("ssotap")
assert service is not None

def run_query(class_name, join_SSObject=False, count_classes=False, show_table=False, show_plots=False, return_astropy=False, verbose=False):
    """
    Runs a TAP query on the ssotap service.

    Args:
        class_name: Name of an orbital group/class (str).
        join_SSObject (bool): Whether to join MPCORB and SSObject catalogs for query.
        count_classes (bool): Whether to print 
        show_table (bool): Whether to print the resulting table (default: False).
        show_plots (bool): Whether to generate basic diagnostic plots (default: False).
        return_astropy (bool): If True, returns an Astropy Table instead of a pandas DataFrame.
        verbose (bool): Whether to print statements that display information about the data in the catalog.
    Returns:
        Table or DataFrame: Query results as either an Astropy Table or pandas DataFrame.
    """
    query_string = make_query(class_name, join_SSObject=join_SSObject)
    if verbose:
        print(f"Running query:\n{query_string}\n")
    
    job = service.submit_job(query_string)
    job.run()
    job.wait(phases=['COMPLETED', 'ERROR'])
    
    if verbose:
        print(f"Job phase is: {job.phase}\n")
        assert job.phase == 'COMPLETED', "Query did not complete successfully."

    result_table = job.fetch_result().to_table()
    
    if 'q' in result_table.colnames and 'e' in result_table.colnames:
        a_values = result_table['q'] / (1.0 - result_table['e'])
        result_table['a'] = a_values
        if verbose:
            print("Added semi-major axis 'a' column to the table.\n")

    if verbose:
        print(f"Query returned {len(result_table)} rows.\n")
        print("Columns in the result table:")
        for col in result_table.colnames:
            print(f"  - {col} ({result_table[col].dtype})")
        print("\nFirst 5 rows:")
        print(result_table[:5])
        
    df = result_table.to_pandas()

    if count_classes:
        counts = {}
        print("\nClass count:")
        counts[class_name] = len(df)
        print(f"{class_name}: {counts[class_name]} objects\n")
        
        # class_list = ['LPCs', 'Centaurs', 'TNOs', 'Neptunian Trojans', 'Jupiter Trojans', 'MBAs', 'NEOs']
        # for class_name in class_list:
            # class_df = run_query(class_name, join_SSObject=join_SSObject, verbose=False)
            # counts[class_name] = len(class_df)
            # print(f"{class_name}: {counts[class_name]} objects")

    if show_table:
        display(df.head(50)) # Will nicely display the first 50 rows
        
    if show_plots:

        # Avoid extreme outliers
        df_plot = df[(df['a'] < 100) & (df['e'] < 1.0)]

        # Scatter plot: a vs e (zoomed)
        plt.figure(figsize=(7, 5))
        plt.scatter(df_plot['a'], df_plot['e'], s=6, alpha=0.5)
        plt.xlabel('a (AU)')
        plt.ylabel('e')
        plt.title('a vs e (zoomed)')
        plt.grid(True, ls="--", lw=0.5)
        plt.tight_layout()
        plt.show()

        # Scatter plot: a vs e (log scale)
        plt.figure(figsize=(7, 5))
        plt.scatter(df['a'], df['e'], s=6, alpha=0.5)
        plt.xscale('log')
        plt.xlabel('a (AU, log scale)')
        plt.ylabel('e')
        plt.title('a vs e (log scale)')
        plt.grid(True, which="both", ls="--", lw=0.5)
        plt.tight_layout()
        plt.show()

        # 2D Histogram: a vs e
        plt.figure(figsize=(7, 5))
        plt.hist2d(df_plot['a'], df_plot['e'], bins=(200, 200), cmap='plasma', cmin=1)
        plt.xlabel('a (AU)')
        plt.ylabel('e')
        plt.title('Density of a vs e')
        plt.colorbar(label='Number of objects')
        plt.tight_layout()
        plt.show()

        # Scatter plot: a vs inclination (zoomed)
        df_incl = df[df['a'] < 100]
        plt.figure(figsize=(7, 5))
        plt.scatter(df['a'], df['incl'], s=6, alpha=0.5)
        plt.xlabel('a (AU)')
        plt.ylabel('incl (deg)')
        plt.title('a vs inclination (zoomed)')
        plt.grid(True, ls="--", lw=0.5)
        plt.tight_layout()
        plt.show()
        
        # Scatter plot: a vs inclination (log scale)
        plt.figure(figsize=(7, 5))
        plt.scatter(df['a'], df['incl'], s=6, alpha=0.5)
        plt.xscale('log')
        plt.xlabel('a (AU, log scale)')
        plt.ylabel('incl')
        plt.title('a vs incl (log scale)')
        plt.grid(True, which="both", ls="--", lw=0.5)
        plt.tight_layout()
        plt.show()

        # 2D Histogram: a vs inclination
        plt.figure(figsize=(7, 5))
        plt.hist2d(df_plot['a'], df_plot['incl'], bins=(200, 200), cmap='plasma', cmin=1)
        plt.xlabel('a (AU)')
        plt.ylabel('incl')
        plt.title('Density of a vs incl')
        plt.colorbar(label='Number of objects')
        plt.tight_layout()
        plt.show()
        
        # Plot color if joined with SSObject
        if 'g_r_color' in df.columns and 'r_i_color' in df.columns:            
            plt.figure(figsize=(7, 5))
            plt.scatter(df['g_r_color'], df['r_i_color'], s=8, alpha=0.6, c='steelblue')
            plt.xlabel("g‒r")
            plt.ylabel("r‒i")
            plt.title("g‒r vs. r‒i")
            plt.grid(True, ls="--", lw=0.5)
            plt.tight_layout()
            plt.show()

    return result_table if return_astropy else df



# Possible idea: make this work for a list of classes 
"""
def classification(classes):
    ""
    Finds dynamical constraints for a list of orbital classes.

    Args:
        classes: List of class names (str).
    Returns:
        List of dicts, each representing the cutoffs for a class.
    ""
    valid_classes = ['lpcs', 'centaurs', 'tnos', 'neptunian trojans', 'jupiter trojans', 'mbas', 'neos']
    all_cutoffs = []

    for class_name in classes:
        name = class_name.lower()
        if name not in valid_classes:
            raise ValueError(f"Unknown orbital class: {class_name}")
        
        cutoffs = {'class': class_name, 'q_min': None, 'q_max': None, 'e_min': None, 'e_max': None, 'a_min': None, 'a_max': None}

        if name == 'lpcs':
            cutoffs['a_min'] = 50.0
        elif name == 'centaurs':
            cutoffs['a_min'] = 5.5
            cutoffs['a_max'] = 30.1
        elif name == 'tnos':
            cutoffs['a_min'] = 30.1
            cutoffs['a_max'] = 50.0
        elif name == 'neptunian trojans':
            cutoffs['a_min'] = 29.8
            cutoffs['a_max'] = 30.4
        elif name == 'jupiter trojans':
            cutoffs['e_max'] = 0.3
            cutoffs['a_min'] = 4.8
            cutoffs['a_max'] = 5.4
        elif name == 'mbas':
            cutoffs['q_min'] = 1.66
            cutoffs['a_min'] = 2.0
            cutoffs['a_max'] = 3.2
        elif name == 'neos':
            cutoffs['q_max'] = 1.3
            cutoffs['e_max'] = 1.0
            cutoffs['a_min'] = 4.0
        
        all_cutoffs.append(cutoffs)

    return all_cutoffs


def make_query(classes, join_SSObject=False):
    ""
    Creates a query to get objects matching any of the given classes.

    Args:
        classes: List of orbital class names.
        join_SSObject (bool): Whether to join with SSObject catalog.
    Returns:
        SQL query string.
    ""
    table_ref = "dp03_catalogs_10yr.MPCORB as mpc"
    join_clause = ""
    select_fields = ["mpc.ssObjectId", "mpc.mpcDesignation", "mpc.e", "mpc.q", "mpc.incl"]
    
    if join_SSObject:
        join_clause = " INNER JOIN dp03_catalogs_10yr.SSObject as sso ON mpc.ssObjectId = sso.ssObjectId"
        select_fields += [
            "sso.g_H", "sso.r_H", "sso.i_H",
            "(sso.g_H - sso.r_H) AS g_r_color",
            "(sso.r_H - sso.i_H) AS r_i_color"
        ]

    start_query = f"SELECT {', '.join(select_fields)} FROM {table_ref}{join_clause} WHERE "
    class_cutoffs = classification(classes)

    or_conditions = []
    for cut in class_cutoffs:
        conds = []
        if cut['q_min'] is not None:
            conds.append(f"mpc.q >= {cut['q_min']}")
        if cut['q_max'] is not None:
            conds.append(f"mpc.q <= {cut['q_max']}")
        if cut['e_min'] is not None:
            conds.append(f"mpc.e >= {cut['e_min']}")
        if cut['e_max'] is not None:
            conds.append(f"mpc.e <= {cut['e_max']}")
        if cut['a_min'] is not None:
            conds.append(f"mpc.q / (1.0 - mpc.e) >= {cut['a_min']}")
        if cut['a_max'] is not None:
            conds.append(f"mpc.q / (1.0 - mpc.e) <= {cut['a_max']}")
        if conds:
            or_conditions.append("(" + " AND ".join(conds) + ")")

    where_clause = " OR ".join(or_conditions)
    query_end = f"{start_query}{where_clause} ORDER BY mpc.mpcDesignation"
    return query_end

from astropy.table import Table
from lsst.rsp import get_tap_service
import matplotlib.pyplot as plt

service = get_tap_service("ssotap")
assert service is not None

def run_query(query_string, count_classes=False, show_table=False, show_plots=False, return_astropy=False, verbose=False):
    ""
    Runs a TAP query on the ssotap service.

    Args:
        query_string: The ADQL query string to run.
        count_classes (bool): Whether to print 
        show_table (bool): Whether to print the resulting table (default: False).
        show_plots (bool): Whether to generate basic diagnostic plots (default: False).
        return_astropy (bool): If True, returns an Astropy Table instead of a pandas DataFrame.
        verbose (bool): Whether to print statements that display information about the data in the catalog.
    Returns:
        Table or DataFrame: Query results as either an Astropy Table or pandas DataFrame.
    ""
    if verbose:
        print(f"Running query:\n{query_string}\n")
    
    job = service.submit_job(query_string)
    job.run()
    job.wait(phases=['COMPLETED', 'ERROR'])

    print(f"Job phase is: {job.phase}\n")
    assert job.phase == 'COMPLETED', "Query did not complete successfully."

    result_table = job.fetch_result().to_table()
    
    if 'q' in result_table.colnames and 'e' in result_table.colnames:
        a_values = result_table['q'] / (1.0 - result_table['e'])
        result_table['a'] = a_values
        if verbose:
            print("Added semi-major axis 'a' column to the table.\n")

    if verbose:
        print(f"Query returned {len(result_table)} rows.\n")
        print("Columns in the result table:")
        for col in result_table.colnames:
            print(f"  - {col} ({result_table[col].dtype})")
        print("\nFirst 5 rows:")
        print(result_table[:5])
        
    df = result_table.to_pandas()

    if count_classes:
        class_defs = classification(classes)
        df['a'] = df['q'] / (1.0 - df['e'])

        counts = {}
        for cut in class_defs:
            name = cut['class']
            mask = pd.Series(True, index=df.index)
            if cut['q_min'] is not None:
                mask &= df['q'] >= cut['q_min']
            if cut['q_max'] is not None:
                mask &= df['q'] <= cut['q_max']
            if cut['e_min'] is not None:
                mask &= df['e'] >= cut['e_min']
            if cut['e_max'] is not None:
                mask &= df['e'] <= cut['e_max']
            if cut['a_min'] is not None:
                mask &= df['a'] >= cut['a_min']
            if cut['a_max'] is not None:
                mask &= df['a'] <= cut['a_max']
            counts[name] = mask.sum()
            print(f"{name}: {counts[name]} objects")

    if show_table:
        print(result_table)

    if show_plots:

        # Plot a vs. e
        plt.figure(figsize=(6, 4))
        plt.scatter(df['a'], df['e'], s=10, alpha=0.6)
        plt.xlabel('a (AU)')
        plt.ylabel('e')
        plt.title('a vs e')
        plt.grid(True)
        plt.show()

        # Plot a vs. i
        plt.figure(figsize=(6, 4))
        plt.scatter(df['a'], df['incl'], s=10, alpha=0.6)
        plt.xlabel('a (AU)')
        plt.ylabel('i (deg)')
        plt.title('a vs i')
        plt.grid(True)
        plt.show()

        # Plot color if joined with SSObject
        if 'g_r_color' in df.columns and 'r_i_color' in df.columns:            
            plt.figure(figsize=(8, 6))
            plt.scatter(df['g_r_color'], df['r_i_color'], s=10, alpha=0.7, c='steelblue')
            plt.xlabel("g‒r")
            plt.ylabel("r‒i")
            plt.title("g-r vs. r-i")
            plt.grid(True)
            plt.tight_layout()
            plt.show()

    return result_table if return_astropy else df

"""