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
    use_heatmap = len(df) > scatterplot_cutoff
    
    # Plot a vs. e
    if 'a' in df.columns and 'e' in df.columns:   
        plt.figure(figsize=(7, 5))
        if use_heatmap:
            norm = LogNorm() if log_scale else None
            plt.hist2d(df['a'], df['e'], bins=(200, 200), cmap='plasma', cmin=1, norm=norm)
            plt.colorbar(label='Number of objects (log scale)' if log_scale else 'Number of objects')
        else:
            plt.scatter(df['a'], df['e'], s=0.1, alpha=0.5)
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
            plt.scatter(df['a'], df['incl'], s=0.1, alpha=0.5)
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
        df = df.copy()
        df['discoverySubmissionDate'] = pd.to_datetime(df['discoverySubmissionDate'], errors='coerce')
        discovery_cutoff = pd.Timestamp(discovery_cutoff)
        df['is_new'] = df['discoverySubmissionDate'] >= discovery_cutoff

        plt.style.use("seaborn-v0_8-colorblind")
        color_map = {True: "C1", False: "C0"}

        if 'a' in df.columns and 'e' in df.columns and 'incl' in df.columns:
            
            # Plot a vs. e
            fig, axs = plt.subplots(1, 2, figsize=(12, 5))
            for is_new, group in df.groupby("is_new"):
                if not group.empty:
                    axs[0].scatter(group["a"], group["e"], label="New" if is_new else "Known", alpha=0.6, s=15, c=color_map[is_new])
            axs[0].set_xlabel("Semi-Major Axis (a) [AU]")
            axs[0].set_ylabel("Eccentricity (e)")
            axs[0].set_title("Semi-Major Axis vs. Eccentricity")
            axs[0].legend()
            
            # Plot a vs. incl
            for is_new, group in df.groupby("is_new"):
                if not group.empty:
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

