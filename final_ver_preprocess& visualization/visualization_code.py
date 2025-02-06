import os
import pandas as pd

VIS_DATA_DIR = os.path.join(os.path.expanduser("~/Desktop/coding/final_ver_data/data"), "extracted_visualization_data")
os.makedirs(VIS_DATA_DIR, exist_ok=True)


def extract_visualization_data(df, analysis_type):
    """Extract data for specific visualization type"""
    try:
        extraction_profiles = {
            'success_rate': ['mapped_regimen', 'standardized_regimen', 'event_mapped', 'duration', 'intent_of_treatment', 'clinical_trial'],
            'cancer_type': ['site_icd10_o2_3char', 'mapped_regimen', 'standardized_regimen', 'event_mapped', 'duration'],
            'modifications': ['previous_regimen', 'mapped_regimen', 'standardized_regimen', 'modification_reason', 'event_mapped'],
            'survival': ['mapped_regimen', 'standardized_regimen', 'duration', 'event_mapped', 'age', 'stage_best'],
            'evolution': ['start_date_of_regimen', 'mapped_regimen', 'standardized_regimen', 'event_mapped', 'duration']
        }

        output_path = os.path.join(VIS_DATA_DIR, f"visualize_{analysis_type}.csv")
        df[extraction_profiles[analysis_type]].to_csv(output_path, index=False)
        print(f"✅ {os.path.basename(output_path)} created")
        return output_path

    except Exception as e:
        print(f"❌ Extraction failed: {str(e)}")
        return None
