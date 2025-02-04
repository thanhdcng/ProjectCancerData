# Cancer Data Analysis Project

## Project Overview
This project aims to identify significant patterns between tumor types and patient survivability by analyzing large-scale cancer datasets (1.7 million patient data, over 200MB).  
It leverages Python, data analysis techniques, and cloud technologies to derive meaningful insights.

## Key Objectives
- Extract valuable insights through in-depth analysis of cancer datasets
- Enhance data exploration, visualization, and interpretation skills
- Provide data-driven recommendations for improving healthcare strategies
- Evaluate data analysis technologies using Google Colab and Generative AI
- Improve proficiency in cloud technologies

## Key Features
- Import cancer datasets into a PostgreSQL database
- Perform data exploration and visualization
- Identify specific use cases and provide actionable insights
- Compile comprehensive analysis reports

## Tech Stack
- Python
- PostgreSQL
- Jupyter Notebook
- pandas, Matplotlib, Seaborn, Plotly, Scikit-learn

## Dataset Description
This project involves analyzing patient treatment regimens and survival data. The following key columns are used:

- **encore_patient_id**: Unique patient identifier
- **merged_regimen_id**: Treatment regimen ID
- **intent_of_treatment**: Purpose of treatment (curative vs palliative)
- **date_decision_to_treat**: Date of treatment decision
- **start_date_of_regimen**: Treatment start date
- **mapped_regimen**: Assigned treatment regimen
- **clinical_trial**: Participation in clinical trials (Yes/No)
- **chemo_radiation**: Chemotherapy/Radiation therapy indicator
- **benchmark_group**: Comparison group
- **patientid**: Unique patient identifier
- **vitalstatus**: Survival status
- **vitalstatusdate**: Last updated survival status date
- **age**: Patient’s age
- **site_icd10_o2_3char**: Cancer type (ICD-10 code)
- **stage_best**: Cancer staging information
- **comorbidities_27_03**: Comorbidities (pre-existing conditions)
- **seq_var**: Genetic mutation information
- **duration**: Survival duration (calculated based on follow-up period)
- **event_mapped**: Mortality indicator (1=Deceased, 0=Survived, -1=Unknown)
- **previous_regimen**: Previous treatment regimen
- **modification_reason**: Reason for treatment modification

## How to Run
1. Install the required libraries:
   ```bash
   pip install -r requirements_en.txt
   ```
2. Launch Jupyter Notebook:
   ```bash
   jupyter notebook
   ```
3. Open `cancer_data_analysis_presentation_en.ipynb` and follow the analysis.

## End Users
- **Healthcare Professionals**: Optimize treatment regimens
- **Administrators**: Develop hospital and healthcare management strategies
- **Policy Makers**: Establish medical policies and patient care guidelines

## Contributions
This project is an open collaboration among healthcare researchers, data scientists, and engineers. Feel free to submit a Pull Request if you would like to contribute.

---

© 2025 Cancer Data Analysis Project
