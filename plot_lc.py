import pandas as pd
import matplotlib.pyplot as plt
import extinction_utils

######function to plot different filters
def plot_photometry(df, title='Light Curve', output_file='lightcurve.png'):
    """
    Plots photometry light curves from a DataFrame.

    Parameters:
        df (pd.DataFrame): DataFrame with columns: 'mjd', 'mag', 'magerr', 'filter'
        title (str): Title of the plot
        output_file (str): File name to save the plot
    """
    df = df.dropna(subset=["mag"])

    plt.figure(figsize=(10, 6))
    plt.gca().invert_yaxis()

    for flt in df['filter'].unique():
        flt_data = df[df['filter'] == flt]
        plt.errorbar(flt_data['mjd'], flt_data['mag'], yerr=flt_data['magerr'],
                     fmt='o', label=flt, capsize=2)

    plt.xlabel('MJD')
    plt.ylabel('Magnitude')
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_file)
    plt.show()

#####function to differentiate telescopes


def plot_photometry_inst(df, title='Light Curve', output_file='lightcurve.png'):
    """
    Plots photometry light curves from a DataFrame with different markers for each instrument.

    Parameters:
        df (pd.DataFrame): DataFrame with columns: 'mjd', 'mag', 'magerr', 'filter', 'inst'
        title (str): Title of the plot
        output_file (str): File name to save the plot
    """
    df = df.dropna(subset=["mag"])

    # Define marker styles and colors for different instruments
    inst_styles = {
        'martini': {'marker': 'D', 'color': 'red', 'label': 'Martini'},
        'aavso': {'marker': 's', 'color': 'green', 'label': 'AAVSO'},
        'goranskij': {'marker': 'o', 'color': 'blue', 'label': 'Goranskij'}
    }

    plt.figure(figsize=(10, 6))
    plt.gca().invert_yaxis()

    # Loop through instruments and plot each one with a different style
    for inst, style in inst_styles.items():
        inst_data = df[df['inst'] == inst]
        plt.errorbar(inst_data['mjd'], inst_data['mag'], yerr=inst_data['magerr'],
                     fmt=style['marker'], color=style['color'], label=style['label'], capsize=2)

    plt.xlabel('MJD')
    plt.ylabel('Magnitude')
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_file)
    plt.show()


def plot_photometry_dereddened(df, title='', output_file=None):
    import matplotlib.pyplot as plt

    plt.figure(figsize=(10, 6))
    for band in sorted(df['filter'].unique()):
        band_df = df[df['filter'] == band]
        plt.errorbar(band_df['mjd'], band_df['app_mag'], yerr=band_df['magerr'],
                     fmt='o', label=f'{band}', alpha=0.8)

    plt.gca().invert_yaxis()
    plt.xlabel("MJD")
    plt.ylabel("De-reddened App-Mag")
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    if output_file:
        plt.savefig(output_file)
    plt.close()
    
def plot_photometry_dereddened_abs(df, title='', output_file=None):
    import matplotlib.pyplot as plt

    plt.figure(figsize=(10, 6))
    for band in sorted(df['filter'].unique()):
        band_df = df[df['filter'] == band]
        plt.errorbar(band_df['mjd'], band_df['abs_mag'], yerr=band_df['magerr'],
                     fmt='o', label=f'{band}', alpha=0.8)

    plt.gca().invert_yaxis()
    plt.xlabel("MJD")
    plt.ylabel("De-reddened App-Mag")
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    if output_file:
        plt.savefig(output_file)
    plt.close()


def plot_photometry_dereddened_gr(df, title='', output_file=None):
    plt.figure(figsize=(10, 6))

    # Separate g and r bands for individual plotting
    for band in ['g', 'r']:  # Specify only the g and r filters
        if band in df['filter'].unique():  # Check if the band exists in the dataframe
            band_df = df[df['filter'] == band]
            plt.errorbar(band_df['mjd'], band_df['mag_dereddened'], yerr=band_df['magerr'],
                         fmt='o', label=f'{band}', alpha=0.8)

    plt.gca().invert_yaxis()
    plt.xlabel("MJD")
    plt.ylabel("De-reddened App-Mag")
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    
    if output_file:
        plt.savefig(output_file)
    
    plt.close()
