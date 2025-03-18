import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from lifelines import KaplanMeierFitter

BASE_DIR = "C:/Users/Black/Desktop/internship/ProjectCancerData/4.Final_ver/data" # Change this to your directory
OUTPUT_DIR = os.path.join(BASE_DIR, "output", "visualizations")
os.makedirs(OUTPUT_DIR, exist_ok=True)

success_rate_path = os.path.join(BASE_DIR, "extracted_visualization_data","visualize_success_rate.csv")
cancer_type_path = os.path.join(BASE_DIR, "visualize_cancer_type.csv")
modifications_path = os.path.join(BASE_DIR, "visualize_modifications.csv")
survival_path = os.path.join(BASE_DIR, "visualize_survival.csv")
evolution_path = os.path.join(BASE_DIR, "visualize_evolution.csv")

def load_data(file_path):
    """Load and preprocess dataset"""
    try:
        df = pd.read_csv(file_path, dtype={
            'event_mapped': 'category',
            'standardized_regimen': 'category',
            'site_icd10_o2_3char': 'category'
        })
        df['event_mapped'] = df['event_mapped'].map({
            "1": 'death', "0": 'survival', "-1": 'unknown'
        }).fillna('unknown')
        df['start_date_of_regimen'] = pd.to_datetime(df['start_date_of_regimen'], errors='coerce')
        return df
    except Exception as e:
        print(f"❌ Data load error: {str(e)}")
        return None

def save_visualization(fig, chart_type, filename):
    """Save visualization files"""
    try:
        chart_dir = os.path.join(OUTPUT_DIR, chart_type)
        os.makedirs(chart_dir, exist_ok=True)
        full_path = os.path.join(chart_dir, filename)

        if isinstance(fig, plt.Figure):
            fig.savefig(full_path, bbox_inches='tight', dpi=300)
        elif isinstance(fig, go.Figure):
            fig.write_html(full_path)

        print(f"✅ Saved: {filename}" if os.path.exists(full_path) else f"❌ Save failed: {filename}")

    except Exception as e:
        print(f"❌ Save error: {str(e)}")

# Function to visualize treatment success rate analysis
def visualize_treatment_success_rate(data_path):
    """Visualize treatment success rate analysis"""
    try:
        data_path = success_rate_path
        df = pd.read_csv(data_path)

        success_rates = df.groupby('standardized_regimen')['event_mapped'].apply(
            lambda x: (x == 'survival').mean() * 100
        ).reset_index(name='success_rate')

        plt.figure(figsize=(14, 8))
        ax = sns.barplot( # changed hue to None
            x='success_rate',
            y='standardized_regimen',
            data=success_rates.sort_values('success_rate', ascending=False),
            palette='viridis',
            hue=None,
            legend=False
        )
        plt.title("Treatment Success Rate by Regimen", pad=20)
        plt.xlabel("Success Rate (%)", labelpad=15)
        plt.ylabel("Treatment Regimen", labelpad=15)
        plt.xlim(0, 100)

        # Annotate the bar plot with success rate values
        for p in ax.patches:
            ax.text(p.get_width() + 1,
                    p.get_y() + p.get_height() / 2,
                    f'{p.get_width():.1f}%',
                    ha='left',
                    va='center')

        # Save visualization after plotting
        save_visualization(plt.gcf(), "success_rates", "treatment_success_rate.png") #  plt.gcf() (get current figure) to retrieve the current Figure.
        plt.close()

    except Exception as e:
        print(f"❌ Visualization error: {str(e)}")

