# GSM Promotion Experimentation Data

## Source of Raw Data
- **Source:** NYC TLC Yellow Taxi Trip Records
- **Period:** January 2026 (or corresponding reference month)
- **Required files:**
  - `yellow_tripdata_2026-01.parquet`
  - `taxi_zone_lookup.csv`

## Directory Structure
- `data/raw/`: Place the downloaded `.parquet` and `.csv` files here.
- `data/processed/`: Contains the generated synthetic datasets (`segmented_simulation_data.csv`, `policy_comparison.csv`, etc.) outputted by the pipeline scripts.

*Note: The raw TLC data files are large and are ignored by git (`.gitignore`). If you are setting up this repository locally, you must download them manually to reproduce the Week 1 EDA and initial Data Quality checks.*
