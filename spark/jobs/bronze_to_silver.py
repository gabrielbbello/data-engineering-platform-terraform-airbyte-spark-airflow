from config.spark_conf import get_spark_session
from config.logger import get_logger
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, TimestampType, MapType, DoubleType
from pyspark.sql.functions import col
import os
from dotenv import load_dotenv

try:
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

    env_path = os.path.join(project_root, ".env")

    load_dotenv(env_path)

    logger = get_logger("bronze_to_silver")

    logger.info("\nStarting bronze_to_silver.py application...\n")

    try:
        logger.info("\nSetting up the spark session...\n")
        spark = get_spark_session(app_name="bronze_to_silver")
    except Exception as e:
        logger.error("Failed to create SparkSession.", exc_info=True)
        raise

    BRONZE_BUCKET_NAME = os.getenv("BRONZE_BUCKET_NAME")
    SILVER_BUCKET_NAME = os.getenv("SILVER_BUCKET_NAME")

    file_bronze_path = f"s3a://{BRONZE_BUCKET_NAME}/origin=airbyte/database=postgres/public/flights/*.parquet"
    destination_silver_path = f"s3a://{SILVER_BUCKET_NAME}/origin=airbyte/database=postgres/public/flights/"

    logger.info("\nSetting up the schema...\n")

    schema = StructType([
        StructField("_airbyte_ab_id", StringType(), True),
        StructField("_airbyte_emitted_at", TimestampType(), True),
        StructField("flight", IntegerType(), True),
        StructField("arr_delay", DoubleType(), True),
        StructField("distance", IntegerType(), True),
        StructField("year", IntegerType(), True),
        StructField("tailnum", StringType(), True),
        StructField("origin", StringType(), True),
        StructField("dep_time", DoubleType(), True),
        StructField("sched_dep_time", IntegerType(), True),
        StructField("sched_arr_time", IntegerType(), True),
        StructField("dep_delay", DoubleType(), True),
        StructField("dest", StringType(), True),
        StructField("minute", IntegerType(), True),
        StructField("carrier", StringType(), True),
        StructField("hour", IntegerType(), True),
        StructField("month", IntegerType(), True),
        StructField("name", StringType(), True),
        StructField("arr_time", DoubleType(), True),
        StructField("id", IntegerType(), True),
        StructField("air_time", DoubleType(), True),
        StructField(
            "time_hour",
            StructType([
                StructField("member0", TimestampType(), True),
                StructField("member1", StringType(), True),
            ]),
            True
        ),
        StructField("day", IntegerType(), True),
        StructField(
            "_airbyte_additional_properties",
            MapType(StringType(), StringType(), True),
            True
        )
    ])

    try:
        logger.info(f"\nReading the file from the {BRONZE_BUCKET_NAME} bucket...\n")
        df = spark.read.format("parquet")\
            .option("header", True)\
            .schema(schema)\
            .load(file_bronze_path)
    except Exception as e:
        logger.error("Failed to read file")
        raise

    logger.info(f"\nDropping the airbyte metadata columns...\n")

    df = df.drop('_airbyte_ab_id')
    df = df.drop('_airbyte_emitted_at')
    df = df.drop('_airbyte_additional_properties')

    logger.info(f"\nFixing the time_hour column...\n")

    df = df.withColumn("time_hour", col("time_hour.member0"))

    logger.info(f"\nShowing final data after transformations...\n")

    df.show(10)

    try:
        logger.info(f"\nSaving file in the silver layer {SILVER_BUCKET_NAME} bucket...\n")
        df.write.format("parquet")\
            .mode("overwrite")\
            .save(destination_silver_path)
    except Exception as e:
        logger.error("Failed to save the file in the Silver layer.", exc_info=True)
        raise

    logger.info("\nFinishing bronze_to_silver.py application with SUCCESS status...\n")
except Exception as e:
    logger.error("Unexpected error in bronze_to_silver pipeline.", exc_info=True)
    raise