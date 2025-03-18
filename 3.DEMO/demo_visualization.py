import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from lifelines import KaplanMeierFitter

def load_data(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        exit()
    data = pd.read_csv(file_path)
    print("Data preview:")
    print(data.head())
    return data

def check_required_columns(data, required_columns):
    missing_columns = [col for col in required_columns if col not in data.columns]
    if missing_columns:
        print(f"Error: Missing required columns: {', '.join(missing_columns)}")
        exit()

def plot_top_n_regimens(data, n=20, output_dir="demo_output/regimen"):
    os.makedirs(output_dir, exist_ok=True)
    plt.figure(figsize=(13, 9))
    try:
        regimen_survival = data.groupby("mapped_regimen")["survival_rate"].mean()
        top_regimens = regimen_survival.sort_values(ascending=False).head(n)

        top_regimens = top_regimens.reset_index()
        top_regimens.index += 1
        top_regimens.rename(columns={"index": "Regimen"}, inplace=True)

        plt.bar(top_regimens.index, top_regimens["survival_rate"], color="skyblue")
        plt.title(f"Top {n} Regimens by Average Survival Rate")
        plt.xlabel("Regimen Number")
        plt.ylabel("Survival Rate (%)")
        plt.xticks(top_regimens.index, top_regimens.index, fontsize=10)
        plt.tight_layout()
        plt.savefig(f"{output_dir}/top_average_survival_rate_by_regimen_with_numbers.png")
        plt.show()

        mapping_table = top_regimens[["mapped_regimen"]]
        mapping_table["Regimen Number"] = top_regimens.index
        mapping_table = mapping_table.rename(columns={"mapped_regimen": "Regimen Name"})
        mapping_table.to_csv(f"{output_dir}/N_regimen_mapping_table.csv", index=False)
        print(f"Mapping table saved as '{output_dir}/N_regimen_mapping_table.csv'")
        print(mapping_table.to_string(index=False))
    except KeyError as e:
        print(f"Error in Visualization 1: {e}")

"""def plot_bottom_n_regimens(data, n=20, output_dir="demo_output/regimen"):
    os.makedirs(output_dir, exist_ok=True)
    plt.figure(figsize=(13, 9))
    try:
        # Group and sort data
        regimen_survival = data.groupby("mapped_regimen")["survival_rate"].mean()
        bottom_regimens = regimen_survival.sort_values(ascending=True).head(n).reset_index()
        bottom_regimens.index += 1

        # Plot bars
        plt.bar(bottom_regimens.index, bottom_regimens["survival_rate"], color="skyblue")
        plt.title(f"Bottom {n} Regimens by Average Survival Rate")
        plt.xlabel("Regimen Number")
        plt.ylabel("Survival Rate (%)")

        # Add annotations to bars
        for index, value in enumerate(bottom_regimens["survival_rate"]):
            plt.text(index + 1, value + 0.001, f"{value:.2f}%", ha='center', fontsize=9)

        # Set y-axis limits
        plt.ylim(-0.1, 0.1)  # Add some padding around zero
        plt.xticks(bottom_regimens.index, fontsize=10)
        plt.tight_layout()
        plt.savefig(f"{output_dir}/bottom_average_survival_rate_by_regimen_with_numbers.png")
        plt.show()

        # Save mapping table
        mapping_table = bottom_regimens.rename(columns={"mapped_regimen": "Regimen Name"})
        mapping_table["Regimen Number"] = bottom_regimens.index
        mapping_table.to_csv(f"{output_dir}/N_regimen_mapping_table.csv", index=False)
        print(f"Mapping table saved as '{output_dir}/N_regimen_mapping_table.csv'")
        print(mapping_table.to_string(index=False))

    except Exception as e:
        print(f"Error: {e}")
"""
def plot_all_regimens(data, output_dir="demo_output/regimen"):
    os.makedirs(output_dir, exist_ok=True)
    plt.figure(figsize=(200, 8))
    try:
        regimen_survival = data.groupby("mapped_regimen")["survival_rate"].mean()
        all_regimens = regimen_survival.sort_values(ascending=False)

        all_regimens = all_regimens.reset_index()
        all_regimens.index += 1
        all_regimens.rename(columns={"index": "Regimen"}, inplace=True)

        plt.bar(all_regimens.index, all_regimens["survival_rate"], color="skyblue")
        plt.title("All Regimens by Average Survival Rate")
        plt.xlabel("Regimen Number")
        plt.ylabel("Survival Rate (%)")
        plt.xticks(all_regimens.index, all_regimens.index, fontsize=10)
        plt.tight_layout()
        plt.savefig(f"{output_dir}/all_average_survival_rate_by_regimen_with_numbers.png")
        plt.show()

        mapping_table = all_regimens[["mapped_regimen"]]
        mapping_table["Regimen Number"] = all_regimens.index
        mapping_table = mapping_table.rename(columns={"mapped_regimen": "Regimen Name"})
        mapping_table.to_csv(f"{output_dir}/all_regimen_mapping_table.csv", index=False)
        print(f"Mapping table saved as '{output_dir}/all_regimen_mapping_table.csv'")
    except KeyError as e:
        print(f"Error in Visualization 3: {e}")

def plot_cancer_type_survival(data):
    if "site_icd10_o2_3char" in data.columns and "survival_rate" in data.columns:
        plt.figure(figsize=(20, 7))
        try:
            sns.boxplot(x="site_icd10_o2_3char", y="survival_rate", data=data, palette="Set3")
            plt.title("Survival Rate by Cancer Type")
            plt.xlabel("Cancer Type")
            plt.ylabel("Survival Rate (%)")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig("demo_output/survival_rate_by_cancer_type.png")
            plt.show()
        except Exception as e:
            print(f"Error in Visualization 4: {e}")
    else:
        print("Warning: Required columns for Visualization 4 are missing. Skipping.")

def plot_kaplan_meier(data):
    if "duration" in data.columns and "event" in data.columns:
        try:
            kmf = KaplanMeierFitter()
            plt.figure(figsize=(10, 6))
            kmf.fit(durations=data["duration"], event_observed=data["event"])
            kmf.plot_survival_function()
            plt.title("Kaplan-Meier Survival Analysis")
            plt.xlabel("Time (days)")
            plt.ylabel("Survival Probability")
            plt.tight_layout()
            plt.savefig("demo_output/kaplan_meier_survival_analysis.png")
            plt.show()
        except Exception as e:
            print(f"Error in Kaplan-Meier Analysis: {e}")
    else:
        print("Warning: Required columns for Kaplan-Meier analysis are missing. Skipping.")

def plot_regimen_changes(data):
    if "start_date_of_regimen" in data.columns:
        try:
            data["START_YEAR"] = pd.to_datetime(data["start_date_of_regimen"], errors='coerce').dt.year
            changes_by_year = data.groupby("START_YEAR")["mapped_regimen"].nunique()

            plt.figure(figsize=(10, 6))
            changes_by_year.plot(kind="line", marker="o", color="green")
            plt.title("Regimen Changes Over Years")
            plt.xlabel("Year")
            plt.ylabel("Number of Unique Regimens")
            plt.grid(True)
            plt.tight_layout()
            plt.savefig("demo_output/regimen_changes_over_years.png")
            plt.show()
        except Exception as e:
            print(f"Error in Regimen Changes Analysis: {e}")
    else:
        print("Warning: START_DATE_OF_REGIMEN column is missing. Skipping regimen changes analysis.")

def plot_tumor_stage_survival(data, output_dir="demo_output/"):
    """
    Plots survival rate by tumor stage using a boxplot.

    Parameters:
    - data (pd.DataFrame): The dataset containing 'stage_best' and 'survival_rate' columns.
    - save_path (str, optional): File path to save the plot. Default is None (plot not saved).
    """
    if "stage_best" in data.columns and "survival_rate" in data.columns:
        try:
            # Clean and normalize stage_best column
            data['stage_best'] = data['stage_best'].str.strip().fillna('Unknown')
            data['stage_best'] = data['stage_best'].replace({'': 'Unknown'})

            # Define initial custom order
            custom_order = [
                '0', '0A', '0IS', '1', '1A', '1A1', '1A2', '1B', '1B1', '1B2', '1C', '1E', '1S',
                '2', '2A', '2A1', '2A2', '2B', '2C', '2E', '2S', '3', '3A', '3B', '3C', '3E', '3S',
                '4', '4A', '4B', '4C', '4S', '5', '6', '?', 'U', 'X', 'Unknown'
            ]

            # Filter custom order to include only stages present in the dataset
            unique_values = data['stage_best'].unique()
            filtered_order = [stage for stage in custom_order if stage in unique_values]

            # Add missing stages to the filtered order
            missing_stages = [stage for stage in unique_values if stage not in filtered_order]
            if missing_stages:
                print(f"Adding missing stages to custom_order: {missing_stages}")
                filtered_order.extend(missing_stages)

            # Sort filtered order alphabetically for consistency
            filtered_order = sorted(filtered_order, key=lambda x: (custom_order.index(x) if x in custom_order else float('inf')))

            # Plot the data
            plt.figure(figsize=(16, 12))
            sns.boxplot(
                x='stage_best',
                y='survival_rate',
                data=data,
                order=filtered_order,
                palette='coolwarm'
            )
            plt.title("Survival Rate by Tumor Stage", fontsize=16)
            plt.xlabel("Tumor Stage", fontsize=14)
            plt.ylabel("Survival Rate (%)", fontsize=14)
            plt.xticks(rotation=45, fontsize=10)  # Rotate x-axis labels for better readability
            plt.tight_layout(rect=[0, 0.1, 1, 0.95])  # Adjust layout for better spacing

            # Save the plot if save_path is provided
            if output_dir:
                plt.savefig("demo_output/plot_tumor_stage_survival.png")
                print(f"Plot saved to {output_dir}")

            plt.show()
        except Exception as e:
            print(f"Error in Tumor Stage Analysis: {e}")
    else:
        print("Error: 'stage_best' or 'survival_rate' column is missing in the data.")

import matplotlib.pyplot as plt

def plot_gene_mutations(data):
    if "seq_var" in data.columns:
        try:
            # 유전자 변이에 따른 치료 변경 수 계산
            gene_changes = data.groupby("seq_var")["mapped_regimen"].nunique()

            # 상위 10개 유전자 변이 선택
            top_gene_changes = gene_changes.sort_values(ascending=False).head(10)

            # 막대 차트를 그리기 위한 데이터 준비
            x_labels = top_gene_changes.index
            y_values = top_gene_changes.values

            # 더 큰 figure size 설정
            plt.figure(figsize=(20, 8))

            # 막대 차트 생성
            plt.bar(x=range(len(x_labels)), height=y_values, color="orange", width=0.8)

            # 차트 제목과 축 레이블 추가
            plt.title("Top Gene Mutations Associated with Regimen Changes", pad=20)
            plt.xlabel("Gene Mutation", labelpad=10)
            plt.ylabel("Number of Regimen Changes")

            # x축 레이블 설정 (정확한 위치 배치)
            plt.xticks(ticks=range(len(x_labels)), labels=x_labels, rotation=30, ha='right')

            # 그래프 여백 확보
            plt.subplots_adjust(bottom=0.2)

            # 그래프 저장
            plt.savefig("demo_output/gene_mutations_regimen_changes_fixed.png",
                        bbox_inches='tight',
                        dpi=300)
            plt.show()

        except Exception as e:
            print(f"Error in Gene Mutation Analysis: {e}")
    else:
        print("Warning: seq_var column is missing. Skipping gene mutation analysis.")

def main():
    file_path = "demo_output/final_merged_data.csv" #changed the name of the  output file
    data = load_data(file_path)

    required_columns = ["mapped_regimen", "survival_rate", "site_icd10_o2_3char", "duration", "event"]
    check_required_columns(data, required_columns)

    # Generate visualizations and save data
    plot_top_n_regimens(data, n=20, output_dir="demo_output/regimen/top_regimens")
    #plot_bottom_n_regimens(data, n=20, output_dir="demo_output/regimen/bottom_regimens")
    plot_all_regimens(data, output_dir="demo_output/regimen/all_regimen")
    plot_cancer_type_survival(data)
    plot_kaplan_meier(data)
    plot_regimen_changes(data)
    plot_tumor_stage_survival(data)
    plot_gene_mutations(data)

if __name__ == "__main__":
    main()
