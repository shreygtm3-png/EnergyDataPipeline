# Global Power Plant Efficiency Pipeline

## Project Context
Modern data analysis often starts with a significant hurdle: raw datasets are frequently too large for standard hardware and too "noisy" for immediate use. This project serves as a complete ETL (Extract, Transform, Load) solution designed to bridge that gap. 

By utilizing the Global Power Plant Database, I developed a pipeline that prioritizes memory efficiency and data integrity, transforming 30,000+ rows of raw information into a streamlined, high-performance dataset ready for production-level analytics.

## Technical Approach

### Data Ingestion
Instead of a standard load, this pipeline uses strategic schema definitions. By explicitly defining data types—such as downcasting floats and utilizing categorical encoding for repetitive strings—I reduced the memory footprint by approximately 90%. This ensures the pipeline remains fast and stable even on machines with limited RAM.

### Contextual Data Repair
Real-world data is rarely complete. Rather than using a generic "fill-all" approach for missing commissioning years, this script uses a grouped median strategy. It calculates the median age of plants within the same fuel category (e.g., matching a missing Hydro plant year with other Hydro plants), ensuring the statistical integrity of the timeline analysis.

### Advanced Feature Engineering
To provide immediate business value, the pipeline classifies facilities into "Renewable" and "Non-Renewable" categories using vectorized operations. This avoids the performance lag of Python loops and allows for instantaneous global capacity summaries.

## Tools and Performance
* **Language:** Python
* **Core Library:** Pandas
* **Storage Engine:** PyArrow (Parquet)
* **Performance Note:** The final output is saved in Parquet format, which maintains all optimized data types while occupying significantly less disk space than the original CSV.

## Getting Started
1. Clone this repository to your local environment.
2. Ensure you have the necessary dependencies installed via `pip install pandas pyarrow`.
3. Place the `global_power_plant_database.csv` in the project root.
4. Run the script to generate the optimized Parquet file and the summary report.
