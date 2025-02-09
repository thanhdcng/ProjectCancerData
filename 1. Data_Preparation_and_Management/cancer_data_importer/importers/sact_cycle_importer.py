from .base_importer import BaseImporter
from datetime import datetime
import logging

class SactCycleImporter(BaseImporter):
    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS SACT_CYCLE (
                MERGED_REGIMEN_ID INTEGER,
                MERGED_CYCLE_ID INT,
                CYCLE_NUMBER INT,
                START_DATE_OF_CYCLE DATE,
                OPCS_PROCUREMENT_CODE CHAR(10),
                PERF_STATUS_START_OF_CYCLE CHAR(5)
                )''')

    def process_row(self, row):
        try:
            integer_fields = ['MERGED_REGIMEN_ID', 'MERGED_CYCLE_ID', 'CYCLE_NUMBER']
            for field in integer_fields:
                if row.get(field) == '':
                    row[field] = None
                elif row.get(field):
                    row[field] = int(row[field])

            date_fields = ['START_DATE_OF_CYCLE']

            for date_field in date_fields:
                if row.get(date_field) and row[date_field].strip():
                    try:
                        row[date_field] = datetime.strptime(row[date_field], '%Y-%m-%d').date()
                    except ValueError:
                        row[date_field] = None
                else:
                    row[date_field] = None


            sql = """INSERT INTO SACT_CYCLE (
                                MERGED_REGIMEN_ID,
                                MERGED_CYCLE_ID,
                                CYCLE_NUMBER,
                                START_DATE_OF_CYCLE,
                                OPCS_PROCUREMENT_CODE,
                                PERF_STATUS_START_OF_CYCLE
            )
                             VALUES (%s, %s, %s, %s, %s, %s)"""

            values = (
                row['MERGED_REGIMEN_ID'], row['MERGED_CYCLE_ID'], row['CYCLE_NUMBER'], row['START_DATE_OF_CYCLE'],
                row['OPCS_PROCUREMENT_CODE'], row['PERF_STATUS_START_OF_CYCLE']
            )
            return sql, values

        except KeyError as ke:
            print(f"Missing key in row: {ke}")
            return None

        except Exception as e:
            print(f"Unexpected error in processing row: {e}")
            return None
