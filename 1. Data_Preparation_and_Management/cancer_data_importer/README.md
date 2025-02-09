# Cancer Data Importer

## Project Overview

This project is a Python-based tool for importing and analyzing large-scale cancer datasets into a PostgreSQL database. It processes datasets over 200MB, including data from 1.7 million patients, aiming to identify significant patterns between tumor types and patient survivability.

# Key Features

- Import cancer datasets into PostgreSQL database
- Process patient, tumor, and gene data
- Data cleaning and validation
- Modular design for easy expansion

# Project Structure

```
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
```


# Installation and Setup
Clone the repository:

git clone https://github.com/your-username/cancer_data_importer.git

cd cancer_data_importer

# Install required packages:
pip install psycopg2 python-dotenv

# Configure database:
config/db_config.py 

Modify database connection information in config/db_config.py file.

# Usage

1. Run main.py:

```python main.py```

Follow the prompts to select an importer and enter the CSV file path

---
```
2. Select an importer as prompted:

Available importers:

1: av_gene_importer

2: av_patient_importer

3: av_tumour_importer

Choose an importer number:
Enter the CSV file path:
```
---
```
3. Check import progress and results:

Processed 1000 rows

Processed 2000 rows

...

Import completed: X rows

Total rows: Y

Successful: X

Failed: Z
```
---

# Code Explanation

config/db_config.py


Manages database connection settings. Uses environment variables for enhanced security.

```
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

```
---

__importers/base_importer.py__

Base class for all importers. Provides common functionality for database connection, table creation, and row processing.

----

**importers/av_gene_importer.py, av_patient_importer.py, av_tumour_importer.py, *_*_importer.py**

Specialized importer classes for processing gene, patient, and tumor data respectively. Implemented by inheriting from BaseImporter.

---

__main.py__

Provides user interface and executes the selected importer.

