import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io
import os
import psycopg2


def load_data_from_postgres(table_name, connection_string):
    """
    Using 'COPY' Command Load data from a PostgreSQL table.

    Parameters:
    - table_name (str): The name of the table to load.
    - connection_string (str): The connection string for the PostgreSQL database.

    Returns:
    - pd.DataFrame: DataFrame containing the table data.
    """

    try:
        # DATABASE connection
        conn = psycopg2.connect(connection_string)
        # create cursor
        cur = conn.cursor()
        #create a buffer to store the data
        buffer = io.StringIO()
        #excute copy command
        cur.copy_expert(f"COPY {table_name} TO STDOUT WITH CSV HEADER", buffer)
        #reset buffer contents into a DataFrame
        buffer.seek(0)
        #read buffer contents into a dataframe
        df = pd.read_csv(buffer)

        #close the connection
        cur.close()
        conn.close()

        return df

    except(Exception, psycopg2.Error) as error:
        print("Error occurred while loading data from PostgreSQL: ", error)
        return None

def check_missing_values(df):
    """
    Check for missing values in a DataFrame.

    Parameters:
    - df (pd.DataFrame): The DataFrame to check.

    Returns:
    - pd.DataFrame: Missing values count and percentage per column.
    """
    # Calculate missing values and their percentages
    missing_count = df.isnull().sum()
    missing_percentage = 100 * missing_count / len(df)

    # Create a summary table
    missing_table = pd.DataFrame({
        "Missing Values": missing_count,
        "Percentage": missing_percentage
    }).sort_values("Missing Values", ascending=False)

    return missing_table

def fill_missing_values(df, column, method="mean"):
    """
    Fill missing values in a specified column.

    Parameters:
    - df (pd.DataFrame): The DataFrame.
    - column (str): The column name to fill missing values for.
    - method (str): The method to use for filling ('mean', 'median', 'mode').

    Returns:
    - pd.DataFrame: The DataFrame with missing values filled.
    """
    if method == "mean": #AVG
        df[column] = df[column].fillna(df[column].mean())
    elif method == "median":
        df[column] = df[column].fillna(df[column].median())
    elif method == "mode": #Most Frequent
        df[column] = df[column].fillna(df[column].mode()[0])
    return df

def merge_dataframes(dataframes, merge_keys, how="inner"):
    """
    Merge multiple DataFrames sequentially.

    Parameters:
    - dataframes (list of pd.DataFrame): List of DataFrames to merge.
    - merge_keys (list of tuples): List of tuples specifying the keys for merging.
    - how (str): The type of merge ('inner', 'outer', etc.).

    Returns:
    - pd.DataFrame: Merged DataFrame.
    """
    merged_df = dataframes[0]
    for i in range(1, len(dataframes)):
        merged_df = pd.merge(
            merged_df,
            dataframes[i],
            left_on=merge_keys[i - 1][0],
            right_on=merge_keys[i - 1][1],
            how=how
        )
    return merged_df

def load_and_prepare_data(connection_string, output_file="final_merged_data.csv"):
    """
    Load, merge, and preprocess data for EDA.
    """
    sact_regimen = load_data_from_postgres("sact_regimen", connection_string).drop(columns=["height_at_start_of_regimen", "weight_at_start_of_regimen"])
    sact_cycle = load_data_from_postgres("sact_cycle", connection_string)
    sact_drug_detail = load_data_from_postgres("sact_drug_detail", connection_string)
    av_patient = load_data_from_postgres("av_patient", connection_string)
    av_tumour = load_data_from_postgres("av_tumour", connection_string)

    for df_name, df in zip(["sact_regimen", "sact_cycle", "sact_drug_detail", "av_patient", "av_tumour"], [sact_regimen, sact_cycle, sact_drug_detail, av_patient, av_tumour]):
        if df is None:
            raise ValueError(f"Failed to load {df_name}")

    av_patient.columns = av_patient.columns.str.strip().str.lower()

    patient_data = pd.merge(sact_regimen, av_patient[["link_number", "patientid"]], on="link_number", how="inner")
    patient_data_with_age = pd.merge(patient_data, av_tumour[["patientid", "age"]], on="patientid", how="inner")

    regimen_cycle = pd.merge(sact_regimen, sact_cycle, on="merged_regimen_id", how="inner")
    merged_data = pd.merge(regimen_cycle, sact_drug_detail[["merged_cycle_id", "actual_dose_per_administration"]], on="merged_cycle_id", how="inner")

    final_merged_data = pd.merge(merged_data, patient_data_with_age[["link_number", "age"]], on="link_number", how="inner")
    final_merged_data.to_csv(output_file, index=False)
    print(f"Final merged data saved to: {output_file}")
    return final_merged_data

def validate_data(merged_data):
    """
    Validate merged data for final checks.

    Parameters:
    - merged_data (pd.DataFrame): The merged and cleaned data.

    Returns:
    - None
    """
    print("Merged Data Head:")
    print(merged_data.head())

    print("\nColumn Information:")
    print(merged_data.info())

    print("\nMissing Values After Merging:")
    print(check_missing_values(merged_data))

def generate_summary_statistics(data, output_path="eda_output/dataset_summary.csv"):
    """
    Generate and save dataset summary statistics.

    Parameters:
    - data (pd.DataFrame): DataFrame containing the data.
    - output_path (str): File path to save the summary.

    Returns:
    - None
    """
    summary = data.describe(include="all").transpose()
    summary.to_csv(output_path, index=True)
    print(f"Summary statistics saved to {output_path}")

def generate_missing_value_report(data, output_path="eda_output/missing_value_report.png"):
    """
    Generate a missing value report and save it as a heatmap.

    Parameters:
    - data (pd.DataFrame): DataFrame containing the data.
    - output_path (str): File path to save the heatmap.

    Returns:
    - None
    """
    plt.figure(figsize=(12, 8))
    sns.heatmap(data.isnull(), cbar=False, cmap="viridis")
    plt.title("Missing Value Heatmap")
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Missing value report saved to {output_path}")
