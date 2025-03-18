# Data Cleaning and Validation Plan

## 1. Project Overview

### Objective
- Ensure data quality for `Sact_Regimen` and related tables to establish a foundation for successful analysis.

### Analysis Scope 
- Includes the following tables:
  - `Sact_Regimen`
  - `AV_Patient`
  - `AV_Tumour`
  - `AV_Gene`
  - `Sact_Cycle`
  - `Sact_Outcome`
  - `Sact_Drug_Detail`

---

## 2. Key Tables and Fields with Rationale 

### 2.1 `Sact_Regimen` (Treatment Regimen Data)
- **Role:**
  - Central table containing treatment regimen details.
- **Selected Fields:**
  - `MERGED_REGIMEN_ID`: Unique identifier for regimens.
  - `ENCORE_PATIENT_ID`: Foreign key linking regimens to patients.
  - `START_DATE_OF_REGIMEN`, `END_DATE_OF_REGIMEN`: Used for analyzing treatment duration and change patterns.
  - `MAPPED_REGIMEN`: Treatment name for comparison and success rate analysis.

### 2.2 `AV_Patient` (Patient Information)
- **Role:**
  - Provides demographic and survival data.
- **Selected Fields:**
  - `PATIENTID`: Unique patient ID.
  - `GENDER`: Analyze treatment response differences by gender.
  - `VITALSTATUS`, `VITALSTATUSDATE`: Critical for survival rate analysis.

### 2.3 `AV_Tumour` (Tumor Data)
- **Role:**
  - Contains cancer stage and diagnosis details for evaluating treatment efficacy.
- **Selected Fields:**
  - `TUMOURID`: Unique tumor ID.
  - `DIAGNOSISDATEBEST`: Diagnosis date, comparable to treatment initiation.
  - `STAGE_BEST`: Cancer stage correlated with treatment success.

### 2.4 `AV_Gene` (Gene Mutation Data)
- **Role:**
  - Evaluate the impact of specific gene mutations on treatment outcomes.
- **Selected Fields:**
  - `GENEID`: Unique gene ID.
  - `ABNORMAL_GAT`: Abnormal gene information impacting treatment efficacy.

### 2.5 Supporting Tables
- `Sact_Cycle`, `Sact_Outcome`, `Sact_Drug_Detail`
  - **Role:** Provide cycle-level, outcome-level, and drug-level details for detailed analysis.

---

## 3. Excluded Elements 

### 3.1 Height and Weight 
- **Reason:**
  - Significant missing values and limited direct impact on analysis.

### 3.2 Radiotherapy Tables 
- **Tables:** `Rtds_Combined`, `Rtds_Episode`, `Rtds_Exposure`, `Rtds_Prescription`
- **Reason :**
  - Less relevant for chemotherapy-focused analysis.

---

## 4. Data Validation Strategy

1. **Handle NULL Values:**
   - Detect and replace missing values in critical fields.
2. **Remove Duplicates:**
   - Identify and remove duplicate records in key fields.
3. **Verify Foreign Key Integrity:**
   - Ensure relationships between tables are consistent.
4. **Validate Dates:**
   - Check treatment and diagnosis dates for logical consistency.

---

## 5. Analysis Strategy

1. **Treatment Success Rates:**
   - Use Kaplan-Meier curves to analyze survival rates.
2. **Modification Patterns:**
   - Identify causes and patterns of treatment modifications.
3. **Gene Correlation Analysis:**
   - Assess correlations between gene mutations and treatment outcomes.

---

## 6. Next Steps

1. Perform data validation tasks.
2. Save cleaned data into new tables.
3. Begin analysis and visualization tasks.

