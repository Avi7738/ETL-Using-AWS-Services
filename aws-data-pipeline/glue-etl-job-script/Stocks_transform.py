import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import col, lit, current_timestamp
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType

# --------- Glue Arguments ---------
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# --------- S3 Paths ---------
raw_s3_path = "s3://raw-data-24-08/stocks/"           # raw JSON data
processed_s3_path = "s3://curated-data-24-08/ready-stocks/"  # processed Parquet output

# --------- Define Schema ---------
schema = StructType([
    StructField("Meta Data", StringType(), True),
    StructField("Time Series (1min)", StringType(), True)  # nested JSON, can process later
])

# --------- Read Raw JSON (recursive for subfolders) ---------
df = spark.read.option("recursiveFileLookup", "true") \
               .schema(schema) \
               .json(raw_s3_path)

# --------- Transformations ---------
df_transformed = df.withColumn("processed_timestamp", current_timestamp())  # add ETL timestamp

# --------- Write to S3 as Parquet (partitioned by symbol) ---------
df_transformed.write.mode("overwrite") \
           .partitionBy("Meta Data") \
           .parquet(processed_s3_path)

# --------- Commit Job ---------
job.commit()
