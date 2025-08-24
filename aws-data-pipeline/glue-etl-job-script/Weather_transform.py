import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import col, lit, current_timestamp
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType, TimestampType

# --------- Glue Arguments ---------
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# --------- S3 Paths ---------
raw_s3_path = "s3://raw-data-24-08/weather/"        # raw JSON data
processed_s3_path = "s3://curated-data-24-08/ready-weather/"    # processed Parquet output

# --------- Define Schema ---------
schema = StructType([
    StructField("city", StringType(), True),
    StructField("temp", DoubleType(), True),
    StructField("humidity", IntegerType(), True),
    StructField("weather", StringType(), True),
    StructField("timestamp", TimestampType(), True)
])

# --------- Read Raw JSON (recursive for subfolders) ---------
df = spark.read.option("recursiveFileLookup", "true") \
               .schema(schema) \
               .json(raw_s3_path)

# --------- Transformations ---------
df_transformed = df.withColumn("temp_celsius", col("temp") - 273.15) \
                   .withColumnRenamed("humidity", "humidity_percent") \
                   .withColumn("processed_timestamp", current_timestamp())  # add ETL timestamp

# Optional filter (e.g., only temps > 20°C)
df_filtered = df_transformed.filter(col("temp_celsius") > 20)

# --------- Write to S3 as Parquet (partitioned by city) ---------
df_filtered.write.mode("overwrite") \
           .partitionBy("city") \
           .parquet(processed_s3_path)

# --------- Commit Job ---------
job.commit()
