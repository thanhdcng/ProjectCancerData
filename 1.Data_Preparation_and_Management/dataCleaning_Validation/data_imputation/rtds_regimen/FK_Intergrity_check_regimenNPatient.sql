'''The query identifies "orphan" rows in SACT_REGIMEN—rows whose ENCORE_PATIENT_ID does not match any PATIENTID in AV_Patient.
If the query returns an empty result, it suggests that the foreign key integrity is maintained.'''
SELECT sr.*
FROM SACT_REGIMEN sr
LEFT JOIN AV_Patient ap ON sr.ENCORE_PATIENT_ID = ap.PATIENTID
WHERE ap.PATIENTID IS NULL;
