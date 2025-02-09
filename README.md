# Cancer Data Analytics Project

## Project Overview

This project aims to identify significant patterns between tumor types and patient survivability by analyzing large-scale cancer datasets containing 1.7 million patient records (over 200MB). The project utilizes Python, data analysis techniques, and cloud technologies to derive meaningful insights that can inform healthcare strategies.

## Key Objectives

- **Extract valuable insights** through in-depth analysis of cancer datasets.
- **Enhance data exploration, visualization, and interpretation skills** to communicate findings effectively.
- **Provide data-driven recommendations** for improving healthcare strategies.
- **Evaluate data analysis technologies** including PostgreSQL, Google Colab, and Generative AI.

## Tech Stack

- **Programming Language**: Python  
- **Database**: PostgreSQL  
- **Development Environment**: Jupyter Notebook, Google Colab  
- **Libraries & Tools**: `pandas`, `Matplotlib`, `Seaborn`, `Plotly`

## End Users

- **Healthcare Professionals**: To analyze treatment outcomes and improve patient care.
- **Administrators**: To monitor regimen effectiveness and streamline hospital processes.
- **Policy Makers**: To inform healthcare policies and improve survival rates.

## Project Structure

```
/Users/juhwanlee/Documents/GitHub/ProjectCancerData
├── 1. Data_Preparation_and_Management
│   ├── DATA RELATED TO REGIMENS CLEANING AND VALIDATION .pdf
│   ├── [ER diagram] Cancer_Data.pdf
│   ├── cancer_data_importer
│   │   ├── README.md
│   │   ├── __init__.py
│   │   ├── config
│   │   │   ├── __init__.py
│   │   │   └── db_config.py
│   │   ├── importers
│   │   │   ├── __init__.py
│   │   │   ├── av_gene_importer.py
│   │   │   ├── av_patient_importer.py
│   │   │   ├── av_tumour_importer.py
│   │   │   ├── base_importer.py
│   │   │   ├── rtds_combined_importer.py
│   │   │   ├── rtds_episode_importer.py
│   │   │   ├── rtds_exposure_importer.py
│   │   │   ├── rtds_prescription_importer.py
│   │   │   ├── sact_cycle_importer.py
│   │   │   ├── sact_drug_detail_importer.py
│   │   │   ├── sact_outcome_importer.py
│   │   │   └── sact_regimen_importer.py
│   │   └── main.py
│   └── dataCleaning_Validation
│       ├── DATA RELATED TO REGIMENS CLEANING AND VALIDATION .pdf
│       ├── README.md
│       └── data_imputation
│           ├── av_gene
│           │   └── Check_missing_av_gene.sql
│           ├── av_patient
│           │   ├── Check_missing_av_patient.sql
│           │   ├── Duplicate_check_av_patient.sql
│           │   └── av_patient_vitalstatusdate.py
│           ├── av_tumour
│           │   ├── Check_missing_av_tumour.sql
│           │   └── Duplicate_check_av_tumour.sql
│           ├── rtds_regimen
│           │   ├── Duplicate_check_sact_regimen.sql
│           │   ├── FK_Intergrity_check_regimenNPatient.sql
│           │   ├── FK_Intergrity_check_regimenNtumour.sql
│           │   └── sact_regimen_major_flled.py
│           └── supportdata
│               ├── start_date_of_cycle.sql
│               └── supportDataCheck.py
├── 2.EDA
│   ├── eda_main.py
│   ├── eda_output
│   │   ├── dataset_summary.csv
│   │   └── variable_distributions
│   │       ├── age_distribution.png
│   │       ├── dose_distribution.png
│   │       └── regimen_frequency.png
│   ├── eda_preprocessing.py
│   ├── eda_summary.txt
│   └── eda_visualization.py
├── 3.DEMO
│   ├── demo_analysis.py
│   ├── demo_output
│   │   ├── demo_summary_report.txt
│   │   ├── gene_mutations_regimen_changes.png
│   │   ├── gene_mutations_regimen_changes_fixed.png
│   │   ├── kaplan_meier_survival_analysis.png
│   │   ├── plot_tumor_stage_survival.png
│   │   ├── regimen
│   │   │   ├── all_regimen
│   │   │   │   ├── all_average_survival_rate_by_regimen_with_numbers.png
│   │   │   │   └── all_regimen_mapping_table.csv
│   │   │   └── top_regimens
│   │   │       ├── N_regimen_mapping_table.csv
│   │   │       └── top_average_survival_rate_by_regimen_with_numbers.png
│   │   ├── regimen_changes_over_years.png
│   │   └── survival_rate_by_cancer_type.png
│   └── demo_visualization.py
├── 4. Final_ver
│   ├── README.md
│   ├── cancer_data_analysis_presentation.ipynb
│   ├── data
│   │   ├── extracted_visualization_data
│   │   │   └── readme.md
│   │   ├── output
│   │   │   └── readme.md
│   │   ├── processed
│   │   │   └── readme.md
│   │   └── raw
│   │       └── readme.md
│   ├── main.py
│   ├── requirements.txt
│   ├── sample_data.csv
│   └── scripts
│       ├── __init__.py
│       ├── final_preprocess.py
│       ├── initial_preprocess.py
│       ├── visualization.py
│       └── visualization_code.py
├── 5. Presentation
│   ├── Justin_Cancer Data Analysis.pdf
│   └── cancer_data_analysis_presentation.ipynb
└── README.md
```

## Timeline

| Week  | Task |
|-------|------|
| 1  | Project setup and data loading |
| 2-3 | Initial chart creation and exploratory data analysis |
| 4-5 | Advanced analysis and interactive chart development |
| 6  | Final presentation and video production |
