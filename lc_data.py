import pandas as pd
import numpy as np
from datetime import datetime 
from astropy.time import Time
from astropy.time import Time
from datetime import datetime, timedelta
import extinction
from astropy.cosmology import Planck18 as cosmo


ENGLISH_MONTHS = [
    '', 'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
]

def ut_to_mjd(datestr):
    parts = datestr.strip().split()
    if len(parts) != 3:
        raise ValueError(f"Unexpected date format: {datestr}")
    
    year = int(parts[0])
    month_str = parts[1].strip().title()
    day_frac = float(parts[2])
    
    if month_str not in ENGLISH_MONTHS:
        raise ValueError(f"Invalid month: {month_str} — not in {ENGLISH_MONTHS}")
    
    month = ENGLISH_MONTHS.index(month_str)
    
    day_int = int(day_frac)
    frac = day_frac - day_int
    
    base_date = datetime(year, month, day_int)
    full_date = base_date + timedelta(days=frac)
    
    return Time(full_date, scale='utc').mjd




def load_lightcurve(file_path, source='martini'):
    """
    Loads and standardizes a photometry CSV file from different sources.

    Parameters:
        file_path (str): Path to the CSV file.
        source (str): Source of the data, either 'martini' or 'aavso'.

    Returns:
        pd.DataFrame: Reformatted long-form photometry DataFrame.
    """
    try:
        df = pd.read_csv(file_path)
        print(f"{source.capitalize()} photometry data loaded successfully.")
        print(df.head())
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None

    if source == 'martini':
        filters = ['U', 'B', 'V', 'R', 'I']
        long_rows = []

        for _, row in df.iterrows():
            for flt in filters:
                mag = row.get(flt)
                if pd.isna(mag):
                    continue
                long_rows.append({
                    'inst': 'martini',
                    'filter': flt,
                    'mjd': ut_to_mjd(row.get('dateobs')),
                    'mjderr': 0.0,
                    'mag': mag,
                    'magerr': 0.02,
                    'ATel': 0,
                    'limit': 0
                })
        return pd.DataFrame(long_rows)

    elif source == 'aavso':
        df['mjd'] = df['JD'] - 2400000.5
        df['inst'] = 'aavso'
        df['mjderr'] = 0.0
        df['mag'] = df['Magnitude']
        df['magerr'] = df['Uncertainty'].fillna(0.1)
        df['ATel'] = 0
        df['limit'] = 0
        df['filter'] = df['Band'].str.strip().str.upper()

        cols = ['inst', 'filter', 'mjd', 'mjderr', 'mag', 'magerr', 'ATel', 'limit']
        return df[cols]

    else:
        raise ValueError(f"Unsupported source: {source}")


def lc_goranskij(file_path):
    """
    Reads Goranskij photometry data and converts it to long-format standardized DataFrame.
    
    Parameters:
        file_path (str): Path to the input CSV file.

    Returns:
        pd.DataFrame: Reformatted photometry data.
    """
    try:
        df = pd.read_csv(file_path)
        print("Goranskij data loaded successfully.")
    except Exception as e:
        print(f"Error loading file: {e}")
        return None

    filters = ['U', 'B', 'V', 'R', 'I']
    long_rows = []

    for _, row in df.iterrows():
        for flt in filters:
            mag = row[flt]
            if mag == 0 or pd.isna(mag):
                continue
            long_rows.append({
                'inst': 'goranskij',
                'filter': flt,
                'mjd': row['mjd'],
                'mjderr': 0.0,
                'mag': mag,
                'magerr': 0.1,  # use a default magerr if none provided
                'ATel': 0,
                'limit': 0
            })

    return pd.DataFrame(long_rows)



def stack_v4332sgr(file_paths, output_csv=None):
    """
    Stacks multiple standardized light curve CSVs into one.

    Parameters:
        file_paths (list): List of file paths to individual light curve CSVs.
        output_csv (str, optional): If given, saves the stacked result to this path.

    Returns:
        pd.DataFrame: Combined DataFrame of all input light curves.
    """
    dfs = []
    for path in file_paths:
        try:
            df = pd.read_csv(path)
            dfs.append(df)
        except Exception as e:
            print(f"Could not read {path}: {e}")
    
    if not dfs:
        print("No valid files to stack.")
        return None

    combined = pd.concat(dfs, ignore_index=True)
    
    if output_csv:
        combined.to_csv(output_csv, index=False)
        print(f"Saved stacked light curve to {output_csv}")

    return combined


def lc_v838mon_goranskij(file_path):
    """
    Reads Goranskij photometry data and converts it to long-format standardized DataFrame.
    
    Parameters:
        file_path (str): Path to the input CSV file.

    Returns:
        pd.DataFrame: Reformatted photometry data.
    """
    try:
        df = pd.read_csv(file_path)
        print("Goranskij data loaded successfully.")
    except Exception as e:
        print(f"Error loading file: {e}")
        return None

    filters = ['U', 'B', 'V', 'R', 'I']
    long_rows = []

    for _, row in df.iterrows():
        for flt in filters:
            mag = row[flt]
            if mag == 0 or pd.isna(mag):
                continue
            long_rows.append({
                'inst': 'goranskij',
                'filter': flt,
                'mjd': row['mjd'],
                'mjderr': 0.0,
                'mag': mag,
                'magerr': 0.02, 
                'ATel': 0,
                'limit': 0
            })

    return pd.DataFrame(long_rows)


