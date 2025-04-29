import pandas as pd
import numpy as np
import extinction
from astropy.cosmology import Planck18 as cosmo

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
    

