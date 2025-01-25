# Data Cleaning and Validation Plan

## 1. Project Overview (프로젝트 개요)

### Objective (목적)
- Ensure data quality for `Sact_Regimen` and related tables to establish a foundation for successful analysis.
  - `Sact_Regimen` 및 관련 테이블의 데이터 품질을 보장하여 성공적인 분석의 기반을 마련합니다.

### Analysis Scope (분석 범위)
- Includes the following tables:
  - `Sact_Regimen`
  - `AV_Patient`
  - `AV_Tumour`
  - `AV_Gene`
  - `Sact_Cycle`
  - `Sact_Outcome`
  - `Sact_Drug_Detail`
  - 다음 테이블이 포함됩니다:
    - `Sact_Regimen`
    - `AV_Patient`
    - `AV_Tumour`
    - `AV_Gene`
    - `Sact_Cycle`
    - `Sact_Outcome`
    - `Sact_Drug_Detail`

---

## 2. Key Tables and Fields with Rationale (주요 테이블 및 필드 선정 이유)

### 2.1 `Sact_Regimen` (Treatment Regimen Data / 치료 요법 데이터)
- **Role (역할):**
  - Central table containing treatment regimen details.
    - 요법 관련 세부 정보를 포함하는 중심 테이블.
- **Selected Fields (선정 필드):**
  - `MERGED_REGIMEN_ID`: Unique identifier for regimens.
    - 요법의 고유 식별자.
  - `ENCORE_PATIENT_ID`: Foreign key linking regimens to patients.
    - 요법과 환자를 연결하는 외래 키.
  - `START_DATE_OF_REGIMEN`, `END_DATE_OF_REGIMEN`: Used for analyzing treatment duration and change patterns.
    - 요법 기간 및 변경 패턴 분석에 사용됨.
  - `MAPPED_REGIMEN`: Treatment name for comparison and success rate analysis.
    - 비교 및 성공률 분석을 위한 요법 이름.

### 2.2 `AV_Patient` (Patient Information / 환자 정보)
- **Role (역할):**
  - Provides demographic and survival data.
    - 인구통계학적 정보와 생존 데이터를 제공합니다.
- **Selected Fields (선정 필드):**
  - `PATIENTID`: Unique patient ID.
    - 환자의 고유 ID.
  - `GENDER`: Analyze treatment response differences by gender.
    - 성별에 따른 요법 반응 차이를 분석.
  - `VITALSTATUS`, `VITALSTATUSDATE`: Critical for survival rate analysis.
    - 생존율 분석에 필수적.

### 2.3 `AV_Tumour` (Tumor Data / 종양 데이터)
- **Role (역할):**
  - Contains cancer stage and diagnosis details for evaluating treatment efficacy.
    - 요법 효과 평가를 위한 암 병기 및 진단 세부 정보를 포함.
- **Selected Fields (선정 필드):**
  - `TUMOURID`: Unique tumor ID.
    - 종양의 고유 ID.
  - `DIAGNOSISDATEBEST`: Diagnosis date, comparable to treatment initiation.
    - 진단 날짜로, 요법 시작 시점과 비교 가능.
  - `STAGE_BEST`: Cancer stage correlated with treatment success.
    - 요법 성공과 연관된 암 병기.

### 2.4 `AV_Gene` (Gene Mutation Data / 유전자 변이 데이터)
- **Role (역할):**
  - Evaluate the impact of specific gene mutations on treatment outcomes.
    - 특정 유전자 변이가 요법 결과에 미치는 영향을 평가.
- **Selected Fields (선정 필드):**
  - `GENEID`: Unique gene ID.
    - 유전자의 고유 ID.
  - `ABNORMAL_GAT`: Abnormal gene information impacting treatment efficacy.
    - 요법 효과에 영향을 미치는 이상 유전자 정보.

### 2.5 Supporting Tables (보조 테이블)
- `Sact_Cycle`, `Sact_Outcome`, `Sact_Drug_Detail`
  - **Role (역할):** Provide cycle-level, outcome-level, and drug-level details for detailed analysis.
    - 사이클, 결과, 약물 수준의 세부 정보를 제공하여 세부 분석에 활용.

---

## 3. Excluded Elements (제외된 요소)

### 3.1 Height and Weight (키와 몸무게)
- **Reason (제외 이유):**
  - Significant missing values and limited direct impact on analysis.
    - 결측값이 많고 분석에 직접적인 영향을 미치지 않음.

### 3.2 Radiotherapy Tables (방사선 치료 테이블)
- **Tables (테이블):** `Rtds_Combined`, `Rtds_Episode`, `Rtds_Exposure`, `Rtds_Prescription`
- **Reason (제외 이유):**
  - Less relevant for chemotherapy-focused analysis.
    - 화학요법 중심 분석과 관련성이 낮음.

---

## 4. Data Validation Strategy (데이터 검증 전략)

1. **Handle NULL Values (NULL 값 처리):**
   - Detect and replace missing values in critical fields.
     - 주요 필드의 결측값을 탐지하고 대체.
2. **Remove Duplicates (중복 데이터 제거):**
   - Identify and remove duplicate records in key fields.
     - 주요 필드에서 중복 데이터를 식별하고 제거.
3. **Verify Foreign Key Integrity (외래 키 무결성 확인):**
   - Ensure relationships between tables are consistent.
     - 테이블 간 관계가 일관성을 유지하도록 확인.
4. **Validate Dates (날짜 검증):**
   - Check treatment and diagnosis dates for logical consistency.
     - 요법 및 진단 날짜의 논리적 일관성을 확인.

---

## 5. Analysis Strategy (분석 전략)

1. **Treatment Success Rates (요법 성공률 분석):**
   - Use Kaplan-Meier curves to analyze survival rates.
     - Kaplan-Meier 곡선을 사용해 생존율 분석.
2. **Modification Patterns (변경 패턴 분석):**
   - Identify causes and patterns of treatment modifications.
     - 요법 변경 원인과 패턴 식별.
3. **Gene Correlation Analysis (유전자 상관관계 분석):**
   - Assess correlations between gene mutations and treatment outcomes.
     - 유전자 변이와 요법 결과 간 상관관계를 평가.

---

## 6. Next Steps (다음 단계)

1. Perform data validation tasks.
   - 데이터 검증 작업 수행.
2. Save cleaned data into new tables.
   - 정리된 데이터를 새로운 테이블에 저장.
3. Begin analysis and visualization tasks.
   - 분석 및 시각화 작업 시작.

