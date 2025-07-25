from astropy.time import Time
import itertools
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np
import pandas as pd
import seaborn as sns


def setup(df):
    if type(df) != pd.DataFrame:
        df = df.to_pandas()
    
    a_min, a_max = np.percentile(df['a'], [0.5, 99.5])
    e_min, e_max = np.percentile(df['e'], [0.5, 99.5])
    i_min, i_max = np.percentile(df['incl'], [0.5, 99.5])
    
    df_trimmed = df[(df['a'] >= a_min) & (df['a'] <= a_max) & (df['e'] >= e_min) & (df['e'] <= e_max) & (df['incl'] >= i_min) & (df['incl'] <= i_max)]
    
    return df_trimmed


def scatter_plots(df):
    """
    Function that creates  a vs. e, a vs. i scatter plots using the returned data table from the original query -- can handle objects from multiple classes.
    Args:
        df (Pandas dataframe): Results from query. 
    """
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))
    palette = sns.color_palette("colorblind")
    color_cycle = {cls: palette[i] for i, cls in enumerate(sorted(df['class_name'].dropna().unique()))}

    # Plot a vs. e
    if 'a' in df.columns and 'e' in df.columns:
        valid_ae = df[['a', 'e']].dropna()
        if valid_ae.empty:
            print("No valid data for a vs. e plot — all values are NaN.")
        else:
            if (len(df) - len(valid_ae)) > 0:
                print(f"Plotting orbital data ({len(valid_ae)} valid values, {len(df) - len(valid_ae)} NaNs skipped).")
        for class_type in df["class_name"].dropna().unique():
            class_data = df[(df["class_name"] == class_type) & df["a"].notna() & df["e"].notna()]
            axs[0].scatter(class_data["a"], class_data["e"], s=1, alpha=0.5, label=class_type, color=color_cycle[class_type])
        axs[0].set_xlabel('Semi-major Axis (AU)')
        axs[0].set_ylabel('Eccentricity')
        axs[0].set_title('a vs. e')
        axs[0].grid(True, ls="--", lw=0.5)
        axs[0].legend(title="Object Class", markerscale=10, fontsize="small", loc="best")

    # Plot a vs. incl
    if 'a' in df.columns and 'incl' in df.columns:
        valid_ai = df[['a', 'incl']].dropna()
        if valid_ai.empty:
            print("No valid data for a vs. incl plot — all values are NaN.")
        else:
            if (len(df) - len(valid_ai)) > 0:
                print(f"Plotting orbital data ({len(valid_ai)} valid values, {len(df) - len(valid_ai)} NaNs skipped).")
        for class_type in df["class_name"].dropna().unique():
            class_data = df[(df["class_name"] == class_type) & df["a"].notna() & df["incl"].notna()]
            axs[1].scatter(class_data["a"], class_data["incl"], s=1, alpha=0.5, label=class_type, color=color_cycle[class_type])
        axs[1].set_xlabel('Semi-major Axis (AU)')
        axs[1].set_ylabel('Inclination (deg)')
        axs[1].set_title('a vs. i')
        axs[1].grid(True, ls="--", lw=0.5)
        axs[1].legend(title="Object Class", markerscale=10, fontsize="small", loc="best")

    plt.suptitle("Dynamical Constraints Scatter Plots")
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

def run_scatter_plots(df):
    df_trimmed = setup(df)
    return scatter_plots(df_trimmed)


