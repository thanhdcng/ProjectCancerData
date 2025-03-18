from .base_importer import BaseImporter
from datetime import datetime
import logging
from decimal import Decimal, InvalidOperation
from psycopg2.extras import execute_values

class SactDrugDetailImporter(BaseImporter):
    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Sact_Drug_Detail (
                MERGED_DRUG_DETAIL_ID INTEGER PRIMARY KEY,
                MERGED_CYCLE_ID INTEGER,
                ACTUAL_DOSE_PER_ADMINISTRATION NUMERIC,
                OPCS_DELIVERY_CODE CHAR(100),
                ADMINISTRATION_ROUTE CHAR(100),
                ADMINISTRATION_DATE DATE,
                DRUG_GROUP CHAR(100)
            )
        ''')
        self.conn.commit()
        print("Table Sact_Drug_Detail created or already exists.")

    def process_row(self, row):
        try:
            # Convert integer fields
            integer_fields = ['MERGED_DRUG_DETAIL_ID', 'MERGED_CYCLE_ID']
            for field in integer_fields:
                if row.get(field) == '':
                    row[field] = None
                elif row.get(field):
                    try:
                        row[field] = int(row[field])
                    except Exception as e:
                        logging.error(f"Error converting field '{field}' to int in row: {row}. Error: {e}")
                        row[field] = None

            # Convert date fields
            date_fields = ['ADMINISTRATION_DATE']
            for date_field in date_fields:
                if row.get(date_field) and row[date_field].strip():
                    try:
                        row[date_field] = datetime.strptime(row[date_field], '%Y-%m-%d').date()
                    except ValueError:
                        row[date_field] = None
                else:
                    row[date_field] = None

            # Convert numeric fields
            numeric_fields = ['ACTUAL_DOSE_PER_ADMINISTRATION']
            for field in numeric_fields:
                if row.get(field) is None or row.get(field) == '':
                    row[field] = None
                else:
                    try:
                        row[field] = Decimal(row[field])
                    except InvalidOperation:
                        logging.error(f"Error converting field '{field}' to Decimal in row: {row}.")
                        row[field] = None

            # Build and return the tuple of values (order must match table definition)
            values = (
                row['MERGED_DRUG_DETAIL_ID'],
                row['MERGED_CYCLE_ID'],
                row['ACTUAL_DOSE_PER_ADMINISTRATION'],
                row['OPCS_DELIVERY_CODE'],
                row['ADMINISTRATION_ROUTE'],
                row['ADMINISTRATION_DATE'],
                row['DRUG_GROUP']
            )
            return values

        except KeyError as ke:
            logging.error(f"Missing key {ke} in row: {row}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error in processing row: {row}. Error: {e}")
            return None

    def bulk_insert(self, data):
        """
        Performs a bulk insert using psycopg2's execute_values.
        `data` is a list of tuples produced by process_row.
        """
        sql = """
            INSERT INTO Sact_Drug_Detail (
                MERGED_DRUG_DETAIL_ID,
                MERGED_CYCLE_ID,
                ACTUAL_DOSE_PER_ADMINISTRATION,
                OPCS_DELIVERY_CODE,
                ADMINISTRATION_ROUTE,
                ADMINISTRATION_DATE,
                DRUG_GROUP
            ) VALUES %s ON CONFLICT DO NOTHING
        """
        try:
            execute_values(self.cursor, sql, data, page_size=100)
            self.conn.commit()
        except Exception as e:
            logging.error(f"Bulk insert error: {e}")
            self.conn.rollback()
