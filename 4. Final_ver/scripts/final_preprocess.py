import os
import pandas as pd
import re
from collections import defaultdict


class RegimenNormalizer:
    def __init__(self):
        self.protocol_patterns = self._load_protocol_database()
        self.component_map = self._load_component_map()
        self.category_map = self._load_category_map()

    def _load_protocol_database(self):
        """Load standard treatment protocols from clinical databases"""
        return {
            r'\bFOLFOX\b': ('Chemotherapy', '5-FU + Oxaliplatin + Leucovorin'),
            r'\bXELOX\b': ('Chemotherapy', 'Capecitabine + Oxaliplatin'),
            r'\bAC-T\b': ('Chemotherapy', 'Doxorubicin/Cyclophosphamide → Paclitaxel'),
            r'\bCHOP\b': ('Chemotherapy', 'Cyclophosphamide + Doxorubicin + Vincristine + Prednisone'),
            r'\bFOLFIRI\b': ('Chemotherapy', '5-FU + Irinotecan + Leucovorin'),
            r'\bTPF\b': ('Chemotherapy', 'Docetaxel + Cisplatin + 5-FU')
        }

    def _load_component_map(self):
        """Map drug components to standardized names"""
        return {
            'cape': 'Capecitabine', 'carbo': 'Carboplatin', 'cis': 'Cisplatin',
            'oxali': 'Oxaliplatin', '5fu': '5-FU', 'gem': 'Gemcitabine',
            'taxol': 'Paclitaxel', 'docet': 'Docetaxel', 'trastu': 'Trastuzumab',
            'bev': 'Bevacizumab', 'pembro': 'Pembrolizumab'
        }

    def _load_category_map(self):
        """Categorize treatment types"""
        return {
            'chemo': 'Chemotherapy',
            'targeted': 'Targeted Therapy',
            'immuno': 'Immunotherapy',
            'radiation': 'Radiotherapy'
        }

    def normalize(self, regimen):
        """Main normalization pipeline"""
        original = str(regimen)
        standardized = self._basic_normalization(original)
        standardized = self._handle_protocols(standardized)
        standardized = self._parse_components(standardized)
        return self._categorize_regimen(standardized)

    def _basic_normalization(self, text):
        """Initial text cleaning and standardization"""
        text = re.sub(r'\s+', ' ', text.lower().strip())
        text = re.sub(r'\d+[mgmcg]\S*', '', text)  # Remove dosage information
        text = re.sub(r'\b(inj|iv|sc)\b', '', text)  # Remove administration routes
        return text

    def _handle_protocols(self, text):
        """Identify and replace standard treatment protocols"""
        for pattern, (category, replacement) in self.protocol_patterns.items():
            if re.search(pattern, text, flags=re.IGNORECASE):
                return f"{category}: {replacement}"
        return text

    def _parse_components(self, text):
        """Deconstruct combination therapies into components"""
        components = []
        for part in re.split(r'[\+\-/]', text):
            part = part.strip()
            for abbr, full in self.component_map.items():
                if re.match(rf'\b{abbr}', part):
                    components.append(full)
                    break
            else:
                components.append(part.title())
        return '+'.join(sorted(set(components)))

    def _categorize_regimen(self, text):
        """Apply hierarchical treatment categorization"""
        for key, category in self.category_map.items():
            if re.search(rf'\b{key}', text, flags=re.IGNORECASE):
                return f"{category}::{text}"
        return f"Other::{text}"

def save_normalization_sample(sample_df, output_file):
    """Save normalization examples to separate CSV"""
    sample_path = os.path.join(
        os.path.dirname(output_file),
        "normalization_sample.csv"
    )
    sample_df.to_csv(sample_path, index=False)
    print(f"💾 Normalization examples saved to: {sample_path}")
    print("🔍 Sample Preview:")
    print(sample_df.head())

