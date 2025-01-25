
# 데이터 분석 프로젝트 / Data Analysis Project

## 📂 폴더 구조 / Folder Structure

### 1. EDA (탐색적 데이터 분석 / Exploratory Data Analysis)
- **목적 / Purpose**: 데이터를 탐색하고 정리하며 분석에 필요한 통찰을 얻는 단계.
- **구성 / Contents**:
  - `eda_preprocessing.py`: 데이터 로드, 전처리 및 정리 코드 (Data loading, preprocessing, and cleaning code).
  - `eda_visualization.py`: 변수 분포 및 상관 관계 시각화 코드 (Visualization of variable distributions and correlations).
  - `eda_summary.txt`: 주요 EDA 결과 요약 파일 (Summary of key EDA findings).
  - `eda_output/`: 시각화 결과물 저장 폴더 (Folder for visualization outputs).

### 2. 데모 (Demo)
- **목적 / Purpose**: 간단한 분석과 시각화를 통해 데모용 결과를 생성.
  (Simple analysis and visualizations for demonstration purposes.)
- **구성 / Contents**:
  - `demo_analysis.py`: 데모 분석 코드 (Demo analysis code).
  - `demo_visualization.py`: 데모 시각화 코드 (Visualization for demo).
  - `demo_summary_report.txt`: 데모 분석 결과 요약 파일 (Summary report of demo analysis).
  - `demo_output/`: 데모 결과물 저장 폴더 (Folder for demo outputs).

### 3. 심화 분석 (Advanced Analysis)
- **목적 / Purpose**: 고급 분석 및 대화형 대시보드 개발.
  (Advanced analysis and interactive dashboard development.)
- **구성 / Contents**:
  - `advanced_analysis.py`: 심화 분석 코드 (Advanced analysis code).
  - `advanced_visualization.py`: 심화 시각화 코드 (Advanced visualizations).
  - `advanced_dashboard.py`: Plotly Dash 기반 대시보드 개발 코드 (Dashboard development with Plotly Dash).
  - `advanced_summary.txt`: 심화 분석 결과 요약 파일 (Summary of advanced analysis).
  - `advanced_output/`: 심화 분석 결과물 저장 폴더 (Folder for advanced analysis outputs).

---

## 🚀 실행 방법 / How to Run

### 1. EDA 실행 / Run EDA
1. `eda_preprocessing.py`를 실행하여 데이터를 로드하고 전처리를 수행합니다.
   (Run `eda_preprocessing.py` to load and preprocess the data.)
2. `eda_visualization.py`를 실행하여 변수의 분포와 관계를 시각화합니다.
   (Run `eda_visualization.py` to visualize variable distributions and correlations.)
3. 결과는 `eda_output/` 폴더에 저장됩니다.
   (Results are saved in the `eda_output/` folder.)

### 2. 데모 분석 실행 / Run Demo Analysis
1. `demo_analysis.py`를 실행하여 간단한 분석을 수행합니다.
   (Run `demo_analysis.py` to perform simple analysis.)
2. `demo_visualization.py`를 실행하여 주요 결과를 시각화합니다.
   (Run `demo_visualization.py` to visualize key findings.)
3. 결과는 `demo_output/` 폴더에 저장됩니다.
   (Results are saved in the `demo_output/` folder.)

### 3. 심화 분석 실행 / Run Advanced Analysis
1. `advanced_analysis.py`를 실행하여 고급 분석을 수행합니다.
   (Run `advanced_analysis.py` for advanced analysis.)
2. `advanced_visualization.py`를 실행하여 심화 분석 결과를 시각화합니다.
   (Run `advanced_visualization.py` to visualize advanced findings.)
3. `advanced_dashboard.py`를 실행하여 대화형 대시보드를 실행합니다.
   (Run `advanced_dashboard.py` to launch the interactive dashboard.)
4. 결과는 `advanced_output/` 폴더에 저장됩니다.
   (Results are saved in the `advanced_output/` folder.)

---

## 🛠️ 필요 라이브러리 / Required Libraries
- pandas
- seaborn
- matplotlib
- lifelines
- plotly
- dash
- sqlalchemy

---

## 📜 프로젝트 개요 / Project Overview
이 프로젝트는 암 데이터셋을 탐색하고, 치료 요법의 성공률을 시각화하며, 치료 변경 사항을 심화 분석하기 위해 설계되었습니다.  
(This project is designed to explore cancer datasets, visualize treatment regimen success rates, and analyze treatment modifications in depth.)

1. **EDA**: 데이터 탐색 및 정리.
   (Exploratory Data Analysis and cleaning.)
2. **데모**: 간단한 분석 및 결과 시연.
   (Simple analysis and demonstration of results.)
3. **심화 분석**: 고급 통계 분석 및 대화형 대시보드 개발.
   (Advanced statistical analysis and interactive dashboard development.)
