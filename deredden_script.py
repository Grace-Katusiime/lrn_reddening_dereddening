import pandas as pd
import numpy as np
from extinction_utils import apply_reddening_df

# Load object info
objects = pd.read_csv("/home/skikk2/Documents/ICCUB/Project/lrn_rates/lrn_params_v838mon.csv")

for _, obj in objects.iterrows():
    name = obj['Name']
    input_path = obj['input_file']
    output_path = input_path.replace(".csv", "_dered.csv")

    E_BV = float(obj['E_BV'])
    R_V = float(obj['R_V'])
    A_V = R_V * E_BV
    distance_pc = float(obj['distance_pc'])  

    # Load light curve
    df = pd.read_csv(input_path)

    # De-redden and compute abs_mag
    
    df_dered = apply_reddening_df(df, A_V, R_V, band_col='filter', mag_col='mag')


    # Compute abs_mag
    if distance_pc is not None:
        distance_modulus = 5 * np.log10(distance_pc / 10)
        df_dered['abs_mag'] = df_dered['app_mag'] - distance_modulus
        
    # Save output
    df_dered.to_csv(output_path, index=False)
    print(f"{name}: De-reddened light curve (with mag_dereddened & abs_mag) saved to {output_path}")
