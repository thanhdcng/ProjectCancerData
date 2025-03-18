from .base_importer import BaseImporter
from datetime import datetime
import logging
from decimal import Decimal, InvalidOperation
from psycopg2.extras import execute_values

class RtdsPrescriptionImporter(BaseImporter):
    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Rtds_Prescription (
                PATIENTID INT,
                PRESCRIPTIONID INT,
                RTTREATMENTMODALITY INT,
                RTPRESCRIBEDDOSE CHAR(5),
                PRESCRIBEDFRACTIONS NUMERIC,
                RTACTUALDOSE NUMERIC,
                RTACTUALFRACTIONS NUMERIC,
                RTTREATMENTREGION CHAR(5),
                RTTREATMENTANATOMICALSITE CHAR(10),
                RADIOTHERAPYEPISODEID CHAR(10),
                ATTENDID CHAR(30),
                APPTDATE DATE,
                LINKCODE CHAR(5)
            )
        ''')
        self.conn.commit()
        print("Table Rtds_Prescription created or already exists.")

    def process_row(self, row):
        try:
            integer_fields = ['PATIENTID', 'PRESCRIPTIONID', 'RTTREATMENTMODALITY']
            for field in integer_fields:
                if row.get(field) == '':
                    row[field] = None
                elif row.get(field):
                    try:
                        row[field] = int(row[field])
                    except Exception as e:
                        logging.error(f"Error converting field '{field}' to int in row: {row}. Error: {e}")
                        row[field] = None

            date_fields = ['APPTDATE']
            for date_field in date_fields:
                if row.get(date_field) and row[date_field].strip():
                    try:
                        row[date_field] = datetime.strptime(row[date_field], '%Y-%m-%d').date()
                    except ValueError:
                        row[date_field] = None
                else:
                    row[date_field] = None

            numeric_fields = ['PRESCRIBEDFRACTIONS', 'RTACTUALDOSE', 'RTACTUALFRACTIONS']
            for field in numeric_fields:
                if row.get(field) is None or row.get(field) == '':
                    row[field] = None
                else:
                    try:
                        row[field] = Decimal(row[field])
                    except InvalidOperation:
                        logging.error(f"Error converting field '{field}' to Decimal in row: {row}.")
                        row[field] = None

            # RTTREATMENTREGION is treated as text (string), not numeric.
            values = (
                row['PATIENTID'],
                row['PRESCRIPTIONID'],
                row['RTTREATMENTMODALITY'],
                row['RTPRESCRIBEDDOSE'],
                row['PRESCRIBEDFRACTIONS'],
                row['RTACTUALDOSE'],
                row['RTACTUALFRACTIONS'],
                row.get('RTTREATMENTREGION'),  # Do not convert; leave as is (e.g., "P")
                row['RTTREATMENTANATOMICALSITE'],
                row['RADIOTHERAPYEPISODEID'],
                row['ATTENDID'],
                row['APPTDATE'],
                row['LINKCODE']
            )
            return values

        except KeyError as ke:
            logging.error(f"Missing key in row: {ke}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error in processing row: {e}")
            return None

    def bulk_insert(self, data):
        sql = """
            INSERT INTO Rtds_Prescription (
                PATIENTID,
                PRESCRIPTIONID,
                RTTREATMENTMODALITY,
                RTPRESCRIBEDDOSE,
                PRESCRIBEDFRACTIONS,
                RTACTUALDOSE,
                RTACTUALFRACTIONS,
                RTTREATMENTREGION,
                RTTREATMENTANATOMICALSITE,
                RADIOTHERAPYEPISODEID,
                ATTENDID,
                APPTDATE,
                LINKCODE
            ) VALUES %s ON CONFLICT DO NOTHING
        """
        try:
            execute_values(self.cursor, sql, data, page_size=100)
            self.conn.commit()
        except Exception as e:
            logging.error(f"Bulk insert error: {e}")
            self.conn.rollback()
