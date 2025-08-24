# ETL-Using-AWS-Services

# AWS Data Pipeline – Stocks & Weather

End-to-end **AWS Data Engineering Pipeline** that ingests data from **Kafka (via Docker + Python)** into **S3 (Raw)**, transforms it using **AWS Glue (PySpark)**, stores curated Parquet datasets in **S3 (Curated)**, and exposes it for querying via **Athena** and visualization in **Power BI**.  

---

## 🏗️ Architecture

![Architecture](docs/architecture.png)

**Flow:**
1. **Kafka (Docker + Python)** → Streams **stocks** and **weather** data into **S3 Raw**.
2. **AWS Glue Crawlers** → Crawl `raw-data-24-08` bucket and create schemas in Glue Data Catalog.
3. **AWS Glue ETL Jobs** →  
   - `stocks_transform.py` → writes curated parquet to `s3://curated-data-24-08/ready_stocks/`  
   - `weather_transform.py` → writes curated parquet to `s3://curated-data-24-08/ready_weather/`
4. **Athena** → Query raw and curated datasets directly.
5. **Power BI** → Uses Athena connector for dashboards & reporting.

---

## 📂 Buckets

- **Raw Data** → `s3://raw-data-24-08/`  
  - `stocks/`  
  - `weather/`  

- **ETL Scripts** → `s3://etl-script-24-08/`  
  - `jobs/stocks_transform.py`  
  - `jobs/weather_transform.py`  

- **Curated Data** → `s3://curated-data-24-08/`  
  - `ready_stocks/` (partitioned parquet)  
  - `ready_weather/` (partitioned parquet)  

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