def lc_v838mon_munari(file_path):
    """
    Reads Goranskij photometry data and converts it to long-format standardized DataFrame.
    
    Parameters:
        file_path (str): Path to the input CSV file.

    Returns:
        pd.DataFrame: Reformatted photometry data.
    """
    try:
        df = pd.read_csv(file_path)
        print("Goranskij data loaded successfully.")
    except Exception as e:
        print(f"Error loading file: {e}")
        return None

    filters = ['U', 'B', 'V', 'R', 'I']
    long_rows = []

    for _, row in df.iterrows():
        for flt in filters:
            mag = row[flt]
            if mag == 0 or pd.isna(mag):
                continue
            long_rows.append({
                'inst': 'munari',
                'filter': flt,
                'mjd': row['mjd'],
                'mjderr': 0.0,
                'mag': mag,
                'magerr': 0.02, 
                'ATel': 0,
                'limit': 0
            })

    return pd.DataFrame(long_rows)

def stack_v838mon(file_paths, output_csv=None):
    """
    Stacks multiple standardized light curve CSVs into one.

    Parameters:
        file_paths (list): List of file paths to individual light curve CSVs.
        output_csv (str, optional): If given, saves the stacked result to this path.

    Returns:
        pd.DataFrame: Combined DataFrame of all input light curves.
    """
    dfs = []
    for path in file_paths:
        try:
            df = pd.read_csv(path)
            dfs.append(df)
        except Exception as e:
            print(f"Could not read {path}: {e}")
    
    if not dfs:
        print("No valid files to stack.")
        return None

    combined = pd.concat(dfs, ignore_index=True)
    
    if output_csv:
        combined.to_csv(output_csv, index=False)
        print(f"Saved stacked light curve to {output_csv}")

    return combined




def pivot_synthetic_lc(input_csv, output_csv):
    df = pd.read_csv(input_csv)

    # Fill synthetic g and r by prioritizing 'strict' when available
    df['g'] = df['g_synth_strict'].combine_first(df['g_synth'])
    df['r'] = df['r_synth_strict'].combine_first(df['r_synth'])

    # Prepare long format rows
    records = []
    for _, row in df.iterrows():
        for band in ['g', 'r']:  # Only g and r for the filter column
            mag = row[band]
            if pd.notna(mag):
                records.append({
                    'inst': row['inst'],
                    'filter': band,  # 'filter' will be either 'g' or 'r'
                    'mjd': row['mjd'],
                    'mjderr': 0,
                    'mag': mag,
                    'magerr': 0.02,
                    'ATel': 0,
                    'limit': 0,
                    'A_lambda': np.nan,
                    'mag_dereddened': mag  # Already dereddened in synthetic data
                   # 'abs_mag': np.nan,  # Fill this later if needed
                })
    
    # Convert the list of records into a DataFrame
    long_df = pd.DataFrame(records)

    # Save the DataFrame to CSV
    long_df.to_csv(output_csv, index=False)
    print(f"Pivoted light curve data saved to {output_csv}")

    df_long = pd.DataFrame(records)
    df_long.to_csv(output_csv, index=False)
    print(f"Pivoted and saved to {output_csv}")
    


# Band effective wavelengths in Angstroms
BAND_WAVELENGTHS = {
    'U': 3600,
    'B': 4400,
    'V': 5500,
    'R': 7100,
    'I': 9700,
    'g': 5200,
    'r': 6700
}

def compute_a_lambda(band, A_V, R_V):
    wl = BAND_WAVELENGTHS.get(band)
    if wl is not None:
        return extinction.fitzpatrick99(np.array([wl]), A_V, R_V, unit='aa')[0]
    else:
        return np.nan

def apply_reddening_df(df, A_V, R_V=3.1, remove=True, mag_col='abs_mag', new_col='app_mag', band_col='filter'):
    
    """
    Apply reddening or dereddening to a DataFrame using extinction curves.
    
    Args:
        df: DataFrame with 'band' and magnitude column (default='abs_mag').
        A_V: Visual extinction.
        R_V: Total-to-selective extinction ratio.
        remove: If True, deredden; if False, apply reddening.
        mag_col: Name of the magnitude column to modify.
        new_col: Name of the output column with corrected magnitudes.
    Returns:
        Modified DataFrame with new_col added.
    """
    df = df.copy()
    df['A_lambda'] = df['filter'].apply(lambda b: compute_a_lambda(b, A_V, R_V))
    
    if remove:
        df[new_col] = df[mag_col] - df['A_lambda']
    else:
        df[new_col] = df[mag_col] + df['A_lambda']
    
    return df.drop(columns='A_lambda')


def appmag_to_absmag(df, mag_col='app_mag', distance_pc=None, z=None, new_col='abs_mag'):
    """
    Add an absolute magnitude column to a DataFrame using either distance or redshift.

    Args:
        df: DataFrame with magnitude column (default='app_mag').
        mag_col: Name of the apparent magnitude column.
        distance_pc: Distance in parsecs.
        z: Redshift (alternative to distance).
        new_col: Name of output absolute magnitude column.

    Returns:
        Modified DataFrame with new_col added.
    """
    df = df.copy()

    if distance_pc is not None:
        DM = 5 * np.log10(distance_pc / 10)
    elif z is not None:
        DM = cosmo.distmod(z).value
    else:
        raise ValueError("Must provide either distance_pc or redshift (z).")
    
    df[new_col] = df[mag_col] - DM
    return df
    
