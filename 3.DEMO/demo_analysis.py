import os
import io
import psycopg2
import pandas as pd

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
        conn = psycopg2.connect(connection_string)
        cur = conn.cursor()
        buffer = io.StringIO()
        cur.copy_expert(f"COPY {table_name} TO STDOUT WITH CSV HEADER", buffer)
        buffer.seek(0)
        df = pd.read_csv(buffer)
        cur.close()
        conn.close()
        return df
    except (Exception, psycopg2.Error) as error:
        print("Error occurred while loading data from PostgreSQL: ", error)
        return None

def load_and_prepare_data_with_update(connection_string, output_file="final_merged_data.csv"):
    """
    Load, merge, preprocess data, calculate survival rates, and update database.

    Parameters:
    - connection_string (str): The connection string for PostgreSQL.
    - output_file (str): The path to save the final merged data CSV.

    Returns:
    - pd.DataFrame: The final merged DataFrame with survival rates.
    """
    # Load data from PostgreSQL tables
    sact_regimen = load_data_from_postgres("sact_regimen", connection_string).drop(
        columns=["height_at_start_of_regimen", "weight_at_start_of_regimen"]
    )
    sact_cycle = load_data_from_postgres("sact_cycle", connection_string)
    sact_drug_detail = load_data_from_postgres("sact_drug_detail", connection_string)
    av_patient = load_data_from_postgres("av_patient", connection_string)
    av_tumour = load_data_from_postgres("av_tumour", connection_string)
    av_gene = load_data_from_postgres("av_gene", connection_string)

    # Check if all tables are loaded successfully
    for df_name, df in zip(
        ["sact_regimen", "sact_cycle", "sact_drug_detail", "av_patient", "av_tumour", "av_gene"],
        [sact_regimen, sact_cycle, sact_drug_detail, av_patient, av_tumour, av_gene],
    ):
        if df is None:
            raise ValueError(f"Failed to load {df_name}")

    # Clean and standardize column names
    av_patient.columns = av_patient.columns.str.strip().str.lower()
    sact_regimen.columns = sact_regimen.columns.str.strip().str.lower()
    av_tumour.columns = av_tumour.columns.str.strip().str.lower()
    av_gene.columns = av_gene.columns.str.strip().str.lower()

    # Merge datasets
    patient_data = pd.merge(
        sact_regimen,
        av_patient[["link_number", "patientid", "vitalstatus", "vitalstatusdate"]],
        on="link_number",
        how="inner",
    )
    patient_data_with_age_and_site = pd.merge(
        patient_data,
        av_tumour[["patientid", "age", "site_icd10_o2_3char", "stage_best"]],
        on="patientid",
        how="inner",
    )
    patient_data_with_genes = pd.merge(
        patient_data_with_age_and_site,
        av_gene[["patientid", "seq_var"]],
        on="patientid",
        how="left",
    )
    regimen_cycle = pd.merge(sact_regimen, sact_cycle, on="merged_regimen_id", how="inner")
    merged_data = pd.merge(
        regimen_cycle,
        sact_drug_detail[["merged_cycle_id", "actual_dose_per_administration"]],
        on="merged_cycle_id",
        how="inner",
    )
    final_merged_data = pd.merge(
        merged_data,
        patient_data_with_genes[
            [
                "link_number",
                "age",
                "vitalstatus",
                "vitalstatusdate",
                "site_icd10_o2_3char",
                "stage_best",
                "seq_var",
            ]
        ],
        on="link_number",
        how="inner",
    )

    # Handle missing values
    final_merged_data["seq_var"].fillna("Unknown", inplace=True)
    final_merged_data["stage_best"].fillna("Not Available", inplace=True)

    # Calculate survival duration and event
    final_merged_data['duration'] = (pd.to_datetime(final_merged_data['vitalstatusdate']) - pd.to_datetime(final_merged_data['start_date_of_regimen'])).dt.days.abs()
    final_merged_data['event'] = final_merged_data['vitalstatus'].apply(lambda x: 1 if x == 'DE' else 0)

    # Calculate survival rates by regimen
    final_merged_data['survival_rate'] = final_merged_data.groupby('mapped_regimen')['duration'].transform(lambda x: (x > 1825).mean() * 100)

    # Update the database with survival rates
    survival_data = final_merged_data[['mapped_regimen', 'survival_rate']].drop_duplicates()
    update_database_with_survival_rates(connection_string, survival_data)

    # Save to CSV
    final_merged_data.to_csv(output_file, index=False)
    print(f"Final merged data with survival rates saved to: {output_file}")
    return final_merged_data

def update_database_with_survival_rates(connection_string, survival_data, table_name="sact_regimen"):
    """
    Update the database with calculated survival rates.

    Parameters:
    - connection_string (str): Connection string to the PostgreSQL database.
    - survival_data (pd.DataFrame): DataFrame containing the calculated survival rates.
    - table_name (str): Name of the table to update.
    """
    try:
        conn = psycopg2.connect(connection_string)
        cur = conn.cursor()
        temp_table = "temp_survival_data"
        cur.execute(f"CREATE TEMP TABLE {temp_table} (mapped_regimen VARCHAR, survival_rate NUMERIC);")
        conn.commit()

        buffer = io.StringIO()
        survival_data.to_csv(buffer, index=False, header=False)
        buffer.seek(0)
        cur.copy_expert(f"COPY {temp_table} FROM STDIN WITH CSV", buffer)
        conn.commit()

        update_query = f"""
        UPDATE {table_name} AS r
        SET survival_rate = t.survival_rate
        FROM {temp_table} AS t
        WHERE r.mapped_regimen = t.mapped_regimen;
        """
        cur.execute(update_query)
        conn.commit()
        cur.execute(f"DROP TABLE {temp_table};")
        conn.commit()
        cur.close()
        conn.close()
        print(f"Successfully updated survival rates in {table_name}.")
    except Exception as e:
        print(f"Error updating the database: {e}")

if __name__ == "__main__":
    connection_string = "postgresql://postgres:wnghks12!!@localhost:5432/juhwanlee"
    output_file = "demo_output/final_merged_data.csv"
    os.makedirs("demo_output", exist_ok=True)
    final_merged_data = load_and_prepare_data_with_update(connection_string, output_file)