def load_data_with_optimized_memory(file_path):
    """
    Load CSV with optimized memory usage while handling mixed-type issues.
    """
    dtype_mapping = {
        "patient_id": "str",
        "link_number": "str",
        "seq_var": "Int16",
        "age": "Int8",
        "duration": "float32",
        "previous_regimen": "category",
        "modification_reason": "category"
    }

    try:
        df = pd.read_csv(file_path, dtype=dtype_mapping, low_memory=False)
    except ValueError as e:
        print(f"⚠️ Dtype conflict detected: {e}")
        print("🔹 Attempting to auto-fix dtype issues...")

        df = pd.read_csv(file_path, low_memory=False)  # Reload without dtype
        for col in df.columns:
            # Remove leading/trailing spaces
            df[col] = df[col].astype(str).str.strip()

            # Convert columns with mixed types
            if df[col].str.match(r"^-?\d+(\.\d+)?$").all():
                df[col] = pd.to_numeric(df[col], errors='coerce')

    # ✅ Drop the specified columns before processing
    columns_to_drop = ["weight_at_start_of_regimen", "height_at_start_of_regimen"]
    df.drop(columns=[col for col in columns_to_drop if col in df.columns], axis=1, inplace=True)

    return df

def load_and_merge_data(df_chunk, raw_data_path):
    """
    Load raw data and merge it with the main dataset in chunks.
    """
    if not os.path.exists(raw_data_path):
        print(f"⚠️ Raw data file {raw_data_path} not found. Using initial dataset only.")
        return df_chunk

    df_raw = load_data_with_optimized_memory(raw_data_path)

    common_keys = list(set(df_chunk.columns) & set(df_raw.columns))
    if not common_keys:
        print("❌ No common columns found for merging. Proceeding without merging raw data.")
        return df_chunk

    # Merge only the necessary columns to avoid duplication
    df_chunk = df_chunk.merge(df_raw[common_keys], on=common_keys, how='left')
    return df_chunk

def required_new_columns(df_chunk, output_file):
    """
    Generate new derived columns while ensuring all computed fields are included.
    """
    print("🔹 Processing new derived columns...")

    date_columns = ["vitalstatusdate", "start_date_of_regimen", "last_followup_date"]
    for col in date_columns:
        if col in df_chunk.columns:
            df_chunk[col] = pd.to_datetime(df_chunk[col], errors="coerce")

    # Compute 'duration'
    df_chunk["duration"] = None
    if "vitalstatusdate" in df_chunk.columns and "start_date_of_regimen" in df_chunk.columns:
        df_chunk["duration"] = (df_chunk["vitalstatusdate"] - df_chunk["start_date_of_regimen"]).dt.days
        df_chunk.loc[df_chunk["duration"] < 0, "duration"] = None

    if "vitalstatus" in df_chunk.columns:
        event_lookup = {
            "A": 0, "A1": 0, "A2": 0, "A3": 0,  # Alive cases
            "D": 1, "D1": 1, "D2": 1, "D3": 1, "D4": 1, "D5": 1,  # Dead cases
            "X1": -1, "X2": -1, "X3": -1, "X4": -1, "X5": -1, "X": -1,  # Lost to follow-up / Unknown
            "I": -1  # Aliased off
        }

        # 🔹 Handle whitespace and case inconsistencies
        df_chunk["vitalstatus"] = df_chunk["vitalstatus"].astype(str).str.strip().str.upper()

        # 🔹 Apply mapping
        df_chunk["event_mapped"] = df_chunk["vitalstatus"].map(event_lookup)

        # 🔹 Check mapping results
        print(df_chunk[["vitalstatus", "event_mapped"]].value_counts())

        # 🔹 Check if there are any NaN values
        num_unknown = df_chunk["event_mapped"].isna().sum()
        if num_unknown > 0:
            print(f"⚠️ Warning: {num_unknown} rows have an unknown vitalstatus value.")

        # 🔹 Replace NaN values with -1
        df_chunk["event_mapped"] = df_chunk["event_mapped"].fillna(-1)

    # Compute 'previous_regimen'
    df_chunk["previous_regimen"] = None

    # Ensure that both 'mapped_regimen' and 'patientid' exist in the data
    if "mapped_regimen" in df_chunk.columns and "patientid" in df_chunk.columns:
        # Group by patientid and shift the 'mapped_regimen' for each patient to get the previous regimen
        df_chunk["previous_regimen"] = df_chunk.groupby("patientid")["mapped_regimen"].shift(1)

        # Modify modification_reason logic to handle 'Y' and 'y'
    df_chunk["modification_reason"] = 0

    if "regimen_mod_dose_reduction" in df_chunk.columns:
        # Standardize casing and strip any extra spaces
        df_chunk["regimen_mod_dose_reduction"] = df_chunk["regimen_mod_dose_reduction"].astype(
            str).str.strip().str.upper()
        df_chunk.loc[df_chunk["regimen_mod_dose_reduction"].isin(['Y']), "modification_reason"] += 1

    if "regimen_mod_time_delay" in df_chunk.columns:
        # Standardize casing and strip any extra spaces
        df_chunk["regimen_mod_time_delay"] = df_chunk["regimen_mod_time_delay"].astype(str).str.strip().str.upper()
        df_chunk.loc[df_chunk["regimen_mod_time_delay"].isin(['Y']), "modification_reason"] += 2

    if "regimen_mod_stopped_early" in df_chunk.columns:
        # Standardize casing and strip any extra spaces
        df_chunk["regimen_mod_stopped_early"] = df_chunk["regimen_mod_stopped_early"].astype(
            str).str.strip().str.upper()
        df_chunk.loc[df_chunk["regimen_mod_stopped_early"].isin(['Y']), "modification_reason"] += 4

    # Debugging: Print out some sample data to see if modification_reason is updated
    print("🔍 Checking modification_reason counts:")
    print(df_chunk["modification_reason"].value_counts())

    # Add standardized regimen column
    if "mapped_regimen" in df_chunk.columns:
        normalizer = RegimenNormalizer()
        df_chunk["standardized_regimen"] = df_chunk["mapped_regimen"].apply(normalizer.normalize)
        print("✅ Standardized regimen column added")

        # Save normalization sample
        save_normalization_sample(
            df_chunk[["mapped_regimen", "standardized_regimen"]].head(),
            output_file
        )

    # Maintain computed fields list
    computed_fields = ["duration", "event_mapped", "previous_regimen",
                       "modification_reason", "standardized_regimen"]

    # Return required columns
    merge_keys = ["patientid", "link_number"]
    valid_keys = [key for key in merge_keys if key in df_chunk.columns]
    return df_chunk[valid_keys + computed_fields]

