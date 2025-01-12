# Cancer Data Importer

## 프로젝트 개요 | Project Overview

이 프로젝트는 대규모 암 데이터셋을 PostgreSQL 데이터베이스로 가져오고 분석하기 위한 Python 기반 도구입니다. 1.7백만 명의 환자 데이터를 포함한 200MB 이상의 데이터셋을 처리하며, 종양 유형과 환자 생존율 간의 중요한 패턴을 파악하는 것을 목표로 합니다.

This project is a Python-based tool for importing and analyzing large-scale cancer datasets into a PostgreSQL database. It processes datasets over 200MB, including data from 1.7 million patients, aiming to identify significant patterns between tumor types and patient survivability.

# 주요 기능 | Key Features
- PostgreSQL 데이터베이스로 암 데이터셋 가져오기
- 환자, 종양, 유전자 데이터 처리
- 데이터 정제 및 유효성 검사
- 모듈식 설계로 쉬운 확장 가능

- Import cancer datasets into PostgreSQL database
- Process patient, tumor, and gene data
- Data cleaning and validation
- Modular design for easy expansion

# 프로젝트 구조 | Project Structure

cancer_data_importer/

├── __init__.py               # Package initializer

├── config/

│   ├── __init__.py           # Config module initializer

│   └── db_config.py          # Database configuration and connection settings

├── importers/

│   ├── __init__.py           # Importers module initializer

│   ├── base_importer.py      # Base class for all importers

│   ├── av_gene_importer.py   # Importer for gene-related data

│   ├── av_patient_importer.py # Importer for patient-related data

│   └── av_tumour_importer.py  # Importer for tumor-related data

└── main.py                   # Entry point for running the data importer



# 설치 및 설정 | Installation and Setup
저장소 클론 | Clone the repository:

git clone https://github.com/your-username/cancer_data_importer.git

cd cancer_data_importer

# 필요한 패키지 설치 | Install required packages:
pip install psycopg2 python-dotenv

# 데이터베이스 설정 | Configure database:
config/db_config.py 

파일에서 데이터베이스 연결 정보를 수정하세요.

Modify database connection information in config/db_config.py file.

# 사용 방법 | Usage

1. main.py 실행 | Run main.py:

python main.py

프롬프트에 따라 임포터 선택 및 CSV 파일 경로 입력

Follow the prompts to select an importer and enter the CSV file path

main.py 실행:

Run main.py:

python main.py

---

2. Select an importer as prompted:

Available importers:

1: av_gene_importer

2: av_patient_importer

3: av_tumour_importer

Choose an importer number:
Enter the CSV file path:

---
3. Check import progress and results:

Processed 1000 rows

Processed 2000 rows

...

Import completed: X rows

Total rows: Y

Successful: X

Failed: Z

---

# 코드 설명 | Code Explanation

config/db_config.py

데이터베이스 연결 설정을 관리합니다. 환경 변수를 사용하여 보안을 강화합니다.

Manages database connection settings. Uses environment variables for enhanced security.

python

import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_CONFIG = {

    'dbname': os.getenv(''),
    
    'user': os.getenv(''),
    
    'password': os.getenv(''),
    
    'host': os.getenv(''),
    
    'port': os.getenv('')
}


---

importers/base_importer.py

모든 임포터의 기본 클래스입니다. 데이터베이스 연결, 테이블 생성, 행 처리 등의 공통 기능을 제공합니다.

Base class for all importers. Provides common functionality for database connection, table creation, and row processing.

----

importers/av_gene_importer.py, av_patient_importer.py, av_tumour_importer.py, *_*_importer.py

각각 유전자, 환자, 종양 데이터를 처리하는 특화된 임포터 클래스입니다. BaseImporter를 상속받아 구현됩니다.

Specialized importer classes for processing gene, patient, and tumor data respectively. Implemented by inheriting from BaseImporter.

---

main.py

사용자 인터페이스를 제공하고 선택된 임포터를 실행합니다.

Provides user interface and executes the selected importer.

