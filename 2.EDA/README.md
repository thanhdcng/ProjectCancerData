# Exploratory Data Analysis (EDA) Documentation

## Project Overview
This project performs Exploratory Data Analysis (EDA) on a large-scale cancer dataset to assess data quality, identify missing values, and generate insights for further analysis. It includes data preprocessing, visualization, and summary statistics to facilitate understanding of patient, tumor, and treatment regimen data.

## Key Features
- Handles large-scale cancer datasets (1.7 million patients, 200MB+ data size).
- Cleans and validates data.
- Provides visualizations to highlight patterns and inconsistencies.
- Modular structure for easy extension.

## Project Structure

```
eda/
├── __init__.py               # Package initializer
├── config/
│   ├── __init__.py           # Config module initializer
│   └── settings.py           # Configuration file for paths and parameters
├── preprocessing/
│   ├── __init__.py           # Preprocessing module initializer
│   ├── eda_preprocessing.py  # Handles data cleaning and missing values
├── visualization/
│   ├── __init__.py           # Visualization module initializer
│   ├── eda_visualization.py  # Generates plots and charts
├── main.py                   # Entry point for executing the EDA process
└── summary/
    ├── eda_summary.txt        # Summary of key findings
```

## Installation and Setup

Clone the repository:
```bash
git clone https://github.com/your-username/cancer_data_eda.git
cd cancer_data_eda
```

Install required packages:
```bash
pip install pandas numpy matplotlib seaborn
```

## Usage

Run `main.py` to start the EDA process:
```bash
python main.py
```

### Steps Performed:
1. **Data Preprocessing**
   - Loads dataset.
   - Identifies missing values.
   - Cleans data where necessary.

2. **Exploratory Analysis**
   - Computes summary statistics.
   - Identifies patterns and trends.
   - Generates visualizations.

3. **Missing Values Report**
   - Summary of missing values (from `eda_summary.txt`):
   ```
   Missing Values Summary:
   encore_patient_id                 0
   merged_regimen_id                 0
   height_at_start_of_regimen    89423
   weight_at_start_of_regimen    88399
   intent_of_treatment               0
   date_decision_to_treat            0
   start_date_of_regimen             0
   mapped_regimen                    0
   clinical_trial                    0
   chemo_radiation                   0
   benchmark_group                   0
   link_number                       0
   linknumber                        0
   patientid                         0
   age                               0
   ```

## Code Explanation

### `eda_preprocessing.py`
Handles data cleaning and preprocessing. Includes functions to identify and handle missing values, standardize data formats, and remove inconsistencies.

### `eda_visualization.py`
Generates visualizations to better understand data distributions and patterns. Uses `matplotlib` and `seaborn` for plotting.

### `main.py`
The entry point that executes the EDA pipeline, orchestrating data loading, cleaning, and visualization generation.

---
