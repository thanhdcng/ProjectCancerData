from .base_importer import BaseImporter
from datetime import datetime
import logging
from decimal import Decimal, InvalidOperation

class RtdsCombinedImporter(BaseImporter):
    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Rtds_Combined (
                PATIENTID INT,
                PRESCRIPTIONID INT,
                RADIOTHERAPYEPISODEID INT,
                ATTENDID CHAR(30),
                APPTDATE DATE,
                LINKCODE CHAR(30),
                RTTREATMENTMODALITY CHAR(30),
                RTPRESCRIBEDDOSE NUMERIC,
                PRESCRIBEDFRACTIONS NUMERIC,
                RTACTUALDOSE NUMERIC,
                RTACTUALFRACTIONS NUMERIC, 
                RTTREATMENTREGION CHAR(30),
                RTTREATMENTANATOMICALSITE CHAR(30),
                DECISIONTOTREATDATE DATE,
                EARLIESTCLINAPPROPDATE DATE,
                RADIOTHERAPYPRIORITY CHAR(30),
                RADIOTHERAPYINTENT CHAR(30),
                RADIOISOTOPE CHAR(30),
                RADIOTHERAPYBEAMTYPE CHAR(30),
                RADIOTHERAPYBEAMENERGY NUMERIC,
                TIMEOFEXPOSURE TIME
            )
        ''')
        self.conn.commit()
        print("Table Rtds_Combined created or already exists.")

    def process_row(self, row):
        try:
            # Convert integer fields
            integer_fields = ['PATIENTID', 'PRESCRIPTIONID', 'RADIOTHERAPYEPISODEID']
            for field in integer_fields:
                if row.get(field) == '':
                    row[field] = None
                elif row.get(field):
                    row[field] = int(row[field])
            
            # Convert date fields
            date_fields = ['APPTDATE', 'DECISIONTOTREATDATE', 'EARLIESTCLINAPPROPDATE']
            for date_field in date_fields:
                if row.get(date_field) and row[date_field].strip():
                    try:
                        row[date_field] = datetime.strptime(row[date_field], '%Y-%m-%d').date()
                    except ValueError:
                        row[date_field] = None
                else:
                    row[date_field] = None

            # Convert time fields
            time_fields = ['TIMEOFEXPOSURE']
            for time_field in time_fields:
                if row.get(time_field) and row[time_field].strip() and row[time_field] != 'NA':
                    try:
                        row[time_field] = datetime.strptime(row[time_field], '%H:%M').time()
                    except ValueError:
                        row[time_field] = None
                else:
                    row[time_field] = None

            # Convert numeric fields
            numeric_fields = ['RTPRESCRIBEDDOSE', 'PRESCRIBEDFRACTIONS', 'RTACTUALDOSE', 'RTACTUALFRACTIONS', 'RADIOTHERAPYBEAMENERGY']
            for field in numeric_fields:
                if row.get(field) is None or row.get(field) == '' or row.get(field) == 'NA':
                    row[field] = None
                else:
                    try:
                        row[field] = Decimal(row[field])
                    except InvalidOperation:
                        row[field] = None

            # Build the tuple of values in the same order as the table columns
            values = (
                row['PATIENTID'],
                row['PRESCRIPTIONID'],
                row['RADIOTHERAPYEPISODEID'],
                row['ATTENDID'],
                row['APPTDATE'],
                row['LINKCODE'],
                row['RTTREATMENTMODALITY'],
                row['RTPRESCRIBEDDOSE'],
                row['PRESCRIBEDFRACTIONS'],
                row['RTACTUALDOSE'],
                row['RTACTUALFRACTIONS'],
                row['RTTREATMENTREGION'],
                row['RTTREATMENTANATOMICALSITE'],
                row['DECISIONTOTREATDATE'],
                row['EARLIESTCLINAPPROPDATE'],
                row['RADIOTHERAPYPRIORITY'],
                row['RADIOTHERAPYINTENT'],
                row['RADIOISOTOPE'],
                row['RADIOTHERAPYBEAMTYPE'],
                row['RADIOTHERAPYBEAMENERGY'],
                row['TIMEOFEXPOSURE']
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
            INSERT INTO Rtds_Combined (
                PATIENTID,
                PRESCRIPTIONID,
                RADIOTHERAPYEPISODEID,
                ATTENDID,
                APPTDATE,
                LINKCODE,
                RTTREATMENTMODALITY,
                RTPRESCRIBEDDOSE,
                PRESCRIBEDFRACTIONS,
                RTACTUALDOSE,
                RTACTUALFRACTIONS,
                RTTREATMENTREGION,
                RTTREATMENTANATOMICALSITE,
                DECISIONTOTREATDATE, 
                EARLIESTCLINAPPROPDATE,
                RADIOTHERAPYPRIORITY,
                RADIOTHERAPYINTENT,
                RADIOISOTOPE,
                RADIOTHERAPYBEAMTYPE,
                RADIOTHERAPYBEAMENERGY,
                TIMEOFEXPOSURE
            ) VALUES %s
        """
        try:
            from psycopg2.extras import execute_values
            execute_values(self.cursor, sql, data, page_size=100)
            self.conn.commit()
        except Exception as e:
            logging.error(f"Bulk insert error: {e}")
            self.conn.rollback()
