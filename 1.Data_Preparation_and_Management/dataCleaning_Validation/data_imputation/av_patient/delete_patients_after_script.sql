'''
- Running the av_patient imputation script for the first time, the number of patients with
null vital status date in av_patient was 710.
-this query verifies that the patients with null vital status date in av_patient are not present in sact_regimen
which are euqal to 710 after running the script to impute the the vital status date again followed by running the 
script for sact_regimen imputation.
- which means those patients do not have any regimen in sact_regimen.
'''
SELECT ap.patientid
FROM av_patient ap
WHERE ap.vitalstatusdate IS NULL
  AND NOT EXISTS (
      SELECT 1
      FROM sact_regimen sr
      WHERE sr.encore_patient_id = ap.patientid
  );
'''Query to Delete the rows with null vital status date in av_patient that are not present in sact_regimen'''
DELETE FROM av_patient
WHERE patientid IN (
    SELECT ap.patientid
    FROM av_patient ap
    WHERE ap.vitalstatusdate IS NULL
      AND NOT EXISTS (
          SELECT 1
          FROM sact_regimen sr
          WHERE sr.encore_patient_id = ap.patientid
      )
);
'''