def heat_maps(df, log_scale:bool = False, bins:int = 200):
    """
    Function that creates a vs. e, a vs. i heat map plots using the returned data table from the original query -- meant for objects of one class.
    Args:
        df (Pandas DataFrame): Results from query.
        log_scale (bool): If True, apply log scale to colorbar (not axes). Default is False.
        bins (int): Number of bins along each axis. Default is 200.
    """
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))
    norm = LogNorm() if log_scale else None
    
    if 'a' in df.columns and 'e' in df.columns and 'incl' in df.columns:
        valid = df[['a', 'e', 'incl']].dropna()
        if valid.empty:
            print("No valid orbital data — all values are NaN.")
        else:
            if (len(df) - len(valid)) > 0:
                print(f"Plotting orbital data ({len(valid)} valid values, {len(df) - len(valid)} NaNs skipped).")
            
        # Plot a vs. e
        h1 = axs[0].hist2d(valid['a'], valid['e'], bins=bins, cmap='plasma', cmin=1, norm=norm)
        fig.colorbar(h1[3], ax=axs[0], label='Number of objects (log scale)' if log_scale else 'Number of objects')
        axs[0].set_xlabel('Semi-major Axis (AU)')
        axs[0].set_ylabel('Eccentricity')
        axs[0].set_title('a vs. e')
        axs[0].grid(True, ls="--", lw=0.5)
        
        # Plot a vs. incl
        h2 = axs[1].hist2d(valid['a'], valid['incl'], bins=bins, cmap='plasma', cmin=1, norm=norm)
        fig.colorbar(h2[3], ax=axs[1], label='Number of objects (log scale)' if log_scale else 'Number of objects')
        axs[1].set_xlabel('Semi-major Axis (AU)')
        axs[1].set_ylabel('Inclination (deg)')
        axs[1].set_title('a vs. i')
        axs[1].grid(True, ls="--", lw=0.5)
    
    plt.suptitle("Dynamical Constraints Heat Maps")
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()
             

def run_heat_maps(df, log_scale:bool = False, bins:int = 200):
    df_trimmed = setup(df)
    return heat_maps(df_trimmed, log_scale=log_scale, bins=bins)
        

def color_plot(df):
    """
    Function that creates f-r vs. r-i color plot if data is available from original query.
    Args:
        df (Pandas DataFrame): Results from query.
    """
    palette = sns.color_palette("colorblind")
    color_cycle = itertools.cycle(palette)

    # Plot color
    if 'g_r_color' in df.columns and 'r_i_color' in df.columns:
        valid_color = df[['g_r_color', 'r_i_color']].dropna()
        if valid_color.empty:
            print("No valid data for g‒r vs. r‒i plot — all values are NaN.")
        else:
            if (len(df) - len(valid_color)) > 0:
                print(f"Plotting color distributions ({len(valid_color)} valid values, {len(df) - len(valid_color)} NaNs skipped).")
        
        plt.figure(figsize=(7, 5))
        for class_type in df["class_name"].unique():
            class_data = df[(df["class_name"] == class_type) & df["g_r_color"].notna() & df["r_i_color"].notna()]
            plt.scatter(class_data['g_r_color'], class_data['r_i_color'], s=1, alpha=0.5, label=class_type, color=next(color_cycle))
        plt.xlim(-5, 5)
        plt.ylim(-5, 5)
        plt.xlabel("g‒r")
        plt.ylabel("r‒i")
        plt.title("g‒r vs. r‒i")
        plt.grid(True, ls="--", lw=0.5)
        plt.legend(title="Object Class", markerscale=10, fontsize="small", loc="best")
        plt.tight_layout()
        plt.show()
    else:
        print("Columns do not exist in this table.")

def run_color_plot(df):
    df_trimmed = setup(df)
    return color_plot(df_trimmed)

    
