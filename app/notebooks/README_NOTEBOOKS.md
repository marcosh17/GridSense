
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

