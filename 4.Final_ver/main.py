import os
import sys
import pandas as pd
from functools import lru_cache

# Ensure the scripts directory is in the path
sys.path.append(os.path.join(os.path.dirname(__file__), "scripts"))

# Import necessary functions
from final_preprocess import execute_final_preprocessing
from initial_preprocess import initial_data_preparation
from visualization import ( # got to this file and change the path of the BASE_DIR
    load_data,
    visualize_treatment_success_rate,
    visualize_cancer_type_success_rate,
    visualize_treatment_modifications,
    visualize_kaplan_meier,
    visualize_treatment_regimen_changes,
)
from visualization_code import extract_visualization_data # got to this file and change the path to the VIS_DATA_DIR

# Define file paths
BASE_DIR = "C:/Users/Black/Desktop/internship/ProjectCancerData/4.Final_ver/data" # Change this to your directory
INITIAL_OUTPUT_FILE = os.path.join(BASE_DIR, "raw/initial_raw_data.csv")
FINAL_OUTPUT_FILE = os.path.join(BASE_DIR, "processed/final_merged_data.csv")
VIS_DATA_DIR = os.path.join(BASE_DIR, "extracted_visualization_data")
os.makedirs(VIS_DATA_DIR, exist_ok=True)

# PostgreSQL connection
DB_CONNECTION_STRING = "postgresql://postgres:Tan%40123@localhost:5432/postgres" #change this to your connection string
connection_string = os.getenv("DB_CONNECTION_STRING", DB_CONNECTION_STRING)

@lru_cache(maxsize=1)
def cached_load_data():
    """Cached data loading function"""
    print("⏳ Loading data... (First time only)")
    return load_data(FINAL_OUTPUT_FILE)

def main():
    """Interactive processing menu"""
    df = None
    while True:
        print("\n🔹 Processing Steps:")
        print("1. Initial Preprocessing")
        print("2. Final Preprocessing")
        print("3. Data Validation")
        print("4. Data Visualization")
        print("5. Extract Sample Data")
        print("6. Exit")
        choice = input("Choose (1-6): ").strip()

        if choice == "1":
            run_initial_processing()
        elif choice == "2":
            run_final_preprocessing(INITIAL_OUTPUT_FILE, FINAL_OUTPUT_FILE)
        elif choice == "3":
            run_data_validation(FINAL_OUTPUT_FILE, "missing_values.xlsx")
        elif choice == "4":
            if df is None:
                df = cached_load_data()
            handle_visualization_menu(df)
        elif choice == "5":
            extract_sample_data(FINAL_OUTPUT_FILE, "sample_data.csv")
        elif choice == "6":
            print("👋 Exiting program.")
            break
        else:
            print("❌ Invalid choice. Enter 1-6.")

def handle_visualization_menu(df):
    """Visualization submenu"""
    print("\n📊 Visualization Options:")
    print("1. Extract Visualization Data")
    print("2. Treatment Success Rate")
    print("3. Cancer Type Success Rate")
    print("4. Treatment Modifications")
    print("5. Survival Analysis")
    print("6. Treatment Evolution")
    print("7. Return to Main")

    viz_choice = input("Choose (1-7): ").strip()
    analysis_map = {
        '1': 'extract',
        '2': 'success_rate',
        '3': 'cancer_type',
        '4': 'modifications',
        '5': 'survival',
        '6': 'evolution'
    }

    if viz_choice == '1':
        for analysis_type in ['success_rate', 'cancer_type', 'modifications', 'survival', 'evolution']:
            extract_visualization_data(df, analysis_type)
    elif viz_choice in ['2', '3', '4', '5', '6']:
        analysis_type = analysis_map[viz_choice]
        data_path = os.path.join(VIS_DATA_DIR, f"visualize_{analysis_type}.csv")
        if not os.path.exists(data_path):
            print(f"⚠️ Missing data file: {os.path.basename(data_path)}")
            return
        {
            '2': visualize_treatment_success_rate,
            '3': visualize_cancer_type_success_rate,
            '4': visualize_treatment_modifications,
            '5': visualize_kaplan_meier,
            '6': visualize_treatment_regimen_changes
        }[viz_choice](data_path)
    elif viz_choice == '7':
        return
    else:
        print("❌ Invalid choice.")

def run_initial_processing():
    """Run the initial preprocessing step."""
    print("🔹 Running Initial Preprocessing...")
    initial_data_preparation(connection_string, INITIAL_OUTPUT_FILE)
    print("✅ Initial preprocessing completed!")

def run_final_preprocessing(input_file, output_file):
    """Run the final preprocessing step."""
    print("🔹 Running Final Preprocessing...")
    execute_final_preprocessing(
        input_file=input_file,
        raw_data_file=os.path.join(BASE_DIR, "raw/initial_raw_data.csv"),
        output_file=output_file
    )
    print("✅ Final preprocessing completed!")

def run_data_validation(file_path, output_excel):
    """Perform data validation by checking for missing values and saving results to an Excel file."""
    print("🔹 Running Data Validation...")
    df = pd.read_csv(file_path, low_memory=False)
    missing_values = df.isnull().sum().reset_index()
    missing_values.columns = ["Variable", "Missing_Count"]
    missing_values.to_excel(output_excel, index=False)
    print(f"✅ Data validation completed! Missing values report saved to {output_excel}")

def extract_sample_data(file_path, output_csv):
    """Extract a sample of 1000 rows from the dataset and save to a CSV file."""
    print("🔹 Extracting Sample Data...")
    df = pd.read_csv(file_path, low_memory=False)
    sample_df = df.sample(n=1000, random_state=42)
    sample_df.to_csv(output_csv, index=False)
    print(f"✅ Sample data extracted! Saved to {output_csv}")

if __name__ == "__main__":
    main()