def ssobject_plots(df):
    """
    Function that plots new vs. known objects if data is available from original query.
    Args:
        df (Pandas DataFrame): Results from query.
    """
    palette = sns.color_palette("colorblind")
    color_cycle = itertools.cycle(palette)

    # Plot new vs. known objects
    if 'discoverySubmissionDate' in df.columns and 'numObs' in df.columns:
        valid_time = df[['discoverySubmissionDate', 'numObs']].dropna()
        if valid_time.empty:
            print("No valid timing data for new vs. known plots — all values are NaN.")
        else:
            if (len(df) - len(valid_time)) > 0:
                print(f"Plotting new vs. known data ({len(valid_time)} valid values, {len(df) - len(valid_time)} NaNs skipped.")
                
        df = df.copy()
        df['is_new'] = df['discoverySubmissionDate'].notna()

        color_map = {True: palette[0], False: palette[1],}  # Known: blue, New: orange
        edge_color = {True: 'black', False: 'white',} 
        
        if 'a' in df.columns and 'e' in df.columns and 'incl' in df.columns:
            
            for class_name, class_df in df.groupby('class_name'):
                valid_class = class_df[['a', 'e', 'incl']].dropna()
                if valid_class.empty:
                    print(f"No valid orbital data for class '{class_name}' — skipping plot.")
                    continue
                elif (len(df) - len(valid_class)) > 0:
                    print(f"Plotting orbital data for class '{class_name}' ({len(valid_class)} valid values, {len(class_df) - len(valid_class)} NaNs skipped).")
            
                fig, axs = plt.subplots(1, 2, figsize=(12, 5))
            
                # Plot a vs. e
                for is_new, group in class_df.groupby("is_new"):
                    valid_group = group[['a', 'e']].dropna()
                    if not valid_group.empty:
                        axs[0].scatter(valid_group["a"], valid_group["e"], label="New" if is_new else "Known", alpha=0.5, s=5, color=color_map[is_new], marker='o', edgecolor=edge_color[is_new], linewidth=0.2)
                axs[0].set_xlabel("Semi-Major Axis (a) [AU]")
                axs[0].set_ylabel("Eccentricity (e)")
                axs[0].set_title(f"Semi-Major Axis vs. Eccentricity")
                axs[0].legend(title="Status", markerscale=2, fontsize="small", loc="best")
                
                # Plot a vs. incl
                for is_new, group in class_df.groupby("is_new"):
                    valid_group = group[['a', 'incl']].dropna()
                    if not valid_group.empty:
                        axs[1].scatter(valid_group["a"], valid_group["incl"], label="New" if is_new else "Known", alpha=0.5, s=5, color=color_map[is_new], marker='o', edgecolor=edge_color[is_new], linewidth=0.2)
                axs[1].set_xlabel("Semi-Major Axis (a) [AU]")
                axs[1].set_ylabel("Inclination (i) [deg]")
                axs[1].set_title("Semi-Major Axis vs. Inclination")
                axs[1].legend(title="Status", markerscale=2, fontsize="small", loc="best")
    
                plt.suptitle(f"New vs. Known Objects for {class_name}")
                plt.tight_layout(rect=[0, 0, 1, 0.95])
                plt.show()
                 
                # Number of Observations Histogram
                fig, ax = plt.subplots(figsize=(8, 6))
                for is_new, group in class_df.groupby("is_new"):
                    valid_group = group[['numObs']].dropna()
                    if not valid_group.empty:
                        ax.hist(group["numObs"], bins=20, alpha=0.5, label="New" if is_new else "Known", color=color_map[is_new], histtype='stepfilled', edgecolor='black')
                ax.set_xlabel("Number of Observations")
                ax.set_ylabel("Number of Objects")
                ax.set_title(f"Observation Count Distribution: New vs. Known Objects for {class_name}")
                ax.legend(title="Status", markerscale=2, fontsize="small", loc="best")
                plt.tight_layout()
                plt.show()
    else:
        print("Columns do not exist in this table.")


def run_ssobject_plots(df):
    df_trimmed = setup(df)
    return ssobject_plots(df_trimmed)


def combine_tables(*dfs: pd.DataFrame) -> pd.DataFrame:
    """
    Vertically concatenates multiple pandas DataFrames. Useful for combining data tables of different types.

    Args:
        *dfs (pd.DataFrame): Any number of dataframes to concatenate.

    Returns:
        pd.DataFrame: Combined dataframe. 
    """
    converted = []
    for df in dfs:
        if isinstance(df, pd.DataFrame):
            converted.append(df)
        else:
            converted.append(df.to_table().to_pandas())
    vertical_concat = pd.concat(converted, axis=0, ignore_index=True)
    return vertical_concat



def obs_type_counts(data_table):
    """
    Function returns the number of observations per class type. 
    Args:
        data_table: Table of data with 'class_name' parameter. Can be pandas table or Astropy table. 
    Returns:
        counts: Pandas series containing counts of each unique value in 'class_name'. 
    """
    if isinstance(data_table, pd.DataFrame): #checks if the data table passed to counts is pandas
        counts = data_table['class_name'].value_counts()
        
    else:
        df = data_table.to_pandas()
        counts = df['class_name'].value_counts()
    print(counts)
    return counts

