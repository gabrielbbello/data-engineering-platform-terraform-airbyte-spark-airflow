import os
from pyspark.sql import SparkSession
from dotenv import load_dotenv

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

env_path = os.path.join(project_root, ".env")

load_dotenv(env_path)

def get_spark_session(app_name="MyAPP"):
    """
    Creates and returns a SparkSession configured for S3 access.
    """
    ACCESS_KEY = os.getenv('ACCESS_KEY')
    SECRET_ACCESS_KEY = os.getenv('SECRET_ACCESS_KEY')
    
    spark = SparkSession.builder \
        .appName(app_name) \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .config("spark.hadoop.fs.s3a.access.key", ACCESS_KEY) \
        .config("spark.hadoop.fs.s3a.secret.key", SECRET_ACCESS_KEY) \
        .config("spark.hadoop.fs.s3a.endpoint", "s3.amazonaws.com") \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel("ERROR")
        
    return spark
