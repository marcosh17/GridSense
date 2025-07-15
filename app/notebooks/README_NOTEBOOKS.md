# NOTEBOOKS STRUCTURE 
01	Preprocessing & Integrity Checks
02	Exploratory Data Analysis (EDA)
03	Model Training
04	Model Evaluation
05	Deployment / Batch Inference



# 📓 Notebook 1 – Preprocessing and Data Integrity Checks

## **Objective**

Prepare, clean, and verify the consistency of the combined **Open-Meteo** and **PVGIS** datasets before training a machine learning model to predict solar irradiance.

---

## **Pipeline Summary**

### **1️⃣ Load raw data**

- Load `openmeteo_all_cities.csv` and `pvgis_all_cities.csv` from `data/raw_data/`
- Use `parse_dates=['time']` to handle timestamps correctly.

---

### **2️⃣ Check data dimensions**

- Display the number of rows and columns for each dataset.
- Verify that both datasets cover the expected number of records.

---

### **3️⃣ Check for duplicates**

- Detect and remove duplicated rows based on `time` and `city`.

---

### **4️⃣ Check for missing values**

- Print the percentage of missing data per column.
- Decide whether to impute, drop, or leave missing values depending on their significance.

---

### **5️⃣ Verify time coverage**

- Compare the time ranges between Open-Meteo and PVGIS datasets.
- Identify any mismatches or gaps.

---

### **6️⃣ Align PVGIS time**

#### **Problem detected:**

PVGIS provides hourly data **with a timestamp at `HH:09`**, representing the **end of the interval**.  
Example:

| PVGIS time (original) | Real interval represented |
|----------------------|---------------------------|
| 2020-12-31 23:09:00   | 23:00:00 – 23:09:00       |

#### **Solution:**

- Shift PVGIS timestamps **back by 9 minutes** to align with the start of the hour.

```python
df_pvgis['time'] = pd.to_datetime(df_pvgis['time']) - pd.to_timedelta(9, unit='m')
df_pvgis['time'] = df_pvgis['time'].dt.floor('h')
```

---

### **7️⃣ Clip PVGIS time range**

After shifting the timestamps, clip PVGIS to match the exact time range of Open-Meteo:

```python
min_time = df_openmeteo['time'].min()
max_time = df_openmeteo['time'].max()

df_pvgis = df_pvgis[(df_pvgis['time'] >= min_time) & (df_pvgis['time'] <= max_time)]
```

This ensures both datasets cover the same time period with the same hourly structure.

---

### **8️⃣ Merge datasets**

Perform an **inner join** on `time` and `city`:

```python
df_merged = pd.merge(df_openmeteo, df_pvgis, on=["time", "city"], how="inner")
```

---

### **9️⃣ Validate merge result**

- Confirm that the merged dataset has the expected number of rows and no time misalignment.
- Ensure all cities and hours are correctly combined.

---

### **🔧 Note on previous runs:**

In early attempts, there was a discrepancy of 2 hours at the end of the dataset due to timestamp shifts.  
After re-running with the correct time clipping, **the final dataset fully aligns without missing hours.**

---

## **Final Output**

- `df_openmeteo_clean.parquet`
- `df_pvgis_clean.parquet`
- `merged_openmeteo_pvgis.parquet`

These files are saved in `data/processed/`.

---

## **Next Step**

Proceed to **Notebook 2**: Exploratory Data Analysis (EDA) and Visualization.

#################################################################################

# 📓 Notebook 2A – Global EDA

## Objective

Perform global exploratory data analysis (EDA) to understand the overall behavior of irradiance and weather variables.

---

## 0️⃣ Load processed data

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# Define project root and data path
current_dir = Path().resolve()
root = current_dir.parents[1]  # From 'app/notebooks/' to 'GridSense/'

data_dir = root / 'data' / 'processed'

# Load merged dataset (Parquet only)
df = pd.read_parquet(data_dir / 'merged_openmeteo_pvgis.parquet')

print("✅ Merged dataset loaded. Shape:", df.shape)
```
---

## 1️⃣ Define features and target

```python
target = 'global_irradiance_W_m2'

features = [
    'temperature_2m',
    'cloudcover',
    'windspeed_10m',
    'winddirection_10m',
    'shortwave_radiation',
    'direct_radiation',
    'diffuse_radiation',
    'cloud_cover'
]

