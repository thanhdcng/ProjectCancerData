from .base_importer import BaseImporter
from datetime import datetime
import logging
from decimal import Decimal, InvalidOperation

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
                    RTTREATMENTREGION NUMERIC,
                    RTTREATMENTANATOMICALSITE CHAR(10),
                    RADIOTHERAPYEPISODEID CHAR(10),
                    LINKCODE CHAR(5),
                    ATTENDID CHAR(30),
                    APPTDATE DATE
                )''')

    def process_row(self, row):
        try:
            integer_fields = ['PATIENTID', 'PRESCRIPTIONID', 'RTTREATMENTMODALITY']
            for field in integer_fields:
                if row.get(field) == '':
                    row[field] = None
                elif row.get(field):
                    row[field] = int(row[field])

            date_fields = ['APPTDATE']
            for date_field in date_fields:
                if row.get(date_field) and row[date_field].strip():
                    try:
                        row[date_field] = datetime.strptime(row[date_field], '%Y-%m-%d').date()
                    except ValueError:
                        row[date_field] = None
                else:
                    row[date_field] = None

            numeric_fields = ['PRESCRIBEDFRACTIONS', 'RTACTUALDOSE', 'RTACTUALFRACTIONS', 'RTTREATMENTREGION']
            for field in numeric_fields:
                if row.get(field) is None or row.get(field) == '':
                    row[field] = None
                else:
                    try:
                        row[field] = Decimal(row[field])
                    except InvalidOperation:
                        row[field] = None


            sql = """INSERT INTO Rtds_Prescription (
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
            )
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

            values = (
                row['PATIENTID'], row['PRESCRIPTIONID'], row['RTTREATMENTMODALITY'], row['RTPRESCRIBEDDOSE'],
                row['PRESCRIBEDFRACTIONS'], row['RTACTUALDOSE'], row['RTACTUALFRACTIONS'],
                row['RTTREATMENTREGION'], row['RTTREATMENTANATOMICALSITE'],
                row['RADIOTHERAPYEPISODEID'], row['ATTENDID'], row['APPTDATE'],
                row['LINKCODE']
            )
            return sql, values

        except KeyError as ke:
            logging.error(f"Missing key in row: {ke}")
            return None

        except Exception as e:
            logging.error(f"Unexpected error in processing row: {e}")
            return None
