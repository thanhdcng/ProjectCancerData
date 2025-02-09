# Demo Version README

## Project Overview
This project provides a demo version of the cancer data analysis pipeline. It includes a subset of the full dataset (5,000 samples) to demonstrate key functionalities such as survival rate analysis, treatment success rates, and Kaplan-Meier survival curves.

## Key Features
- Processes a demo dataset with 5,000 samples.
- Computes average survival rates.
- Analyzes success rates by cancer type.
- Implements Kaplan-Meier survival analysis.
- Generates visualizations to support findings.

## Project Structure

```
demo_version/
├── __init__.py               # Package initializer
├── config/
│   ├── __init__.py           # Config module initializer
│   └── settings.py           # Configuration file for paths and parameters
├── analysis/
│   ├── __init__.py           # Analysis module initializer
│   ├── demo_analysis.py      # Performs key demo analysis
├── visualization/
│   ├── __init__.py           # Visualization module initializer
│   ├── demo_visualization.py # Generates demo charts and plots
├── main.py                   # Entry point for executing the demo
└── summary/
    ├── demo_summary_report.txt # Summary of key findings
```

## Installation and Setup

Clone the repository:
```bash
git clone https://github.com/justinCoKA/cancer_data_demo.git
cd cancer_data_demo
```

Install required packages:
```bash
pip install pandas numpy matplotlib seaborn lifelines
```

## Usage

Run `main.py` to start the demo analysis:
```bash
python main.py
```

### Steps Performed:
1. **Data Analysis**
   - Computes survival rates and regimen success.
   - Analyzes key treatment patterns.
   - Performs Kaplan-Meier survival analysis.

2. **Visualization**
   - Generates survival curves.
   - Visualizes treatment success by cancer type.

3. **Summary Report**
   - Key findings (from `demo_summary_report.txt`):
   ```
   Demo Summary Report
   ====================
   1. Number of data samples: 5000
   2. Average survival rate: 7.87%
   3. Key analysis points:
      - Average survival rate by regimen
      - Success rate by cancer type
      - Kaplan-Meier survival analysis results
   ====================
   ```

## Code Explanation

### `demo_analysis.py`
Performs core survival rate analysis and computes key statistics on the demo dataset.

### `demo_visualization.py`
Generates visualizations such as survival curves and treatment success rates.

### `main.py`
Executes the demo pipeline, orchestrating data analysis and visualization generation.


