from .base_importer import BaseImporter
from datetime import datetime
import logging
from psycopg2.extras import execute_values

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
            )
        ''')
        self.conn.commit()
        print("Table SACT_CYCLE created or already exists.")

    def process_row(self, row):
        try:
            # Convert integer fields
            integer_fields = ['MERGED_REGIMEN_ID', 'MERGED_CYCLE_ID', 'CYCLE_NUMBER']
            for field in integer_fields:
                if row.get(field) == '':
                    row[field] = None
                elif row.get(field):
                    row[field] = int(row[field])
            
            # Convert date fields
            date_fields = ['START_DATE_OF_CYCLE']
            for date_field in date_fields:
                if row.get(date_field) and row[date_field].strip():
                    try:
                        row[date_field] = datetime.strptime(row[date_field], '%Y-%m-%d').date()
                    except ValueError:
                        row[date_field] = None
                else:
                    row[date_field] = None

            # Build the tuple of values in the same order as in the table definition
            values = (
                row['MERGED_REGIMEN_ID'],
                row['MERGED_CYCLE_ID'],
                row['CYCLE_NUMBER'],
                row['START_DATE_OF_CYCLE'],
                row['OPCS_PROCUREMENT_CODE'],
                row['PERF_STATUS_START_OF_CYCLE']
            )
            return values

        except KeyError as ke:
            print(f"Missing key in row: {ke} | Row content: {row}")
            return None
        except Exception as e:
            print(f"Unexpected error in processing row: {row} | Error: {e}")
            return None

    def bulk_insert(self, data):
        """
        Performs a bulk insert using psycopg2's execute_values.
        `data` is a list of tuples produced by process_row.
        """
        sql = """
            INSERT INTO SACT_CYCLE (
                MERGED_REGIMEN_ID,
                MERGED_CYCLE_ID,
                CYCLE_NUMBER,
                START_DATE_OF_CYCLE,
                OPCS_PROCUREMENT_CODE,
                PERF_STATUS_START_OF_CYCLE
            ) VALUES %s ON CONFLICT DO NOTHING
        """
        try:
            execute_values(self.cursor, sql, data, page_size=100)
            self.conn.commit()
        except Exception as e:
            print(f"Bulk insert error: {e}")
            self.conn.rollback()
