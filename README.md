# ETL-Using-AWS-Services

# AWS Data Pipeline – Stocks & Weather

End-to-end **AWS Data Engineering Pipeline** that ingests data from **Kafka (via Docker + Python)** into **S3 (Raw)**, transforms it using **AWS Glue (PySpark)**, stores curated Parquet datasets in **S3 (Curated)**, and exposes it for querying via **Athena** and visualization in **Power BI**.  

---

## 🏗️ Architecture

<img width="1748" height="1240" alt="Image" src="https://github.com/user-attachments/assets/692b682f-d83d-451c-ae8e-9ff28040e159" />

**Flow:**
1. **Kafka (Docker + Python)** → Streams **stocks** and **weather** data into **S3 Raw**.
2. **AWS Glue Crawlers** → Crawl `raw-data-24-08` bucket and create schemas in Glue Data Catalog.
3. **AWS Glue ETL Jobs** →  
   - `stocks_transform.py` → writes curated parquet to `s3://curated-data-24-08/ready_stocks/`  
   - `weather_transform.py` → writes curated parquet to `s3://curated-data-24-08/ready_weather/`
4. **Athena** → Query raw and curated datasets directly.
5. **Power BI** → Uses Athena connector for dashboards & reporting.

---

## 📂 Folder Structure
```
aws-data-pipeline-repo/
│── fetching-data-script/        # Kafka → S3 Raw ingestion scripts
│   ├── stocks_producer.py
│   ├── weather_producer.py
│   └── .env                     # Kafka & AWS configs (never commit secrets!)
│
│── glue-etl-job-script/         # AWS Glue ETL jobs (PySpark)
│   ├── stocks_transform.py
│   └── weather_transform.py

```


