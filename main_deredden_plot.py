import pandas as pd
import matplotlib.pyplot as plt
import plot_lc
import os

PLOTS_DIR = "/home/skikk2/Documents/ICCUB/Project/lrn_rates/plots"
os.makedirs(PLOTS_DIR, exist_ok=True)

def v838mon_dereddened():
    # Load the de-reddened light curve CSV
    file_path = "/home/skikk2/Documents/ICCUB/Project/lrn_rates/v838mon_munari_n_dered.csv"
    df = pd.read_csv(file_path)

    # Generate plot
    output_plot = os.path.join(PLOTS_DIR, "v838mon_munari_dered1.png")
    plot_lc.plot_photometry_dereddened(df, title="V838 Mon (De-reddened)", output_file=output_plot)
    print(f"Saved plot to {output_plot}")

def v838mon_dereddened_abs():
    # Load the de-reddened light curve CSV
    file_path = "/home/skikk2/Documents/ICCUB/Project/lrn_rates/v838mon_munari_n_dered.csv"
    df = pd.read_csv(file_path)

    # Generate plot
    output_plot = os.path.join(PLOTS_DIR, "v838mon_abs_dered1.png")
    plot_lc.plot_photometry_dereddened_abs(df, title="V838 Mon (abs-De-reddened)", output_file=output_plot)
    print(f"Saved plot to {output_plot}")


def v838mon_pivot_synthetic_and_plot():
    input_csv = "/home/skikk2/Documents/ICCUB/Project/lrn_rates/v838mon_munari_n_dered_gr_vi.csv"
    output_csv = "/home/skikk2/Documents/ICCUB/Project/lrn_rates/v838mon_munari_n_dered_gr_vi_n.csv"
    
    from lc_data import pivot_synthetic_lc
    pivot_synthetic_lc(input_csv, output_csv)

    # Load and filter for g and r bands only
    df = pd.read_csv(output_csv)
    df_gr = df[df['filter'].isin(['g', 'r'])]

    # Plot
    output_plot = os.path.join(PLOTS_DIR, "v838mon_gr.png")
    plot_lc.plot_photometry_dereddened_gr(df_gr, title="V838 Mon (gr)", output_file=output_plot)
    print(f"Saved plot to {output_plot}")


if __name__ == "__main__":
    v838mon_dereddened()
    v838mon_dereddened_abs()
    #v838mon_pivot_synthetic_and_plot()
