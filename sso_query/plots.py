import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np
import pandas as pd


def setup(df):
    if type(df) != pd.DataFrame:
        df = df.to_pandas()
    
    a_min, a_max = np.percentile(df['a'], [0.5, 99.5])
    e_min, e_max = np.percentile(df['e'], [0.5, 99.5])
    i_min, i_max = np.percentile(df['incl'], [0.5, 99.5])
    
    df_trimmed = df[(df['a'] >= a_min) & (df['a'] <= a_max) & (df['e'] >= e_min) & (df['e'] <= e_max) & (df['incl'] >= i_min) & (df['incl'] <= i_max)]
    
    return df_trimmed


def basic_plots(df, scatterplot_cutoff:int = 500, log_scale:bool = False):
    """
    Function that creates  a vs. e, a vs. i plots using the returned data table from the original query.
    Args:
        data_table (Pandas dataframe): Results from query. 
        scatterplot_cutoff (int) = 500: Number of points to create a heat map plot instead of a scatter plot. 
        log (boolean) = False: Boolean that can turn on x-axis log. Default off (False)
    """
    use_heatmap = len(df) > scatterplot_cutoff
    
    # Plot a vs. e
    if 'a' in df.columns and 'e' in df.columns:   
        plt.figure(figsize=(7, 5))
        if use_heatmap:
            norm = LogNorm() if log_scale else None
            plt.hist2d(df['a'], df['e'], bins=(200, 200), cmap='plasma', cmin=1, norm=norm)
            plt.colorbar(label='Number of objects (log scale)' if log_scale else 'Number of objects')
        else:
            for class_type in df["class_name"].unique():
                class_data = df[df["class_name"] == class_type]
                plt.scatter(class_data["a"], class_data["e"], s=0.1, alpha=0.5, label=class_type)
        plt.xlabel('Semi-major Axis (AU)')
        plt.ylabel('Eccentricity')
        plt.title('a vs. e')
        plt.tight_layout()
        plt.grid(True, ls="--", lw=0.5)
        plt.show()

    # Plot a vs. incl
    if 'a' in df.columns and 'incl' in df.columns:
        plt.figure(figsize=(7, 5))
        if use_heatmap:
            norm = LogNorm() if log_scale else None
            plt.hist2d(df['a'], df['incl'], bins=(200, 200), cmap='plasma', cmin=1, norm=norm)
            plt.colorbar(label='Number of objects (log scale)' if log_scale else 'Number of objects')
        else:
            for class_type in df["class_name"].unique():
                class_data = df[df["class_name"] == class_type]
                plt.scatter(class_data["a"], class_data["incl"], s=0.1, alpha=0.5, label=class_type)
        plt.xlabel('Semi-major Axis (AU)')
        plt.ylabel('Inclination (deg)')
        plt.title('a vs. i')
        plt.tight_layout()
        plt.grid(True, ls="--", lw=0.5)
        plt.show()

def run_basic_plots(df, scatterplot_cutoff:int = 500, log_scale:bool = False):
    df_trimmed = setup(df)
    return basic_plots(df_trimmed, scatterplot_cutoff=scatterplot_cutoff, log_scale=log_scale)


def ssobject_plots(df, discovery_cutoff:str = "2025-06-30"):
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

    # Plot new vs. known objects
    if 'discoverySubmissionDate' in df.columns and 'numObs' in df.columns:
        df['discoverySubmissionDate'] = pd.to_datetime(df['discoverySubmissionDate'], errors='coerce')
        discovery_cutoff = pd.Timestamp(discovery_cutoff)
        df['is_new'] = df['discoverySubmissionDate'] >= discovery_cutoff

        plt.style.use("seaborn-v0_8-colorblind")
        color_map = {True: "C1", False: "C0"}

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
        ax.set_ylabel("Number of Objects")
        ax.set_title("Observation Count Distribution: New vs. Known Objects")
        ax.legend()
        plt.tight_layout()
        plt.show()


def run_ssobject_plots(df, discovery_cutoff:str = "2025-06-30"):
    df_trimmed = setup(df)
    return ssobject_plots(df_trimmed, discovery_cutoff=discovery_cutoff)


def combine_tables(df1, df2):
    """
    Function vertically concatenates two dataframes. Useful for combining data tables of different types.
    Args:
        df1 (Pandas dataframe): First dataframe to concatenate. 
        df2 (Pandas dataframe): Second dataframe to concatenate. 
    Returns:
        vertical_concat (Pandas dataframe): Combine df1 and df2 dataframe. 
    """
    vertical_concat = pd.concat([df1, df2], axis=0, ignore_index=True)
    return vertical_concat


def type_counts(data_table):
    """
    Function returns the number of counts per unique class_name. 
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


def data_grouped_mags(df):
    """
    Function groups everything by class name, observations by unique object, gets min/max mags
    Args:
        df (Pandas Dataframe): Results data with columns 'class_name', 'ssObjectID'
    Returns:
        sorted_filt_lrg_ranges (Pandas df): Original dataframe grouped by class name and unique observation, added min/max/mean/range magnitude columns,
            filtered by 2 std deviation criterion in mag range, in a descending order according to mag range column.
    """
    
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
    large_criterion = np.mean(mag_range) + (np.std(mag_range)*1)
    print(f"Large range criterion:", large_criterion)
    filtered_large_ranges = grouped_obs_data[grouped_obs_data['mag_range'] > large_criterion]
    # print(filtered_large_ranges) # debugging
    # print(filtered_large_ranges.columns) #debugging
    
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
    Function plots magnitude ranges (V) for the first number of objects. 
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