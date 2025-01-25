UPDATE sact_cycle sc
SET start_date_of_cycle = sr.start_date_of_regimen
FROM sact_regimen sr
WHERE sc.merged_regimen_id = sr.merged_regimen_id
  AND sc.start_date_of_cycle IS NULL;
