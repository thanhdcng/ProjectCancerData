from .base_importer import BaseImporter
from datetime import datetime
import logging

#TUMOURID, Pseudonymised tumour ID, Integer, The format of this field in the Simulacrum is deliberately different from the format of pseudonymised tumour id for real individuals. For real individuals TUMOURID is different and stored in different formats.
#GENDER, Person stated gender, Character, Consult ZGENDER for lookup table. Data is identical to that in AV_PATIENT and the field is present for convenience.
#PATIENTID, Pseudonymised patient ID, Integer, The format of this field in the Simulacrum is deliberately different from the format of pseudonymised patient id for real individuals. For real individuals PATIENTID is different and stored in different formats.
#DIAGNOSISDATEBEST, Diagnosis date, Date, Internal registration rules require that this be linked to pathological confirmation where possible, which means it is possible to observe treatment prior to recorded diagnosis.
#SITE_ICD10_O2_3CHAR, Site of neoplasm (3-character ICD-10/O2 code original version), Character, Consult ZICD for lookup table
#SITE_ICD10_O2, Site of neoplasm (4-character ICD-10/O2 code original version), Character, Consult ZICD for lookup table
#SITE_ICD10R4_O2_3CHAR_FROM2013, Site of neoplasm (3-character ICD-10/O2 code revision 2010) for diagnoses from 2013 onwards, Character, Look up codes at https://icd.who.int/browse10/2010/en#/II
#SITE_ICD10R4_O2_FROM2013, Site of neoplasm (4-character ICD-10/O2 code revision 2010) for diagnoses from 2013 onwards, Character, Look up codes at https://icd.who.int/browse10/2010/en#/II
#SITE_ICDO3REV2011, Site of neoplasm (3-character code ICD-O-3 1st revision 2013), Character, Look up codes at https://apps.who.int/iris/bitstream/handle/10665/96612/9789241548496_eng.pdf
#SITE_ICDO3REV2011_3CHAR, Site of neoplasm (4-character ICD-O-3 1st revision 2013), Character, Look up codes at https://apps.who.int/iris/bitstream/handle/10665/96612/9789241548496_eng.pdf
#MORPH_ICD10_O2, Histology of the cancer in the ICD-10/O2 system, Character, Consult ZHISTOLOGYLOOKUP for the lookup table for morphologies
#MORPH_ICDO3REV2011, Histology of the cancer in the ICD-O-3 1st revision 2013, Character, Look up codes at https://apps.who.int/iris/bitstream/handle/10665/96612/9789241548496_eng.pdf
#BEHAVIOUR_ICD10_O2, Behaviour of the cancer in the ICD-10/O2 system, Character, Consult ZBEHAVIOUR for lookup table
#BEHAVIOUR_ICDO3REV2011, Behaviour of the cancer in the ICD-O-3 1st revision 2013, Character, Look up codes at https://apps.who.int/iris/bitstream/handle/10665/96612/9789241548496_eng.pdf
#T_BEST, T stage flagged by the registry as the 'best' T stage, Character
#N_BEST, N stage flagged by the registry as the 'best' N stage, Character
#M_BEST, M stage flagged by the registry as the 'best' M stage, Character
#STAGE_BEST, Best 'registry' stage at diagnosis of the tumour, Character, Consult ZSTAGE for lookup table
#GRADE, Grade of tumour, Character, Consult ZGRADE for lookup table
#AGE, Age at diagnosis, Integer, Age is recorded in years
#CREG_CODE, Cancer registry catchment area code the patient was resident in when the tumour was diagnosed, Character, The CREG_CODE variable has been obfuscated so that its values do not correspond to real CREG code values
#STAGE_BEST_SYSTEM, System used to record best registry stage at diagnosis, Character
#LATERALITY, Laterality, Character, Consult ZLATERALITY for lookup table
#SCREENINGSTATUSFULL_CODE, Full detailed screening status of the tumour, Character, These are only available for certain primary sites
#ER_STATUS, Oestrogen receptor status of the tumour, Character, These are only available for certain primary sites
#PR_STATUS, Progesterone receptor status of the tumour, Character, These are only available for certain primary sites
#HER2_STATUS, HER2 status of the tumour, Character, These are only available for certain primary sites
#QUINTILE_2019, Measure of deprivation: the population-weighted quintile of income-level deprivation at small area level (LSAO), Character
#DATE_FIRST_SURGERY, Date of first surgical event linked to this tumour recorded in the Cancer Registration treatment table, Date, This is a derived field from the Cancer Registration treatment table
#CANCERCAREPLANINTENT, Intent of treatment as recorded in COSD Cancer Care Plan, Character, Consult ZCANCERCAREPLANINTENT for the lookup table
#PERFORMANCESTATUS, Performance status recorded at diagnosis, Character
#CHRL_TOT_27_03, Total Charlson comorbididy score, Integer, A combination of HES-derived and Registry-derived Charlson scores
#COMORBIDITIES_27_03, Charlson groups making up the total Charlson score for a lookback of 27 to 3 months, Character, Consult ZCOMORBIDITIES to look up the different Charlson comorbidity groups and their respective Charlson scores
#GLEASON_PRIMARY, Gleason primary pattern, Character, These are only available for certain primary sites
#GLEASON_SECONDARY, Gleason secondary pattern, Character, These are only available for certain primary sites
#GLEASON_TERTIARY, Gleason tertiary pattern, Character, These are only available for certain primary sites
#GLEASON_COMBINED, Combined Gleason primary and secondary scores, Integer, These are only available for certain primary sites

