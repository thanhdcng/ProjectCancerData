# Cancer Treatment Analysis Project

## Overview
This project analyzes cancer treatment regimens and patient outcomes to derive meaningful insights. The analysis includes data preprocessing, visualization, and statistical evaluations to support decision-making in healthcare.

## Prerequisites
Ensure you have the following dependencies installed:

- Python 3.8+
- pandas
- numpy
- matplotlib
- seaborn
- plotly
- lifelines
- SQLAlchemy

You can install the required packages using:

```bash
pip install -r requirements.txt
```

## Data Loading
Before running the analysis, ensure the dataset is imported into the database using [`cancer_data_importer`](https://github.com/JustinCoKA/ProjectCancerData/tree/main/cancer_data_importer). Follow these steps:

```bash
git clone https://github.com/JustinCoKA/ProjectCancerData.git
cd ProjectCancerData/cancer_data_importer
python import_data.py
```

## Project Structure
```
/Users/juhwanlee/Desktop/coding/final_ver_data/
├── Justin_Cancer Data Analysis.pdf
├── README.md
├── cancer_data_analysis_presentation.ipynb
├── data
│   ├── extracted_visualization_data
│   │   ├── visualize_cancer_type.csv
│   │   ├── visualize_evolution.csv
│   │   ├── visualize_modifications.csv
│   │   ├── visualize_success_rate.csv
│   │   ├── visualize_survival.csv
│   ├── output
│   │   ├── visualizations
│   ├── processed
│   │   ├── final_merged_data.csv
│   ├── raw
│   │   ├── initial_raw_data.csv
├── main.py
├── missing_values.xlsx
├── requirements.txt
├── sample_data.csv
├── scripts
│   ├── __init__.py
│   ├── final_preprocess.py
│   ├── initial_preprocess.py
│   ├── visualization.py
│   ├── visualization_code.py
```

## Usage

### Running the Pipeline
To execute the complete data processing and visualization pipeline, run the main script:

```bash
python main.py
```

### Functionality of `main.py`
The `main.py` script automates the data processing and visualization process in the following steps:

1. **Environment Setup**:
   - Adds the `scripts` directory to the system path.
   - Imports necessary functions from the preprocessing and visualization scripts.

2. **Data Processing**:
   - Loads raw data from `raw/initial_raw_data.csv`.
   - Executes **initial preprocessing** using `initial_data_preparation()`.
   - Saves the processed data into `processed/final_merged_data.csv`.
   - Runs **final preprocessing** using `execute_final_preprocessing()`.

3. **Visualization Data Extraction**:
   - Extracts necessary data for visualizations and saves it to `extracted_visualization_data/`.

4. **Data Visualization**:
   - Generates multiple treatment-related visualizations:
     - **Treatment Success Rate** (`visualize_treatment_success_rate()`)
     - **Cancer Type Success Rate** (`visualize_cancer_type_success_rate()`)
     - **Treatment Modifications** (`visualize_treatment_modifications()`)
     - **Kaplan-Meier Survival Analysis** (`visualize_kaplan_meier()`)
     - **Treatment Regimen Changes** (`visualize_treatment_regimen_changes()`)

## Code Explanation

### `final_preprocess.py`
Handles advanced data cleaning and feature engineering to prepare the dataset for analysis.

### `initial_preprocess.py`
Processes raw data, handles missing values, and standardizes formats for consistency.

### `visualization.py`
Generates various plots and charts to visualize key trends in cancer treatment effectiveness.

### `visualization_code.py`
Includes functions that generate Kaplan-Meier survival curves and other advanced visual analytics.