def obs_unique_obj_counts(data_table):
    """
    Function returns the number of observations per unique object.
    Args:
        data_table: Table of data with 'ssObjectID' and 'class_name' parameters. Can be pandas table or Astropy table. 
    Returns:
        counts: Pandas series containing counts of each unique value in 'ssObjectID'.  
    """
    if isinstance(data_table, pd.DataFrame):
        counts = data_table.groupby('ssObjectID')["class_name"].value_counts().reset_index(name="obs_count")
    else:
        df = data_table.to_pandas()
        counts = df.groupby('ssObjectID')["class_name"].value_counts().reset_index(name="obs_count")
    print(counts)
    return counts

def type_counts(data_table):
    """
    Function returns number of unique objects per class type.
    Args:
        data_table: Pandas Dataframe containing all dp1 data. 
    Returns:
        counts: Dictionary containing object count per class type. 
    """
    if isinstance(data_table, pd.DataFrame):
        counts = data_table.groupby("class_name")["ssObjectID"].nunique().reset_index(name="object_count")
    else:
        df = data_table.to_pandas()
        counts = df.groupby("class_name")["ssObjectID"].nunique().reset_index(name="object_count")
    print(counts)
    return counts

def data_grouped_mags(df):
    """
    Function groups everything by class name, observations by unique object, gets min/max mags
    Args:
        df (Pandas Dataframe): Results data with columns 'class_name', 'ssObjectID'
    Returns:
        sorted_filt_lrg_ranges (Pandas df): Original dataframe grouped by class name and unique observation, added min/max/mean/range magnitude columns,
            filtered by 2 std deviation criterion in mag range, in a descending order according to mag range column.
    """
    if not isinstance(df, pd.DataFrame):
        df = df.to_pandas()

    if df is None or df.empty:
        print("No values found.")
        return pd.DataFrame()
    
    # Check that class_name and ssObjectID are actual columns
    if "class_name" not in df.columns:
        raise KeyError("class_name is not a column.")
    if "ssObjectID" not in df.columns:
        raise KeyError("ssObjectID is not a column.")
    
    # 1. Group observations by class name, by ssObjectID, get the min/max/mean magnitudes
    grouped_obs_data = df.groupby(['class_name', 'ssObjectID']).agg(
        mag_min = ('magTrueVband', 'min'), 
        mag_max = ('magTrueVband', 'max'), 
        mag_mean = ('magTrueVband', 'mean')
    )
    grouped_obs_data = grouped_obs_data.reset_index() # groupby turns 'class_name' and 'ssObjectID' into indeces, this turns them back into columns
    # print(grouped_obs_data) # degbugging
    
    # 2. Create ranges column from min/max magnitudes, get standard deviation of ranges. 
    # want to look at when the range has a larger spread than normal, so want to get the std. deviation of the range
    mag_range = grouped_obs_data["mag_max"] - grouped_obs_data["mag_min"]
    # print(mag_range) # debugging
    grouped_obs_data['mag_range'] = mag_range
    print("Standard Deviation of Range:", np.std(mag_range))
    print("Mean Range:", np.mean(mag_range))
    
    # 3. Need to check which ranges are above change criterion. Using mean and std. deviation by object_type. 
    large_criterion = np.mean(mag_range) + (np.std(mag_range) * 1)
    print(f"Large range criterion:", large_criterion)
    
    filtered_large_ranges = grouped_obs_data[grouped_obs_data['mag_range'] > large_criterion]
    
    # Check if filtering removed all or too many rows
    if filtered_large_ranges.empty or len(filtered_large_ranges) > len(grouped_obs_data):
        print("Large range criterion removed all or too many objects — skipping filter.")
        filtered_large_ranges = grouped_obs_data.copy()
    
    # 4. Rearranging dataframe so magnitude ranges are in descending order (largest at the top).
    sorted_filt_lrg_ranges = filtered_large_ranges.sort_values(by='mag_range', ascending=False)
    # print(sorted_filt_lrg_ranges) # debugging
    
    return sorted_filt_lrg_ranges


