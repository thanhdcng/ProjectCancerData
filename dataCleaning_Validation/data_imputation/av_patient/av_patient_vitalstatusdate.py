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


def calculate_patient_based_median_dates(engine):
    """
    For each patient, calculate the median dates from the SACT_REGIMEN table to update the VITALSTATUSDATE in AV_PATIENT.
    """
    query = """
    SELECT 
        ap.patientid,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY EXTRACT(EPOCH FROM sr.start_date_of_regimen)) AS median_start_date,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY EXTRACT(EPOCH FROM sr.date_decision_to_treat)) AS median_decision_date
    FROM av_patient ap
    LEFT JOIN sact_regimen sr ON ap.patientid = sr.encore_patient_id
    GROUP BY ap.patientid;
    """
    try:
        patient_medians = pd.read_sql(query, engine)
        return patient_medians
    except Exception as e:
        print(f"Error calculating patient-based median dates: {str(e)}")
        return None


def update_av_patient_vitalstatusdate(engine, patient_medians):
    try:
        with engine.connect() as connection:
            trans = connection.begin()
            try:
                for index, row in patient_medians.iterrows():
                    # Convert to standard Python types
                    median_date = float(row['median_start_date']) if pd.notna(row['median_start_date']) else float(row['median_decision_date'])
                    patient_id = int(row['patientid'])

                    if pd.notna(median_date):
                        connection.execute(text("""
                            UPDATE av_patient
                            SET vitalstatusdate = TO_TIMESTAMP(:median_date)
                            WHERE patientid = :patient_id
                              AND vitalstatusdate IS NULL;
                        """), {"median_date": median_date, "patient_id": patient_id})

                trans.commit()
                print("VITALSTATUSDATE updated successfully.")
            except Exception as e:
                trans.rollback()
                print(f"Error updating VITALSTATUSDATE: {str(e)}")
                raise
    except Exception as e:
        print(f"Error in transaction: {str(e)}")


def main():
    """
    Main function to update VITALSTATUSDATE for AV_PATIENT based on SACT_REGIMEN median dates.
    """
    engine = connect_to_database()
    if engine is None:
        return "Database connection failed."

    try:
        # Step 1: Calculate patient-based median dates
        patient_medians = calculate_patient_based_median_dates(engine)
        if patient_medians is None or patient_medians.empty:
            print("No patient-based median dates available.")
            return

        # Step 2: Update VITALSTATUSDATE
        update_av_patient_vitalstatusdate(engine, patient_medians)

    except Exception as e:
        print(f"Error during processing: {str(e)}")


if __name__ == "__main__":
    main()
