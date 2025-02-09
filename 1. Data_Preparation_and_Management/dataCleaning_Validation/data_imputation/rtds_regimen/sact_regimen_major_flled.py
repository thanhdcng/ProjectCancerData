from sqlalchemy import create_engine, text
import pandas as pd


def connect_to_database():
    """
    Establish a connection to the PostgreSQL database using SQLAlchemy.
    """
    try:
        engine = create_engine('postgresql://postgres:wnghks12!!@localhost:5432/juhwanlee')
        return engine
    except Exception as e:
        print(f"Database connection error: {str(e)}")
        return None


def calculate_median_diff(engine):
    """
    Calculate the median difference in days between START_DATE_OF_REGIMEN and DATE_DECISION_TO_TREAT.
    """
    query = """
    SELECT EXTRACT(DAY FROM (start_date_of_regimen::timestamp - date_decision_to_treat::timestamp)) as diff_days
    FROM sact_regimen 
    WHERE date_decision_to_treat IS NOT NULL 
    AND start_date_of_regimen IS NOT NULL;
    """
    try:
        median_diff = pd.read_sql(query, engine)['diff_days'].median()
        return int(median_diff) if pd.notna(median_diff) else 7  # Default to 7 if no data is available
    except Exception as e:
        print(f"Error calculating median difference: {str(e)}")
        return 7


def calculate_mid_date(engine):
    """
    Calculate the mid date based on the date range of START_DATE_OF_REGIMEN.
    """
    query = """
    SELECT 
        MIN(start_date_of_regimen) as earliest_date,
        MAX(start_date_of_regimen) as latest_date
    FROM sact_regimen;
    """
    try:
        date_range = pd.read_sql(query, engine)
        if not date_range.empty:
            earliest_date = date_range['earliest_date'].iloc[0]
            latest_date = date_range['latest_date'].iloc[0]
            return earliest_date + (latest_date - earliest_date) / 2
        else:
            return pd.Timestamp.now().date()  # Default to today's date
    except Exception as e:
        print(f"Error calculating mid date: {str(e)}")
        return pd.Timestamp.now().date()


def calculate_group_based_medians(engine):
    """
    Calculate group-based medians for START_DATE_OF_REGIMEN and DATE_DECISION_TO_TREAT.
    """
    query = """
    SELECT 
        gender,
        age_group,
        MEDIAN(EXTRACT(DAY FROM (start_date_of_regimen::timestamp - date_decision_to_treat::timestamp))) as median_diff
    FROM (
        SELECT *,
            CASE 
                WHEN age <= 24 THEN '18-24'
                WHEN age <= 34 THEN '25-34'
                WHEN age <= 44 THEN '35-44'
                WHEN age <= 54 THEN '45-54'
                WHEN age <= 64 THEN '55-64'
                WHEN age <= 74 THEN '65-74'
                ELSE '75+'
            END AS age_group
        FROM sact_regimen sr
        LEFT JOIN av_patient ap ON sr.link_number = ap.patientid
        LEFT JOIN av_tumour at ON ap.patientid = at.patientid
        WHERE date_decision_to_treat IS NOT NULL 
        AND start_date_of_regimen IS NOT NULL
    ) sub
    GROUP BY gender, age_group;
    """
    try:
        group_medians = pd.read_sql(query, engine)
        return group_medians
    except Exception as e:
        print(f"Error calculating group-based medians: {str(e)}")
        return None


def update_missing_dates(engine, median_diff, mid_date):
    """
    Update the missing dates in the SACT_REGIMEN table for each case.
    """
    try:
        with engine.connect() as connection:
            trans = connection.begin()
            try:
                # Case 1: Only DATE_DECISION_TO_TREAT exists
                connection.execute(text(f"""
                    UPDATE sact_regimen
                    SET start_date_of_regimen = date_decision_to_treat + INTERVAL '{median_diff} days'
                    WHERE date_decision_to_treat IS NOT NULL 
                    AND start_date_of_regimen IS NULL;
                """))

                # Case 2: Only START_DATE_OF_REGIMEN exists
                connection.execute(text(f"""
                    UPDATE sact_regimen
                    SET date_decision_to_treat = start_date_of_regimen - INTERVAL '{median_diff} days'
                    WHERE date_decision_to_treat IS NULL 
                    AND start_date_of_regimen IS NOT NULL;
                """))

                # Case 3: Both dates are missing
                connection.execute(text(f"""
                    UPDATE sact_regimen
                    SET 
                        date_decision_to_treat = '{mid_date}'::date,
                        start_date_of_regimen = '{mid_date}'::date + INTERVAL '7 days'
                    WHERE date_decision_to_treat IS NULL 
                    AND start_date_of_regimen IS NULL;
                """))

                trans.commit()
                print("Dates updated successfully.")
            except Exception as e:
                trans.rollback()
                print(f"Error during date update: {str(e)}")
                raise
    except Exception as e:
        print(f"Error in transaction: {str(e)}")



def verify_results(engine):
    """
    Verify the results of the updates by checking the missing records count.
    """
    query = """
    SELECT 
        COUNT(*) as total_records,
        SUM(CASE WHEN date_decision_to_treat IS NULL THEN 1 ELSE 0 END) as missing_decision,
        SUM(CASE WHEN start_date_of_regimen IS NULL THEN 1 ELSE 0 END) as missing_start
    FROM sact_regimen;
    """
    try:
        results = pd.read_sql(query, engine)
        return results
    except Exception as e:
        print(f"Error verifying results: {str(e)}")
        return None


def impute_treatment_dates():
    """
    Main function to impute missing treatment dates in the SACT_REGIMEN table.
    """
    engine = connect_to_database()
    if engine is None:
        return "Database connection failed."

    try:
        # Step 1: Calculate median difference
        median_diff = calculate_median_diff(engine)

        # Step 2: Calculate mid date
        mid_date = calculate_mid_date(engine)

        # Step 3: Update missing dates
        update_missing_dates(engine, median_diff, mid_date)

        # Step 4: Verify results
        results = verify_results(engine)
        return results

    except Exception as e:
        print(f"Error during imputation: {str(e)}")
        return None


if __name__ == "__main__":
    results = impute_treatment_dates()
    if isinstance(results, pd.DataFrame):
        print("Verification Results:")
        print(results)
    else:
        print(results)
