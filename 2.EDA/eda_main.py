from eda_preprocessing import load_and_prepare_data, validate_data, generate_summary_statistics
from eda_visualization import load_data_from_csv, visualize_regimen_frequency, visualize_dose_distribution, \
    visualize_age_distribution

# PostgreSQL connection string
connection_str = "postgresql://postgres:wnghks12!!@localhost:5432/juhwanlee"
output_file_path = "eda_output/final_merged_data.csv"


def main():
    print("========== EDA TOOL ==========")
    print("1. Run Data Preprocessing")
    print("2. Run Data Visualization")
    print("================================")

    try:
        # User input for option selection
        choice = int(input("Select an option (1 or 2): ").strip())

        if choice == 1:
            # Execute data preprocessing
            print("\nStarting data preprocessing...")
            data = load_and_prepare_data(connection_str, output_file=output_file_path)
            print("Data preprocessing completed.")

            # Validate the preprocessed data
            print("\nValidating preprocessed data...")
            validate_data(data)

            # Generate and save summary statistics
            print("\nGenerating dataset summary...")
            generate_summary_statistics(data, output_path="eda_output/dataset_summary.csv")
            print("Summary statistics generated and saved.")

        elif choice == 2:
            # Execute data visualization
            print("\nLoading data for visualization...")

            # Ask user for the CSV path
            csv_path = input(f"Enter the path to the CSV file: ").strip()
            print(f"\nUsing CSV file at: {csv_path}")

            # Load the data
            data_for_visualization = load_data_from_csv(csv_path)

            if data_for_visualization is not None:
                print("\nStarting data visualization...")

                # Visualize regimen frequency
                visualize_regimen_frequency(data_for_visualization, output_path="eda_output/variable_distributions/regimen_frequency.png")

                # Visualize dose distribution
                visualize_dose_distribution(data_for_visualization, output_path="eda_output/variable_distributions/dose_distribution.png")

                # Visualize age distribution
                visualize_age_distribution(data_for_visualization, output_path="eda_output/variable_distributions/age_distribution.png")

                print("\nData visualization completed.")
            else:
                print(f"Failed to load data from {csv_path}. Please check the file path.")
        else:
            print("Invalid option. Please select either 1 or 2.")

    except ValueError:
        print("Invalid input. Please enter a numeric value (1 or 2).")


if __name__ == "__main__":
    main()
