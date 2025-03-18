# Step 1: Connect to the database
import psycopg2

# Database connection parameters
db_params = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "Tan@123",
    "host": "localhost",
    "port": "5432"
}

# Establish connection
try:
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()
    print("Connected to the database.")
except Exception as e:
    print("Database connection failed:", e)
    raise

# Step 2: Verify SACT_CYCLE table

# 2.1 Check for NULLs in critical fields
cycle_null_checks = {
    "MERGED_REGIMEN_ID": "SELECT COUNT(*) FROM SACT_CYCLE WHERE MERGED_REGIMEN_ID IS NULL",
    "CYCLE_NUMBER": "SELECT COUNT(*) FROM SACT_CYCLE WHERE CYCLE_NUMBER IS NULL",
    "START_DATE_OF_CYCLE": "SELECT COUNT(*) FROM SACT_CYCLE WHERE START_DATE_OF_CYCLE IS NULL"
}

print("\nSACT_CYCLE Table Checks:")
for field, query in cycle_null_checks.items():
    cursor.execute(query)
    count = cursor.fetchone()[0]
    print(f"Nulls in {field}: {count}")

# Step 3: Verify SACT_OUTCOME table

# 3.1 Check for NULLs in critical fields
outcome_null_checks = {
    "MERGED_REGIMEN_ID": "SELECT COUNT(*) FROM SACT_OUTCOME WHERE MERGED_REGIMEN_ID IS NULL",
    "REGIMEN_OUTCOME_SUMMARY": "SELECT COUNT(*) FROM SACT_OUTCOME WHERE REGIMEN_OUTCOME_SUMMARY IS NULL"
}

print("\nSACT_OUTCOME Table Checks:")
for field, query in outcome_null_checks.items():
    cursor.execute(query)
    count = cursor.fetchone()[0]
    print(f"Nulls in {field}: {count}")

# Step 4: Verify SACT_DRUG_DETAIL table

# 4.1 Check for NULLs in critical fields
drug_detail_null_checks = {
    "MERGED_DRUG_DETAIL_ID": "SELECT COUNT(*) FROM SACT_DRUG_DETAIL WHERE MERGED_DRUG_DETAIL_ID IS NULL",
    "ACTUAL_DOSE_PER_ADMINISTRATION": "SELECT COUNT(*) FROM SACT_DRUG_DETAIL WHERE ACTUAL_DOSE_PER_ADMINISTRATION IS NULL",
    "ADMINISTRATION_DATE": "SELECT COUNT(*) FROM SACT_DRUG_DETAIL WHERE ADMINISTRATION_DATE IS NULL"
}

print("\nSACT_DRUG_DETAIL Table Checks:")
for field, query in drug_detail_null_checks.items():
    cursor.execute(query)
    count = cursor.fetchone()[0]
    print(f"Nulls in {field}: {count}")

# Step 5: Close the database connection
cursor.close()
connection.close()
print("Database connection closed.")