# Function to visualize cancer type success rate
def visualize_cancer_type_success_rate(data_path):
    """Visualize success rate by cancer type"""
    try:
        df = pd.read_csv(data_path)

        heatmap_data = df.pivot_table(
            index='site_icd10_o2_3char',
            columns='standardized_regimen',
            values='event_mapped',
            aggfunc=lambda x: (x == 'survival').mean()
        )
        plt.figure(figsize=(16, 12))
        ax = sns.heatmap(
            heatmap_data * 100,
            annot=True,
            fmt=".1f",
            cmap="YlGnBu",
            linewidths=.5,
            annot_kws={"size": 8}
        )
        plt.title("Survival Rate by Cancer Type and Treatment Regimen (%)", pad=20)
        plt.xlabel("Treatment Regimen", labelpad=15)
        plt.ylabel("Cancer Type", labelpad=15)
        ax.xaxis.tick_top()
        plt.xticks(rotation=90)
        save_visualization(plt.gcf(), "cancer_type", "cancer_type_success_heatmap.png") #  plt.gcf() (get current figure) to retrieve the current Figure.
        plt.close()
    except Exception as e:
        print(f"❌ Visualization error: {str(e)}")

# Function to visualize treatment modification patterns
def visualize_treatment_modifications(data_path):
    """Visualize treatment modification patterns"""
    try:
        df = pd.read_csv(data_path)

        regimen_counts = df['previous_regimen'].value_counts()
        top_regimens = regimen_counts[regimen_counts >= 10].index.tolist()
        filtered_df = df[df['previous_regimen'].isin(top_regimens)]
        links = filtered_df.groupby(['previous_regimen', 'standardized_regimen']).size().reset_index(name='count')
        all_regimens = pd.unique(links[['previous_regimen', 'standardized_regimen']].values.ravel('K'))
        nodes = [{'label': str(regimen)} for regimen in all_regimens]
        source_indices = [all_regimens.tolist().index(x) for x in links['previous_regimen']]
        target_indices = [all_regimens.tolist().index(x) for x in links['standardized_regimen']]
        fig = go.Figure(go.Sankey(
            node=dict(
                pad=25,
                thickness=20,
                line=dict(color="black", width=0.8),
                label=[node['label'] for node in nodes],
                color="lightblue"
            ),
            link=dict(
                source=source_indices,
                target=target_indices,
                value=links['count'],
                hovertemplate='%{source.label} → %{target.label}Count: %{value}'
            )
        ))
        fig.update_layout(
            title_text="Treatment Regimen Modification Patterns",
            font=dict(size=10),
            height=800,
            width=1200
        )
        save_visualization(fig, "modification_patterns", "treatment_modification_sankey.html")
    except Exception as e:
        print(f"❌ Visualization error: {str(e)}")

# Function to visualize Kaplan-Meier Survival Curve Visualization
def visualize_kaplan_meier(data_path):
    """Visualize survival rates using Kaplan-Meier curve"""
    df = pd.read_csv(data_path)
    try:
        kmf = KaplanMeierFitter()

        # Filter data for event_mapped != 'unknown'
        survival_data = df[df['event_mapped'] != 'unknown'].copy()
        # Drop rows where 'duration' is NaN
        survival_data = survival_data.dropna(subset=['duration'])

        plt.figure(figsize=(10, 6))
        ax = plt.gca()

        for regimen in survival_data['standardized_regimen'].unique():
            regimen_data = survival_data[survival_data['standardized_regimen'] == regimen].dropna(subset=['duration'])
            if regimen_data.empty:
                continue
            # Fit the model for each regimen, ensuring no NaNs are present
            kmf.fit(regimen_data['duration'], event_observed=(regimen_data['event_mapped'] == 'death'))
            kmf.plot_survival_function(ax=ax, label=f"Regimen: {regimen}")

        plt.title("Kaplan-Meier Survival Curve by Treatment Regimen", pad=20)
        plt.xlabel("Survival Duration (days)", labelpad=15)
        plt.ylabel("Survival Probability", labelpad=15)
        plt.legend(title="Treatment Regimen")

        # Use plt.gcf() to get the current figure
        save_visualization(plt.gcf(), "survival_analysis", "kaplan_meier_survival_curve.png")
        plt.close()

    except Exception as e:
        print(f"❌ Visualization error: {str(e)}")

