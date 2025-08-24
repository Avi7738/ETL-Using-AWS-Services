# ETL-Using-AWS-Services

# AWS Data Engineering Pipeline (Kafka → S3 → Glue → Athena → Power BI)

## 🚀 Architecture
1. **Kafka → S3 (raw-data-24-08)**  
   - Weather + Stocks raw data stored.  

2. **Glue Crawlers**  
   - `weather_crawler` → raw weather data  
   - `stocks_crawler` → raw stocks data  

3. **Glue ETL Jobs**  
   - `weather_transform` → process raw → curated parquet (`ready-weather/`)  
   - `stocks_transform` → process raw → curated parquet (`ready-stocks/`)  

4. **Athena**  
   - Query raw + curated data  

5. **Power BI**  
   - Connects to curated-data-24-08 or use Python export scripts to CSV.  

---

## 🗂️ Folder Structure
- `glue-scripts/` → Glue ETL jobs (PySpark scripts)  
- `powerbi/` → Power BI integration scripts  
- `s3-buckets/` → Documentation of raw + curated storage layout  

---

## 🔧 Glue Scripts
- `weather_transform.py` → Cleans and transforms raw weather data → curated parquet  
- `stocks_transform.py` → Cleans and transforms raw stocks data → curated parquet  

---

## 🔗 Power BI Connection
Option 1: Connect Power BI directly to Athena.  
Option 2: Run export scripts to convert parquet → CSV:
- `export_weather_csv.py`  
- `export_stocks_csv.py`  
