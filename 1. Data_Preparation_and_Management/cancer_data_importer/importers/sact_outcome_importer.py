from .base_importer import BaseImporter
from datetime import datetime
import logging

class SactOutcomeImporter(BaseImporter):
    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Sact_Outcome (
            MERGED_REGIMEN_ID INT PRIMARY KEY,
            DATE_OF_FINAL_TREATMENT DATE,
            REGIMEN_MOD_DOSE_REDUCTION CHAR(1),
            REGIMEN_MOD_TIME_DELAY CHAR(1),
            REGIMEN_MOD_STOPPED_EARLY CHAR(1),
            REGIMEN_OUTCOME_SUMMARY CHAR(2)
                )''')

    def process_row(self, row):
        try:
            integer_fields = ['MERGED_REGIMEN_ID']
            for field in integer_fields:
                if row.get(field) == '':
                    row[field] = None
                elif row.get(field):
                    row[field] = int(row[field])

            date_fields = ['DATE_OF_FINAL_TREATMENT']

            for date_field in date_fields:
                if row.get(date_field) and row[date_field].strip():
                    try:
                        row[date_field] = datetime.strptime(row[date_field], '%Y-%m-%d').date()
                    except ValueError:
                        row[date_field] = None
                else:
                    row[date_field] = None

            sql = """INSERT INTO Sact_Outcome (MERGED_REGIMEN_ID, DATE_OF_FINAL_TREATMENT, REGIMEN_MOD_DOSE_REDUCTION,
                                            REGIMEN_MOD_TIME_DELAY, REGIMEN_MOD_STOPPED_EARLY, REGIMEN_OUTCOME_SUMMARY)
                     VALUES (%s, %s, %s, %s, %s, %s)"""

            values = (
                row['MERGED_REGIMEN_ID'], row['DATE_OF_FINAL_TREATMENT'], row['REGIMEN_MOD_DOSE_REDUCTION'], row['REGIMEN_MOD_TIME_DELAY'],
                row['REGIMEN_MOD_STOPPED_EARLY'], row['REGIMEN_OUTCOME_SUMMARY'])
            return sql, values


        except KeyError as ke:
            print(f"Missing key in row: {ke}")
            return None

        except Exception as e:
            print(f"Unexpected error in processing row: {e}")
            return None
