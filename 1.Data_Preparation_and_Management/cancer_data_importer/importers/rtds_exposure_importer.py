from .base_importer import BaseImporter
from datetime import datetime
import logging
from decimal import Decimal, InvalidOperation
from psycopg2.extras import execute_values

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
            )
        ''')
        self.conn.commit()
        print("Table Rtds_Exposure created or already exists.")

    def process_row(self, row):
        try:
            # Convert integer fields
            integer_fields = ['PRESCRIPTIONID', 'PATIENTID']
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
            date_fields = ['APPTDATE']
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
                if row.get(time_field) and row[time_field].strip():
                    try:
                        row[time_field] = datetime.strptime(row[time_field], '%H:%M').time()
                    except ValueError:
                        row[time_field] = None
                else:
                    row[time_field] = None

            # Convert numeric fields
            numeric_fields = ['RADIOTHERAPYBEAMENERGY']
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
                row['PRESCRIPTIONID'],
                row['RADIOISOTOPE'],
                row['RADIOTHERAPYBEAMTYPE'],
                row['RADIOTHERAPYBEAMENERGY'],
                row['TIMEOFEXPOSURE'],
                row['RADIOTHERAPYEPISODEID'],
                row['ATTENDID'],
                row['APPTDATE'],
                row['LINKCODE'],
                row['PATIENTID']
            )
            return values

        except KeyError as ke:
            logging.error(f"Missing key {ke} in row: {row}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error in processing row: {row} | Error: {e}")
            return None

    def bulk_insert(self, data):
        """
        Performs a bulk insert using psycopg2's execute_values.
        `data` is a list of tuples produced by process_row.
        """
        sql = """
            INSERT INTO Rtds_Exposure (
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
            ) VALUES %s ON CONFLICT DO NOTHING
        """
        try:
            execute_values(self.cursor, sql, data, page_size=100)
            self.conn.commit()
        except Exception as e:
            logging.error(f"Bulk insert error: {e}")
            self.conn.rollback()
