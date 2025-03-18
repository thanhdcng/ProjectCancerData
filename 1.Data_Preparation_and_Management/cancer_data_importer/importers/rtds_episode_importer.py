from .base_importer import BaseImporter
from datetime import datetime
import logging
from psycopg2.extras import execute_values

class RtdsEpisodeImporter(BaseImporter):
    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Rtds_Episode (
                PATIENTID INT,
                RADIOTHERAPYEPISODEID INT,
                ATTENDID CHAR(30),
                APPTDATE DATE,
                LINKCODE CHAR(10),
                DECISIONTOTREATDATE DATE, 
                EARLIESTCLINAPPROPDATE DATE,
                RADIOTHERAPYPRIORITY CHAR(5),
                RADIOTHERAPYINTENT CHAR(5)
            )
        ''')
        self.conn.commit()
        print("Table Rtds_Episode created or already exists.")

    def process_row(self, row):
        try:
            # Convert integer fields
            integer_fields = ['PATIENTID', 'RADIOTHERAPYEPISODEID']
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
            date_fields = ['APPTDATE', 'DECISIONTOTREATDATE', 'EARLIESTCLINAPPROPDATE']
            for date_field in date_fields:
                if row.get(date_field) and row[date_field].strip():
                    try:
                        row[date_field] = datetime.strptime(row[date_field], '%Y-%m-%d').date()
                    except ValueError as ve:
                        logging.error(f"Date parsing error for field '{date_field}' in row: {row}. Error: {ve}")
                        row[date_field] = None
                else:
                    row[date_field] = None

            # Build and return a tuple of values in the same order as the table definition
            values = (
                row['PATIENTID'],
                row['RADIOTHERAPYEPISODEID'],
                row['ATTENDID'],
                row['APPTDATE'],
                row['LINKCODE'],
                row['DECISIONTOTREATDATE'],
                row['EARLIESTCLINAPPROPDATE'],
                row['RADIOTHERAPYPRIORITY'],
                row['RADIOTHERAPYINTENT']
            )
            return values

        except KeyError as ke:
            logging.error(f"Missing key {ke} in row: {row}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error in processing row: {row}. Error: {e}")
            return None

    def bulk_insert(self, data):
        """
        Performs a bulk insert using psycopg2's execute_values.
        `data` is a list of tuples produced by process_row.
        The SQL includes an ON CONFLICT clause to skip duplicate rows if needed.
        """
        sql = """
            INSERT INTO Rtds_Episode (
                PATIENTID,
                RADIOTHERAPYEPISODEID,
                ATTENDID,
                APPTDATE,
                LINKCODE,
                DECISIONTOTREATDATE, 
                EARLIESTCLINAPPROPDATE,
                RADIOTHERAPYPRIORITY,
                RADIOTHERAPYINTENT
            ) VALUES %s ON CONFLICT DO NOTHING
        """
        try:
            execute_values(self.cursor, sql, data, page_size=100)
            self.conn.commit()
        except Exception as e:
            logging.error(f"Bulk insert error: {e}")
            self.conn.rollback()
