from .base_importer import BaseImporter
from datetime import datetime
import logging
from decimal import Decimal, InvalidOperation

class RtdsExposureImporter(BaseImporter):
    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Rtds_Exposure (
                    PRESCRIPTIONID INT,
                    RADIOISOTOPE CHAR (30),
                    RADIOTHERAPYBEAMTYPE CHAR(30),
                    RADIOTHERAPYBEAMENERGY NUMERIC,
                    TIMEOFEXPOSURE TIME,
                    RADIOTHERAPYEPISODEID INTEGER,
                    ATTENDID CHAR(30),
                    APPTDATE DATE,
                    LINKCODE CHAR(30),
                    PATIENTID INT
                )''')

    def process_row(self, row):
        try:
            integer_fields = ['PRESCRIPTIONID', 'PATIENTID']
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

            time_fields = ['TIMEOFEXPOSURE']
            for time_field in time_fields:
                if row.get(time_field) and row[time_field].strip():
                    try:
                        row[time_field] = datetime.strptime(row[time_field], '%H:%M').time()
                    except ValueError:
                        row[time_field] = None
                else:
                    row[time_field] = None

            numeric_fields = ['RADIOTHERAPYBEAMENERGY']
            for field in numeric_fields:
                if row.get(field) is None or row.get(field) == '':
                    row[field] = None
                else:
                    try:
                        row[field] = Decimal(row[field])
                    except InvalidOperation:
                        row[field] = None


            sql = """INSERT INTO Rtds_Exposure (
                            PRESCRIPTIONID,
                            RADIOISOTOPE,
                            RADIOTHERAPYBEAMTYPE,
                            RADIOTHERAPYBEAMENERGY,
                            TIMEOFEXPOSURE,
                            RADIOTHERAPYEPISODEID,
                            ATTENDID,
                            APPTDATE,
                            LINKCODE,
                            PATIENTID
            )
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

            values = (
                row['PRESCRIPTIONID'], row['RADIOISOTOPE'], row['RADIOTHERAPYBEAMTYPE'], row['RADIOTHERAPYBEAMENERGY'],
                row['TIMEOFEXPOSURE'], row['RADIOTHERAPYEPISODEID'], row['ATTENDID'],
                row['APPTDATE'], row['LINKCODE'], row['PATIENTID']
            )
            return sql, values

        except KeyError as ke:
            logging.error(f"Missing key in row: {ke}")
            return None

        except Exception as e:
            logging.error(f"Unexpected error in processing row: {e}")
            return None
