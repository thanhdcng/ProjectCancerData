'''the query identifies "orphan" SACT_REGIMEN records,
those for which the patient ID does not appear in the AV_Tumour table.'''
SELECT sr.*
FROM SACT_REGIMEN sr
LEFT JOIN AV_Tumour at ON sr.ENCORE_PATIENT_ID = at.PATIENTID
WHERE at.PATIENTID IS NULL;
