from .base_importer import BaseImporter
from datetime import datetime
import logging
from decimal import Decimal, InvalidOperation

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
                )''')

    def process_row(self, row):
        try:
            integer_fields = ['MERGED_DRUG_DETAIL_ID', 'MERGED_CYCLE_ID']
            for field in integer_fields:
                if row.get(field) == '':
                    row[field] = None
                elif row.get(field):
                    row[field] = int(row[field])

            date_fields = ['ADMINISTRATION_DATE']
            for date_field in date_fields:
                if row.get(date_field) and row[date_field].strip():
                    try:
                        row[date_field] = datetime.strptime(row[date_field], '%Y-%m-%d').date()
                    except ValueError:
                        row[date_field] = None
                else:
                    row[date_field] = None

            numeric_fields = ['ACTUAL_DOSE_PER_ADMINISTRATION']
            for field in numeric_fields:
                if row.get(field) is None or row.get(field) == '':
                    row[field] = None
                else:
                    try:
                        row[field] = Decimal(row[field])
                    except InvalidOperation:
                        row[field] = None

            sql = """INSERT INTO Sact_Drug_Detail (MERGED_DRUG_DETAIL_ID,
                                                    MERGED_CYCLE_ID,
                                                    ACTUAL_DOSE_PER_ADMINISTRATION,
                                                    OPCS_DELIVERY_CODE,
                                                    ADMINISTRATION_ROUTE,
                                                    ADMINISTRATION_DATE,
                                                    DRUG_GROUP)
                     VALUES (%s, %s, %s, %s, %s, %s, %s)"""

            values = (
                row['MERGED_DRUG_DETAIL_ID'], row['MERGED_CYCLE_ID'], row['ACTUAL_DOSE_PER_ADMINISTRATION'], row['OPCS_DELIVERY_CODE'],
                row['ADMINISTRATION_ROUTE'], row['ADMINISTRATION_DATE'], row['DRUG_GROUP'],
            )
            return sql, values

        except KeyError as ke:
            logging.error(f"Missing key in row: {ke}")
            return None

        except Exception as e:
            logging.error(f"Unexpected error in processing row: {e}")
            return None