class AvTumourImporter(BaseImporter):
    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS AV_TUMOUR (
            TUMOURID INTEGER PRIMARY KEY,
            GENDER CHAR(30),
            PATIENTID INTEGER, 
            DIAGNOSISDATEBEST DATE,
            SITE_ICD10_O2_3CHAR CHAR(3),
            SITE_ICD10_O2 CHAR(30),
            SITE_ICD10R4_O2_3CHAR_FROM2013 CHAR(3),
            SITE_ICD10R4_O2_FROM2013 CHAR(30),
            SITE_ICDO3REV2011 CHAR(30),
            SITE_ICDO3REV2011_3CHAR CHAR(3),
            MORPH_ICD10_O2 CHAR(30),
            MORPH_ICDO3REV2011 CHAR(30),
            BEHAVIOUR_ICD10_O2 CHAR(30),
            BEHAVIOUR_ICDO3REV2011 CHAR(30),
            T_BEST CHAR(30),
            N_BEST CHAR(30),
            M_BEST CHAR(30),
            STAGE_BEST CHAR(30),
            GRADE CHAR(30),
            AGE INTEGER,
            CREG_CODE CHAR(30),
            STAGE_BEST_SYSTEM CHAR(30),
            LATERALITY CHAR(30),
            SCREENINGSTATUSFULL_CODE CHAR(30),
            ER_STATUS CHAR(30),
            PR_STATUS CHAR(30),
            HER2_STATUS CHAR(30),
            QUINTILE_2019 CHAR(30),
            DATE_FIRST_SURGERY DATE,
            CANCERCAREPLANINTENT CHAR(30),
            PERFORMANCESTATUS CHAR(30),
            CHRL_TOT_27_03 CHAR(30),
            COMORBIDITIES_27_03 CHAR(60),
            GLEASON_PRIMARY CHAR(30),
            GLEASON_SECONDARY CHAR(30),
            GLEASON_TERTIARY CHAR(30),
            GLEASON_COMBINED INTEGER
                )''')

    def process_row(self, row):
        try:
            integer_fields = ['TUMOURID', 'PATIENTID', 'AGE', 'GLEASON_COMBINED']
            for field in integer_fields:
                if row.get(field) == '':
                    row[field] = None
                elif row.get(field):
                    row[field] = int(row[field])

            if row.get('DIAGNOSISDATEBEST'):
             try:
                row['DIAGNOSISDATEBEST'] = datetime.strptime(row['DIAGNOSISDATEBEST'], '%Y-%m-%d').date()
             except ValueError as ve:
                print(f"Date parsing error for DIAGNOSISDATEBEST: {ve}")
                return None

            if row.get('DATE_FIRST_SURGERY') and row['DATE_FIRST_SURGERY'].strip():
                try:
                    row['DATE_FIRST_SURGERY'] = datetime.strptime(row['DATE_FIRST_SURGERY'], '%Y-%m-%d').date()
                except ValueError:
                    row['DATE_FIRST_SURGERY'] = None
            else:
                row['DATE_FIRST_SURGERY'] = None


            sql = """INSERT INTO AV_TUMOUR (TUMOURID, GENDER, PATIENTID, DIAGNOSISDATEBEST, 
                             SITE_ICD10_O2_3CHAR, SITE_ICD10_O2, SITE_ICD10R4_O2_3CHAR_FROM2013, 
                             SITE_ICD10R4_O2_FROM2013, SITE_ICDO3REV2011, SITE_ICDO3REV2011_3CHAR,
                             MORPH_ICD10_O2, MORPH_ICDO3REV2011, BEHAVIOUR_ICD10_O2, BEHAVIOUR_ICDO3REV2011,
                             T_BEST, N_BEST, M_BEST, STAGE_BEST, GRADE, AGE, CREG_CODE, STAGE_BEST_SYSTEM,
                             LATERALITY, SCREENINGSTATUSFULL_CODE, ER_STATUS, PR_STATUS, HER2_STATUS,
                             QUINTILE_2019, DATE_FIRST_SURGERY, CANCERCAREPLANINTENT, PERFORMANCESTATUS,
                             CHRL_TOT_27_03, COMORBIDITIES_27_03, GLEASON_PRIMARY, GLEASON_SECONDARY,
                             GLEASON_TERTIARY, GLEASON_COMBINED)
                             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                                     %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                                     %s, %s, %s)"""

            values = (
                row['TUMOURID'], row['GENDER'], row['PATIENTID'], row['DIAGNOSISDATEBEST'],
                row['SITE_ICD10_O2_3CHAR'], row['SITE_ICD10_O2'], row['SITE_ICD10R4_O2_3CHAR_FROM2013'],
                row['SITE_ICD10R4_O2_FROM2013'], row['SITE_ICDO3REV2011'], row['SITE_ICDO3REV2011_3CHAR'],
                row['MORPH_ICD10_O2'], row['MORPH_ICDO3REV2011'], row['BEHAVIOUR_ICD10_O2'],
                row['BEHAVIOUR_ICDO3REV2011'], row.get('T_BEST'), row.get('N_BEST'), row.get('M_BEST'),
                row['STAGE_BEST'], row['GRADE'], row['AGE'], row['CREG_CODE'], row.get('STAGE_BEST_SYSTEM'),
                row['LATERALITY'], row.get('SCREENINGSTATUSFULL_CODE'), row.get('ER_STATUS'),
                row.get('PR_STATUS'), row.get('HER2_STATUS'), row['QUINTILE_2019'],
                row.get('DATE_FIRST_SURGERY'), row.get('CANCERCAREPLANINTENT'),
                row.get('PERFORMANCESTATUS'), row['CHRL_TOT_27_03'], row.get('COMORBIDITIES_27_03'),
                row.get('GLEASON_PRIMARY'), row.get('GLEASON_SECONDARY'), row.get('GLEASON_TERTIARY'),
                row.get('GLEASON_COMBINED')
            )
            return sql, values

        except KeyError as ke:
            print(f"Missing key in row: {ke}")
            return None

        except Exception as e:
            print(f"Unexpected error in processing row: {e}")
            return None
