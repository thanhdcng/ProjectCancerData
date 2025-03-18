'''this query finds orphan rows in sact_regimen—rows that do not have a matching patient in av_patient
(i.e., rows where ENCORE_PATIENT_ID does not appear in av_patient.patientid).
If the result set is empty, it means every ENCORE_PATIENT_ID in sact_regimen is present in av_patient.'''
SELECT sr.*
FROM SACT_REGIMEN sr
LEFT JOIN AV_Patient ap ON sr.ENCORE_PATIENT_ID = ap.PATIENTID
WHERE ap.PATIENTID IS NULL;