# Function to visualize Motion Chart (Animated Bubble Chart)
def visualize_treatment_regimen_changes(data_path):
    """Visualize treatment regimen changes and survival rate using Motion Chart"""
    try:
        df = pd.read_csv(data_path)

        # Ensure start_date_of_regimen is datetime
        df['start_date_of_regimen'] = pd.to_datetime(df['start_date_of_regimen'], errors='coerce')

        # Filter necessary columns
        motion_data = df[['start_date_of_regimen', 'standardized_regimen', 'event_mapped', 'duration']].dropna()

        # Create a new column for year-month to track trends over time
        motion_data['year_month'] = motion_data['start_date_of_regimen'].dt.to_period('M')

        # Create an animated bubble chart
        fig = go.Figure()

        for regimen in motion_data['standardized_regimen'].unique():
            regimen_data = motion_data[motion_data['standardized_regimen'] == regimen]
            fig.add_trace(go.Scatter(
                x=regimen_data['year_month'].astype(str),
                y=regimen_data['duration'],
                mode='markers',
                marker=dict(size=regimen_data['duration'] / 10, opacity=0.6, color=regimen_data['event_mapped'].map(
                    {'survival': 'green', 'death': 'red', 'unknown': 'gray'})),
                text=regimen_data['standardized_regimen'],
                name=f"Regimen: {regimen}",
                showlegend=True
            ))

        fig.update_layout(
            title="Treatment Regimen Changes & Survival Rate Over Time",
            xaxis_title="Time (Year-Month)",
            yaxis_title="Survival Duration",
            updatemenus=[dict(
                type='buttons',
                showactive=False,
                buttons=[dict(label='Play',
                              method='animate',
                              args=[None, dict(frame=dict(duration=500, redraw=True), fromcurrent=True,
                                               mode='immediate')])])],
            sliders=[dict(
                steps=[dict(
                    args=[None, dict(frame=dict(duration=500, redraw=True), mode='immediate')],
                    label="All Time", method="animate")])],
            height=800,
            width=1200
        )

        save_visualization(fig, "motion_chart", "treatment_regimen_changes_motion_chart.html")

    except Exception as e:
        print(f"❌ Visualization error: {str(e)}")

# Main function to run the visualizations
def main():
    file_path = os.path.join(BASE_DIR, "processed/final_merged_data.csv")
    df = load_data(file_path)
    if df is None:
        print("❌ Failed to load data. Please check the file path.")
        return
    print(f"\n🔍 Loaded data sample:")
    print(df.head())
    while True:
        print("\n📊 Visualization Menu:")
        print("1. Extract Visualization Data")
        print("2. Treatment Success Rate Analysis")
        print("3. Success Rate by Cancer Type")
        print("4. Treatment Modification Pattern Analysis")
        print("5. Kaplan-Meier Survival Curve")
        print("6. Treatment Regimen Changes & Survival Rate (Motion Chart)")
        print("7. Exit")
        choice = input("Select (1-7): ").strip()
        if choice == '1':
            analysis_types = ["success_rate", "cancer_type", "modification_patterns",
                              "survival_analysis", "motion_chart"]
            for analysis_type in analysis_types:
                extract_visualization_data(df, analysis_type)
        elif choice == '2':
            visualize_treatment_success_rate(os.path.join(VIS_DATA_DIR, "success_rate_data.csv"))
        elif choice == '3':
            visualize_cancer_type_success_rate(os.path.join(VIS_DATA_DIR, "cancer_type_data.csv"))
        elif choice == '4':
            visualize_treatment_modifications(os.path.join(VIS_DATA_DIR, "modification_patterns_data.csv"))
        elif choice == '5':
            visualize_kaplan_meier(os.path.join(VIS_DATA_DIR, "survival_analysis_data.csv"))
        elif choice == '6':
            visualize_treatment_regimen_changes(os.path.join(VIS_DATA_DIR, "motion_chart_data.csv"))
        elif choice == '7':
            print("👋 Exiting the program.")
            break
        else:
            print("❌ Invalid input. Please try again.")

if __name__ == "__main__":
    main()