X = df[features]
y = df[target]
```
---

## 2️⃣ Summary statistics

```python
df.describe()
```
---

## 3️⃣ Missing values check

```python
print("Missing values per column:
")
print(df.isnull().sum())
```
---

## 4️⃣ Distributions of variables

```python
# Histogram of target
sns.histplot(df[target], bins=50, kde=True)
plt.title("Distribution of Global Irradiance (W/m²)")
plt.show()

# Histograms of features
for feature in features:
    sns.histplot(df[feature], bins=50, kde=True)
    plt.title(f"Distribution of {feature}")
    plt.show()
```
---

## 5️⃣ Correlation analysis

```python
corr = df[features + [target]].corr()

plt.figure(figsize=(10,8))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Correlation Matrix (Features + Target)")
plt.show()
```
---

## 6️⃣ Seasonality and temporal patterns

```python
df['month'] = df['time'].dt.month
df['hour'] = df['time'].dt.hour

# Monthly seasonality
sns.boxplot(x='month', y=target, data=df)
plt.title("Monthly Irradiance Distribution")
plt.show()

# Hourly seasonality
sns.boxplot(x='hour', y=target, data=df)
plt.title("Hourly Irradiance Distribution")
plt.show()
```
---

## 7️⃣ Outlier detection (visual)

```python
sns.boxplot(y=df[target])
plt.title("Outliers in Global Irradiance (W/m²)")
plt.show()
```

---

# 📓 Notebook 2B – EDA Per City



# 📓 Notebook 2B – EDA Per City

## Objective

Perform detailed exploratory data analysis (EDA) by city to understand local behavior of irradiance and weather variables.

---

## 0️⃣ Load processed data

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# Define project root and data path
current_dir = Path().resolve()
root = current_dir.parents[1]  # From 'app/notebooks/' to 'GridSense/'

data_dir = root / 'data' / 'processed'

# Load merged dataset (Parquet only)
df = pd.read_parquet(data_dir / 'merged_openmeteo_pvgis.parquet')

print("✅ Merged dataset loaded. Shape:", df.shape)
```
---

## 1️⃣ Filter irradiance > 0

```python
target = 'global_irradiance_W_m2'
df_nonzero = df[df[target] > 0]
print("✅ Filtered non-zero irradiance. Shape:", df_nonzero.shape)
```
---

## 2️⃣ Histograms of irradiance per city (FacetGrid)

```python
g = sns.FacetGrid(df_nonzero, col="city", col_wrap=5, sharex=True, sharey=True)
g.map(sns.histplot, target, bins=30)

for ax, title in zip(g.axes.flatten(), df_nonzero['city'].unique()):
    ax.set_title(title)

g.fig.subplots_adjust(top=0.9)
g.fig.suptitle("Irradiance Distribution by City (Irradiance > 0)", fontsize=16)
plt.show()
```
---

## 3️⃣ Boxplot of irradiance per city

```python
sns.boxplot(x='city', y=target, data=df_nonzero)
plt.xticks(rotation=90)
plt.title("Global Irradiance Distribution per City (Irradiance > 0)")
plt.show()
```
---

## 4️⃣ Correlation matrix per city

```python
features = [
    'temperature_2m',
    'cloudcover',
    'windspeed_10m',
    'winddirection_10m',
    'shortwave_radiation',
    'direct_radiation',
    'diffuse_radiation',
    'cloud_cover'
]

cities = df['city'].unique()

for city in cities:
    df_city = df[df['city'] == city]
    corr = df_city[features + [target]].corr()
    
    plt.figure(figsize=(8,6))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title(f"Correlation Matrix - {city.title()}")
    plt.show()
```
---

## 5️⃣ Seasonality per city (Month & Hour)

### Monthly seasonality:

```python
df_nonzero['month'] = df_nonzero['time'].dt.month

g = sns.FacetGrid(df_nonzero, col="city", col_wrap=5, sharex=True, sharey=True)
g.map_dataframe(sns.boxplot, x="month", y=target)

for ax, title in zip(g.axes.flatten(), df_nonzero['city'].unique()):
    ax.set_title(title)

g.fig.subplots_adjust(top=0.9)
g.fig.suptitle("Monthly Irradiance Distribution by City (Irradiance > 0)", fontsize=16)
plt.show()
```

### Hourly seasonality:

```python
df_nonzero['hour'] = df_nonzero['time'].dt.hour

g = sns.FacetGrid(df_nonzero, col="city", col_wrap=5, sharex=True, sharey=True)
g.map_dataframe(sns.boxplot, x="hour", y=target)

for ax, title in zip(g.axes.flatten(), df_nonzero['city'].unique()):
    ax.set_title(title)

g.fig.subplots_adjust(top=0.9)
g.fig.suptitle("Hourly Irradiance Distribution by City (Irradiance > 0)", fontsize=16)
plt.show()
```
---

## ✅ Notebook 2B Complete

You now have a detailed view of each city's irradiance patterns and their correlations with weather variables. Ready to proceed to model training.

