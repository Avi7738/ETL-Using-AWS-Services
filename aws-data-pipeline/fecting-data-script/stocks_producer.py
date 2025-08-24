import requests
import json
import boto3
from dotenv import load_dotenv
import os
import time
from datetime import datetime

# Load environment variables
load_dotenv()

API_KEY = os.getenv("ALPHA_VANTAGE_KEY")

# Multiple stock symbols (jitne chaho add kar lo)
SYMBOLS = ["IBM", "AAPL", "GOOG"]

# AWS creds from .env
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")

# S3 client
s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

BUCKET_NAME = "raw-data-24-08"
FOLDER = "stocks"

while True:
    for symbol in SYMBOLS:
        URL = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&apikey={API_KEY}"

        response = requests.get(URL)
        data = response.json()
        
        payload = {
            "symbol": symbol,
            "data": data,
            "timestamp": datetime.utcnow().isoformat()
        }

        # File path → stocks/<symbol>/<symbol>-<timestamp>.json
        file_name = f"{FOLDER}/{symbol}/{symbol}-{int(time.time())}.json"

        # Upload to S3
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=file_name,
            Body=json.dumps(payload),
            ContentType="application/json"
        )

        print(f"✅ Uploaded: s3://{BUCKET_NAME}/{file_name}")

    time.sleep(60)  # wait 1 min, then repeat for all symbols
