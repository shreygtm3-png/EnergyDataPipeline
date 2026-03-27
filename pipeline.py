import pandas as pd
import os

# Memory Optimization

path = "D:\Python_Projects\Projects\Global Power Plant\globalpowerplantdatabasev110\global_power_plant_database.csv"

columns = ['country', 'name', 'capacity_mw', 'fuel1', 'commissioning_year']

dtype_dict = {
    'country': 'category',
    'fuel1': 'category',
    'capacity_mw': 'float32'
}

df = pd.read_csv(
    path,
    usecols = columns,
    dtype = dtype_dict
)

print(f"Memory Usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")


# Cleaning & Contextual Imputation

df['name'] = df['name'].str.strip().str.title()

missing = df['commissioning_year'].isnull().sum()
print(f"Missing years BEFORE: {missing}")

df['commissioning_year'] = df.groupby('fuel1')['commissioning_year'].transform(
    lambda x: x.fillna(x.median())
)

missing_after = df['commissioning_year'].isnull().sum()
print(f"Current Missing Years: {missing_after}")


# New Data

renewable_sources = ['Hydro', 'Wind', 'Solar', 'Biomass', 'Geothermal', 'Wave and Tidal']

df['is_renewable'] = df['fuel1'].isin(renewable_sources)

df['renewable_capacity_mw'] = df['capacity_mw'] * df['is_renewable']

country_metrics = (
    df.groupby('country', observed = True)
    .agg(
        total_mw = ('capacity_mw', 'sum'), 
        renewable_mw = ('renewable_capacity_mw', 'sum')
    )
    .assign(
        renewable_pct = lambda x: (x['renewable_mw'] / x['total_mw']) * 100
    )
    .query('total_mw > 1000')
    .sort_values('renewable_pct', ascending= False)
    .round(1)
)


# Parquet

output_file = ('cleaned_power_plants.parquet')

df.to_parquet(output_file, engine='pyarrow', index = False)

original_size_mb = os.path.getsize(path) / (1024 * 1024)
new_size_mb = os.path.getsize(output_file) (1024 * 1024)

print(f"\nOriginal CSV Size: {original_size_mb:.2f} MB")
print(f"New Parquet Size: {new_size_mb:.2f} MB")
print(f"Storage Reduced By: {((original_size_mb - new_size_mb) / original_size_mb) * 100:.1f}%")

pd.set_option('display.max_rows', 50)
pd.set_option('display.max_columns', None)

print("\n--- First 50 rows of the Cleaned Data ---")
print(df.head(50))