def execute_final_preprocessing(input_file, raw_data_file, output_file):
    """
    Process large datasets in chunks, merge new computed columns, and automatically remove duplicate columns.
    """
    print("🔹 Running final data preprocessing in chunks...")

    chunksize = 100000  # Process in smaller chunks

    output_temp_file = output_file + ".tmp"
    if os.path.exists(output_temp_file):
        os.remove(output_temp_file)

    for chunk in pd.read_csv(input_file, chunksize=chunksize, low_memory=False):
        chunk = load_and_merge_data(chunk, raw_data_file)
        df_new_columns = required_new_columns(chunk, output_file)

        # ✅ Identify a valid merge key
        possible_keys = ["patientid", "link_number"]
        merge_key = next((key for key in possible_keys if key in chunk.columns and key in df_new_columns.columns), None)

        if not merge_key:
            raise ValueError("❌ No valid key found for merging. Check available keys.")

        # ✅ Merge and remove duplicate columns (_x and _y) by using a custom logic
        chunk = chunk.merge(df_new_columns, on=merge_key, how="left")

        # ✅ Remove duplicate columns by checking suffixes and retaining one of them
        for col in chunk.columns:
            if col.endswith("_x"):
                base_col = col[:-2]
                if base_col in chunk.columns:
                    chunk.drop(columns=[col], inplace=True)
                else:
                    chunk.rename(columns={col: base_col}, inplace=True)
            elif col.endswith("_y"):
                base_col = col[:-2]
                if base_col in chunk.columns:
                    chunk.drop(columns=[col], inplace=True)
                else:
                    chunk.rename(columns={col: base_col}, inplace=True)

        # ✅ Drop unnecessary columns before saving
        columns_to_drop = ["weight_at_start_of_regimen", "height_at_start_of_regimen"]
        chunk.drop(columns=[col for col in columns_to_drop if col in chunk.columns], axis=1, inplace=True)

        chunk.to_csv(output_temp_file, mode='a', index=False, header=not os.path.exists(output_temp_file))

    os.rename(output_temp_file, output_file)
    print(f"✅ Final merged dataset saved to {output_file}")
