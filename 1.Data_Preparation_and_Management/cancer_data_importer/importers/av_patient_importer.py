import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime
from .base_importer import BaseImporter

    # PATIENTID, Pseudonymised patient ID, Int, The format of this field in the Simulacrum is deliberately different from the format of pseudonymised patient id for real individuals. For real individuals PATIENTID is different and stored in different formats.
    # GENDER,Person Stated gender, Char, Look up codes in ZGENDER
    # ZGENDER - 'CODE' - '1','2','9','X'
    # ETHNICITY, Ethnicity, Char, Look up codes in ZETHNICITY
    # ZETHICITY - 'CODE' - '0','8','A','B','C','C2','C3','CA','CB','CC','CD','CE','CF','CG','CH','CJ',
#                 'CK','CL','CM','CN','CP','CQ','CR','CS','CT','CU','CV','CW','CX','CY','D',
#                 'E','F','G','GA','GB','GC','GD','GE','GF','H','J','K','L','LA','LB','LC',
#                 'LD','LE','LF','LG','LH','LJ','LK','M','N','P','PA','PB','PC','PD','PE',
#                 'R','S','SA','SB','SC','SD','SE','X','Z'
    # DEATHCAUSECODE_1A, As provided with death notification, Char, Codes are in ICD-10 format, and may be a comma-separated list
    # DEATHCAUSECODE_1B, As provided with death notification, Char, Codes are in ICD-10 format, and may be a comma-separated list
    # DEATHCAUSECODE_1C, As provided with death notification, Char, Codes are in ICD-10 format, and may be a comma-separated list
    # DEATHCAUSECODE_2, As provided with death notification, Char, Codes are in ICD-10 format, and may be a comma-separated list
    # DEATHCAUSECODE_UNDERLYING, As provided with death notification, Char, Codes are in ICD-10 format, and may be a comma-separated list
    # DEATHLOCATIONCODE, Code of the location where the patient died, Char, Look up codes in ZDEATHLOCATION
    # ZDEATHLOCAITON - 'CODE' - '1','2','3','4','4077','4087','4097','4107','4117','4127','4137','5','X'
    # VITALSTATUS, vital status of the patient, Char, Look up codes in ZVITALSTATUS
    # ZVITALSTATUS - 'CODE' - 'A','A1','A2','A3','D','D1','D2','D3','D4','D5',
#                             'X1','X2','X3','X4','X5','X','I'
    # VITALSTATUSDATE, date of vital status, Date, If the patient has embarked or died, this is the corresponding date. If the patient is alive, this is the last date of follow-up.
    # LINKUMBER, substitute for HNS number in the real data(coded as NHSNUMBER), INT, The format and name of this field in the Simulacrum is deliberately different from the format of NHS numbers for real individuals.  For real individuals NHSNUMBER is different and stored in different formats.
    
class AvPatientImporter(BaseImporter):
    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS AV_PATIENT (
                PATIENTID INTEGER PRIMARY KEY NOT NULL,
                GENDER CHAR(1) NOT NULL,
                ETHNICITY CHAR(2),
                DEATHCAUSECODE_1A VARCHAR(20),
                DEATHCAUSECODE_1B VARCHAR(20),
                DEATHCAUSECODE_1C VARCHAR(20),
                DEATHCAUSECODE_2 VARCHAR(20),
                DEATHCAUSECODE_UNDERLYING VARCHAR(15),
                DEATHLOCATIONCODE CHAR(4),
                VITALSTATUS CHAR(2) NOT NULL,
                VITALSTATUSDATE DATE,
                LINKNUMBER INTEGER NOT NULL UNIQUE
            )
        ''')
        self.conn.commit()
        print("Table AV_PATIENT created or already exists.")

    def process_row(self, row):
        """
        Return a tuple in the correct order for the AV_PATIENT table.
        If any required fields are missing or invalid, return None.
        """
        try:
            required = ['PATIENTID', 'GENDER', 'VITALSTATUS', 'LINKNUMBER']
            if not all(row.get(f) for f in required):
                return None

            # Parse date
            if row.get('VITALSTATUSDATE'):
                try:
                    row['VITALSTATUSDATE'] = datetime.strptime(
                        row['VITALSTATUSDATE'], '%Y-%m-%d'
                    ).date()
                except ValueError:
                    row['VITALSTATUSDATE'] = None
            else:
                row['VITALSTATUSDATE'] = None

            return (
                int(row['PATIENTID']),
                row['GENDER'],
                row.get('ETHNICITY'),
                row.get('DEATHCAUSECODE_1A'),
                row.get('DEATHCAUSECODE_1B'),
                row.get('DEATHCAUSECODE_1C'),
                row.get('DEATHCAUSECODE_2'),
                row.get('DEATHCAUSECODE_UNDERLYING'),
                row.get('DEATHLOCATIONCODE'),
                row['VITALSTATUS'],
                row['VITALSTATUSDATE'],
                int(row['LINKNUMBER'])
            )
        except Exception:
            return None

    def bulk_insert(self, data):
        """
        data: List of tuples, each tuple is a row for AV_PATIENT.
        Use execute_values for efficient bulk insertion.
        """
        sql = """
            INSERT INTO AV_PATIENT (
                PATIENTID, GENDER, ETHNICITY, DEATHCAUSECODE_1A, DEATHCAUSECODE_1B,
                DEATHCAUSECODE_1C, DEATHCAUSECODE_2, DEATHCAUSECODE_UNDERLYING,
                DEATHLOCATIONCODE, VITALSTATUS, VITALSTATUSDATE, LINKNUMBER
            ) VALUES %s
        """
        try:
            execute_values(self.cursor, sql, data, page_size=100)
            self.conn.commit()
        except Exception as e:
            print("Bulk insert error:", e)
            self.conn.rollback()
