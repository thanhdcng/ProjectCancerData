import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import numpy as np
import pandas as pd


def load_data_from_csv(file_path):
    """
    Load data from a CSV file.

    Parameters:
    - file_path (str): Path to the CSV file.

    Returns:
    - pd.DataFrame: Loaded DataFrame.
    """
    try:
        data = pd.read_csv(file_path)
        print(f"Data loaded successfully from {file_path}")
        return data
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except Exception as e:
        print(f"Error loading data: {e}")
        return None


def visualize_data(data, column, plot_type="hist", bins=30, color="skyblue", title="Visualization", xlabel="X-axis",
                   ylabel="Frequency", output_path=None, annotate=False):
    """
    Generalized visualization function to handle different types of plots.

    Parameters:
    - data (pd.DataFrame): DataFrame containing the data.
    - column (str): Column name to visualize.
    - plot_type (str): Type of plot ('hist' for histogram, 'bar' for bar chart).
    - bins (int): Number of bins for histogram (if applicable).
    - color (str): Color of the plot.
    - title (str): Title of the plot.
    - xlabel (str): Label for the X-axis.
    - ylabel (str): Label for the Y-axis.
    - output_path (str): Path to save the visualization. If None, the plot will only be shown.
    - annotate (bool): Whether to display value annotations on the bars.

    Returns:
    - None
    """
    if column not in data.columns:
        raise ValueError(f"Column '{column}' not found in the DataFrame.")

    plt.figure(figsize=(14, 8))

    if plot_type == "hist":
        sns.histplot(data[column].dropna(), bins=bins, kde=True, color=color, edgecolor="black")
    elif plot_type == "bar":
        bar_data = data[column].value_counts().head(20)
        ax = bar_data.plot(kind="bar", color=color, edgecolor="black", width=0.7)

        if annotate:
            for i, value in enumerate(bar_data):
                ax.text(i, value + (value * 0.01), f"{value:,}", ha="center", va="bottom", fontsize=10,
                        fontweight="bold")
    else:
        raise ValueError("Invalid plot_type. Use 'hist' or 'bar'.")

    plt.title(title, fontsize=16, pad=10)
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.xticks(rotation=45, ha="right", fontsize=10, wrap=True)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout(pad=3.0)

    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches="tight", pad_inches=0.3)
        print(f"Plot saved to {output_path}")
    else:
        plt.show()
    plt.close()

def visualize_regimen_frequency(data, output_path="eda_output/variable_distributions/regimen_frequency.png"):
    plt.figure(figsize=(18, 10))
    colors = plt.cm.Blues(np.linspace(0.4, 0.8, 20))

    # Create bar chart
    ax = plt.gca()
    bar_data = data["mapped_regimen"].value_counts().head(20)
    bars = ax.bar(range(len(bar_data)), bar_data.values, color=colors, edgecolor="black", width=0.8)

    # Set x-axis labels
    ax.set_xticks(range(len(bar_data)))
    ax.set_xticklabels(bar_data.index, rotation=45, ha='right')

    # Adjust x-axis label padding
    ax.tick_params(axis='x', which='major', pad=10)  # Increased pad to 10 for better spacing

    # Title and labels
    plt.title("Top 20 Regimen Frequencies", pad=20, fontsize=16, fontweight="bold")
    plt.xlabel("Regimen Type", fontsize=12, labelpad=10)
    plt.ylabel("Frequency", fontsize=12)
    plt.grid(axis="y", linestyle="--", alpha=0.3)

    # Adjust bottom margin
    plt.subplots_adjust(bottom=0.3)  # Increased bottom margin for more space

    # Save plot
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()


def visualize_dose_distribution(data, output_path="eda_output/variable_distributions/dose_distribution.png"):
    # Set the style for a cleaner look
    plt.style.use('seaborn-v0_8-whitegrid')

    # Figure and axis setup
    fig, ax = plt.subplots(figsize=(16, 10))

    # Create the histogram
    n, bins, patches = plt.hist(
        data["actual_dose_per_administration"],
        bins=30,
        color='#A78BFA',  # Soft purple
        edgecolor='black',
        linewidth=0.7,
        alpha=0.8,
        range=(0, 5e6)
    )

    # Set y-axis to log scale
    ax.set_yscale('log')

    # Set x-axis and y-axis limits
    ax.set_xlim(-0.2e6, 5.2e6)
    ax.set_ylim(1, 1e7)

    # Improve grid settings
    ax.grid(visible=True, which='major', linestyle='-', alpha=0.3, color='gray')
    ax.grid(visible=True, which='minor', linestyle=':', alpha=0.2, color='gray')

    # Add title and axis labels
    ax.set_title(
        "Distribution of Actual Dose Per Administration",
        fontsize=18,
        fontweight='bold',
        pad=30
    )
    ax.set_xlabel("Dose (Million Units)", fontsize=14, labelpad=15)
    ax.set_ylabel("Frequency (Log Scale)", fontsize=14, labelpad=15)

    # Format x-axis ticks
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1e6))  # Every 1M
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x / 1e6)}M'))

    # Format y-axis ticks
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: f"{int(y):,}" if y >= 1 else f"{y:.1f}"))

    # Customize tick parameters
    ax.tick_params(axis='both', which='major', labelsize=12)
    ax.tick_params(axis='both', which='minor', labelsize=10)

    # Add subtle borders around the plot
    for spine in ax.spines.values():
        spine.set_linewidth(0.8)
        spine.set_color('#505050')

    # Adjust layout to avoid overlapping elements
    plt.tight_layout()

    # Save the plot to the specified path
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches="tight", facecolor='white')
    plt.close()

def visualize_age_distribution(data, output_path="eda_output/variable_distributions/age_distribution.png"):
    """
    Visualize age distribution.

    Parameters:
    - data (pd.DataFrame): DataFrame containing the data.
    - output_path (str): Path to save the visualization. If None, the plot will only be shown.
    """
    if "age" not in data.columns:
        raise ValueError("Column 'age' not found in the DataFrame.")

    # Drop NaN values
    age_data = data['age'].dropna()

    if age_data.empty:
        raise ValueError("No valid data found in 'age' column for visualization.")

    plt.figure(figsize=(12, 6))
    sns.histplot(age_data, bins=20, kde=True, color="skyblue", edgecolor="black")
    plt.title("Age Distribution")
    plt.xlabel("Age")
    plt.ylabel("Frequency")
    plt.tight_layout()

    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        print(f"Age distribution plot saved to {output_path}")
    else:
        plt.show()
    plt.close()
