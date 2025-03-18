import os
import io
import psycopg2
import pandas as pd

# Function to load data from a PostgreSQL table into a Pandas DataFrame
# Uses COPY TO STDOUT for efficient data retrieval
def load_data_from_postgres(table_name, connection_string):
    """
    Retrieve data from a PostgreSQL table and load it into a Pandas DataFrame.
    Ensures efficient data transfer and handles exceptions gracefully.
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
        print(f"❌ Error loading table '{table_name}':", error)
        return None

# Function to prepare and preprocess initial dataset by merging multiple tables
def initial_data_preparation(connection_string, output_file):
    """
    Load data from multiple PostgreSQL tables, standardize column names,
    merge relevant datasets, and save the processed output.
    """
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    print("🔹 Loading data from PostgreSQL...")
    sact_regimen = load_data_from_postgres("sact_regimen", connection_string)
    sact_cycle = load_data_from_postgres("sact_cycle", connection_string)
    sact_drug_detail = load_data_from_postgres("sact_drug_detail", connection_string)
    av_patient = load_data_from_postgres("av_patient", connection_string)
    av_tumour = load_data_from_postgres("av_tumour", connection_string)
    av_gene = load_data_from_postgres("av_gene", connection_string)
    sact_outcome = load_data_from_postgres("sact_outcome", connection_string)

    # Validate that all necessary tables are successfully loaded
    table_dict = {
        "sact_regimen": sact_regimen,
        "sact_cycle": sact_cycle,
        "sact_drug_detail": sact_drug_detail,
        "av_patient": av_patient,
        "av_tumour": av_tumour,
        "av_gene": av_gene,
        "sact_outcome": sact_outcome
    }

    missing_tables = [name for name, df in table_dict.items() if df is None]
    if missing_tables:
        raise ValueError(f"❌ Failed to load tables: {', '.join(missing_tables)}")

    print("✅ All necessary tables loaded successfully!")

    # Standardize column names by removing extra spaces and converting to lowercase
    for df in table_dict.values():
        df.columns = df.columns.str.strip().str.lower()

    # Merge datasets step by step to integrate necessary information
    print("🔹 Merging datasets...")

    # Clean and standardize column names
    av_patient.columns = av_patient.columns.str.strip().str.lower() 
    # Rename 'linknumber' to 'link_number' if necessary:
    if 'linknumber' in av_patient.columns:
        av_patient = av_patient.rename(columns={'linknumber': 'link_number'}) # changed the name of the column to match the column name in the sact_regimen table

    # Merging sact_regimen with av_patient
    patient_data = pd.merge(
        sact_regimen,
        av_patient[["link_number", "patientid", "vitalstatus", "vitalstatusdate"]],
        on="link_number",
        how="left"
    )

    # Merging with av_tumour (age, site, stage, comorbidities)
    patient_data_with_age_and_site = pd.merge(
        patient_data,
        av_tumour[["patientid", "age", "site_icd10_o2_3char", "stage_best", "comorbidities_27_03"]],
        on="patientid",
        how="left"
    )

    # Merging with av_gene (genetic data)
    patient_data_with_genes = pd.merge(
        patient_data_with_age_and_site,
        av_gene[["patientid", "seq_var"]],
        on="patientid",
        how="left"
    )

    # Merging with sact_outcome to include modification variables
    patient_data_with_modifications = pd.merge(
        patient_data_with_genes,
        sact_outcome[
            ["merged_regimen_id", "regimen_mod_dose_reduction", "regimen_mod_time_delay", "regimen_mod_stopped_early"]],
        on="merged_regimen_id",  # Use the correct column for merging
        how="left"
    )

    # Save the processed dataset to a CSV file for further analysis
    patient_data_with_modifications.to_csv(output_file, index=False)
    print(f"✅ Initial preprocessed data saved: {output_file}")

    return patient_data_with_modifications
