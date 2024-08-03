import matplotlib.pyplot as plt
import seaborn as sns

def apply_plot_settings():
    # Set plot background to be transparent
    plt.rcParams['figure.facecolor'] = 'none'
    plt.rcParams['axes.facecolor'] = 'none'
    plt.rcParams['savefig.facecolor'] = 'none'
    
    # Set text and grid colors to match the new theme
    plt.rcParams['axes.labelcolor'] = '#333333'  # Dark Gray text color
    plt.rcParams['xtick.color'] = '#333333'  # Dark Gray tick color
    plt.rcParams['ytick.color'] = '#333333'  # Dark Gray tick color
    plt.rcParams['grid.color'] = '#D3D3D3'  # Light Gray grid color
    plt.rcParams['text.color'] = '#333333'  # Dark Gray text color
    
    # Set font to match the config
    plt.rcParams['font.family'] = 'sans-serif'

def apply_axes_settings(axes):
    if isinstance(axes, sns.axisgrid.PairGrid):
        axes = axes.axes.flatten()
    for ax in axes:
        ax.patch.set_alpha(0.0)
        # Change the color of the spine to match the new theme
        ax.spines['top'].set_color('#333333')  # Dark Gray spine color
        ax.spines['right'].set_color('#333333')  # Dark Gray spine color
        ax.spines['left'].set_color('#333333')  # Dark Gray spine color
        ax.spines['bottom'].set_color('#333333')  # Dark Gray spine color