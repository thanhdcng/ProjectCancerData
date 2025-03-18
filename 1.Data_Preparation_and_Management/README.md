# Cancer Data Processing Documentation

## 1. cancer_data_importer
This module is responsible for importing locally stored CSV files into a PostgreSQL database. It ensures efficient data ingestion and maintains data integrity throughout the process.

### Features:
- Reads raw cancer-related CSV datasets.
- Establishes a connection to PostgreSQL.
- Imports data into predefined tables.
- Handles errors related to missing or malformed records.

### Technologies Used:
- Python (pandas, psycopg2)
- PostgreSQL

## 2. dataCleaning_Validation
This module processes and validates the imported cancer dataset using Python and SQL queries. It ensures data quality and consistency before further analysis.

### Features:
- Cleans and formats raw data.
- Identifies and resolves missing values.
- Validates key constraints and relationships.
- Generates reports on data inconsistencies.

### Technologies Used:
- Python (pandas, NumPy, SQLAlchemy)
- PostgreSQL

## 3. DATA RELATED TO REGIMENS CLEANING AND VALIDATION.pdf
This document provides an overview of issues related to data cleaning and validation for cancer treatment regimens. It outlines detected anomalies and proposes corrective actions to ensure data accuracy and reliability.

### Key Sections:
- Data integrity issues and detection methods.
- Proposed solutions for identified problems.
- Best practices for maintaining clean and validated data.
- Recommendations for future data management improvements.

## 4. ER diagram] Cancer_Data.pdf
This document contains the Entity-Relationship (ER) diagram representing the database schema of the imported cancer dataset. It provides a visual representation of table structures, relationships, and key constraints.

### Key Elements:
- Entity relationships between patients, tumors, treatments, and outcomes.
- Primary and foreign key mappings.
- Structural overview of database normalization.

### Usage:
- Reference for database design and query optimization.
- Helps in understanding data dependencies for analytical tasks.

---
