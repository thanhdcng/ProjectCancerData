from .base_importer import BaseImporter
from datetime import datetime
import logging
from decimal import Decimal, InvalidOperation

class SactRegimenImporter(BaseImporter):
    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Sact_Regimen (
            ENCORE_PATIENT_ID INT,
            MERGED_REGIMEN_ID INT,
            HEIGHT_AT_START_OF_REGIMEN NUMERIC,
            WEIGHT_AT_START_OF_REGIMEN NUMERIC,
            INTENT_OF_TREATMENT CHAR(2),
            DATE_DECISION_TO_TREAT DATE,
            START_DATE_OF_REGIMEN DATE,
            MAPPED_REGIMEN CHAR(200),
            CLINICAL_TRIAL CHAR(10),
            CHEMO_RADIATION CHAR(5),
            BENCHMARK_GROUP CHAR(200),
            LINK_NUMBER INT
                )''')

    def process_row(self, row):
        try:
            integer_fields = ['ENCORE_PATIENT_ID', 'MERGED_REGIMEN_ID', 'LINK_NUMBER']
            for field in integer_fields:
                if row.get(field) == '':
                    row[field] = None
                elif row.get(field):
                    row[field] = int(row[field])

            date_fields = ['DATE_DECISION_TO_TREAT', 'START_DATE_OF_REGIMEN']
            for date_field in date_fields:
                if row.get(date_field) and row[date_field].strip():
                    try:
                        row[date_field] = datetime.strptime(row[date_field], '%Y-%m-%d').date()
                    except ValueError:
                        row[date_field] = None
                else:
                    row[date_field] = None

            numeric_fields = ['HEIGHT_AT_START_OF_REGIMEN', 'WEIGHT_AT_START_OF_REGIMEN']
            for field in numeric_fields:
                if row.get(field) is None or row.get(field) == '':
                    row[field] = None
                else:
                    try:
                        row[field] = Decimal(row[field])
                    except InvalidOperation:
                        row[field] = None

            sql = """INSERT INTO Sact_Regimen (ENCORE_PATIENT_ID,
                                                MERGED_REGIMEN_ID,
                                                HEIGHT_AT_START_OF_REGIMEN,
                                                WEIGHT_AT_START_OF_REGIMEN,
                                                INTENT_OF_TREATMENT,
                                                DATE_DECISION_TO_TREAT,
                                                START_DATE_OF_REGIMEN,
                                                MAPPED_REGIMEN,
                                                CLINICAL_TRIAL,
                                                CHEMO_RADIATION,
                                                BENCHMARK_GROUP,
                                                LINK_NUMBER)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

            values = (
                row['ENCORE_PATIENT_ID'], row['MERGED_REGIMEN_ID'], row['HEIGHT_AT_START_OF_REGIMEN'], row['WEIGHT_AT_START_OF_REGIMEN'],
                row['INTENT_OF_TREATMENT'], row['DATE_DECISION_TO_TREAT'], row['START_DATE_OF_REGIMEN'],
                row['MAPPED_REGIMEN'], row['CLINICAL_TRIAL'], row['CHEMO_RADIATION'],
                row['BENCHMARK_GROUP'], row['LINK_NUMBER']
            )
            return sql, values

        except KeyError as ke:
            logging.error(f"Missing key in row: {ke}")
            return None

        except Exception as e:
            logging.error(f"Unexpected error in processing row: {e}")
            return None