def obs_filter(df):
    """
    Function returns pandas data frame with data grouped by observations and filter.
    Args:
        df (Pandas dataframe): Dataframe with 'ssObjectID' and 'band' columns. 
    Returns:
        observations_by_object_filter: Dataframe containing counts of all observations by unique ssO_id and filter.
    """
    if df.get('band') is None:
        raise KeyError("No 'band' column. Check that query joined with DiaSource.")
    if df.get('ssObjectID') is None:
        raise KeyError("No 'ssObjectID' column. Check query fields.")

    # need to count observations for each unique object in SSO_id
    observations_by_object = df['ssObjectID'].value_counts()
    
    # unique observations within each filter
    observations_by_filter = df['band'].value_counts()
    
    # count of unique observations for each unique object in SSO_id within each filter
    observations_by_object_filter = df.groupby(['ssObjectID', 'band']).size().reset_index(name='obs_filter_count')

    # print statements
    print(f"# of observations by Object:", observations_by_object)
    print(f"# of observations by Filter:", observations_by_filter)
    print(f"# of unique observations for each unique object, by filter:", observations_by_object_filter)
    
    return observations_by_object_filter

   
def mag_range_plot(data_table, head_number = 5):
    """
    Function plots magnitude ranges for the specified number of objects.
        1. If head_number is None, all objects plotted. 
    Args:
        data_table: Pandas dataframe with values to plot.
        number: Int representing the number of objects to plot. 
    """
    class_name = data_table['class_name'].iloc[0]
    color_map = {
    "NEO": "red",
    "TNO": "blue",
    "Centaur": "green",
    "MBA": "orange",
    "Jtrojan": "purple",
    "LPC": "brown",
    "Ntrojan": "pink"
    }
    color = color_map.get(class_name, "gray")  # fallback to 'gray' if type unknown
    
    sorted_filt_lrg_ranges = data_table.sort_values(by='mag_range', ascending=False)


    #
    if head_number is not None: # only filtering for the top number of values if number provided
        top_srtd_filt_lrg_ranges = sorted_filt_lrg_ranges.iloc[:head_number,:]
        plot_title = "Top " + str(head_number) + " Magnitude Ranges"
    else:
        top_srtd_filt_lrg_ranges = data_table
        plot_title = "Magnitude Ranges"
    
    top_ranges = top_srtd_filt_lrg_ranges.copy()
    top_ranges['y_spacing'] = range(1, len(top_ranges) + 1) 
    # print(top_ranges) #degbugging
    
    # For the largest objects, want to visualize their ranges
    fig, ax = plt.subplots()
    ax.hlines(data = top_ranges, y = 'y_spacing', xmin = 'mag_min', xmax = 'mag_max', color = color, linewidth = 2, zorder = 2, label = class_name)
    
    # adding reference line
    x_center = (top_ranges['mag_min'].min() + top_ranges['mag_max'].max()) / 2
    xmin_ref = x_center - (np.mean(sorted_filt_lrg_ranges['mag_range']/2))
    xmax_ref = x_center + (np.mean(sorted_filt_lrg_ranges['mag_range']/2))
    ax.hlines(y = 0, xmin = xmin_ref, xmax = xmax_ref, color = "blue", linewidth = 2, label = "Mean Range")
    sc = ax.scatter(data = top_ranges, x = 'mag_mean', y = 'y_spacing', s = 40, marker='o', edgecolors = "black", linewidth = 0.5, c='mag_mean', cmap = 'PiYG', zorder = 3, label = None)
    cbar = fig.colorbar(sc, ax=ax)
    cbar.set_label('Mean Magnitude (V)')
    ax.set_xlabel('Magnitude Range (V)')
    ax.set_ylabel('ssObject ID')
    ax.set_title(plot_title)
    ax.set_yticks(top_ranges['y_spacing'])
    ax.set_yticklabels(top_ranges['ssObjectID'])
    ax.minorticks_on()
    ax.grid(zorder = 1)
    plt.legend(loc="lower left")
    plt.show()