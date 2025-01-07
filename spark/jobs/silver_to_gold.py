from config.spark_conf import get_spark_session
from config.logger import get_logger
from pyspark.sql.functions import *
import os
from dotenv import load_dotenv

try:
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

    env_path = os.path.join(project_root, ".env")

    load_dotenv(env_path)

    logger = get_logger("silver_to_gold")

    logger.info("\nStarting silver_to_gold.py application...\n")

    try:
        logger.info("\nSetting up the spark session...\n")
        spark = get_spark_session(app_name="bronze_to_silver")
    except Exception as e:
        logger.error("Failed to create SparkSession.", exc_info=True)
        raise

    SILVER_BUCKET_NAME = os.getenv("SILVER_BUCKET_NAME")
    GOLD_BUCKET_NAME = os.getenv("GOLD_BUCKET_NAME")

    file_silver_path = f"s3a://{SILVER_BUCKET_NAME}/origin=airbyte/database=postgres/public/flights/*.parquet"
    destination_gold_path = f"s3a://{GOLD_BUCKET_NAME}/origin=airbyte/database=postgres/public/flights/"

    try:
        logger.info(f"\nReading the file from the {SILVER_BUCKET_NAME} bucket...\n")
        df = spark.read.format("parquet")\
            .option("header", True)\
            .option("inferSchema", True)\
            .load(file_silver_path)
    except Exception as e:
        logger.error("Failed to read file")
        raise

    df.createOrReplaceTempView("silver_view")

    logger.info(f"\nCreating the aggregated table with Spark.sql...\n")

    aggregated_table_by_company = spark.sql(
        """
        SELECT 
            month
            ,name
            ,COUNT(*) AS total_flights
            ,ROUND(AVG(dep_delay), 1) AS average_departure_delay_time
            ,ROUND(AVG(arr_delay), 1) AS average_arrival_delay_time
            ,ROUND(SUM(CASE WHEN dep_delay <= 0 THEN 1 ELSE 0 END) / COUNT(*) * 100, 1) AS pct_on_time_departures
            ,ROUND(SUM(CASE WHEN arr_delay <= 0 THEN 1 ELSE 0 END) / COUNT(*) * 100, 1) AS pct_on_time_arrivals
            ,ROUND(SUM(CASE WHEN dep_delay > 15 THEN 1 ELSE 0 END), 1) AS flights_with_significant_departure_delay
            ,ROUND(SUM(CASE WHEN arr_delay > 15 THEN 1 ELSE 0 END), 1) AS flights_with_significant_arrival_delay
            ,ROUND(AVG(air_time + dep_delay + arr_delay), 1) AS avg_total_travel_time
            ,ROUND(AVG(distance), 1) AS avg_distance
            ,ROUND(SUM(CASE WHEN distance <= 500 THEN 1 ELSE 0 END), 1) AS short_flights
            ,ROUND(SUM(CASE WHEN distance > 500 AND distance <= 1500 THEN 1 ELSE 0 END), 1) AS medium_flights
            ,ROUND(SUM(CASE WHEN distance > 1500 THEN 1 ELSE 0 END), 1) AS long_flights
            ,ROUND(MAX(dep_delay), 1) AS max_departure_delay
            ,ROUND(MIN(dep_delay), 1) AS min_departure_delay
            ,ROUND(MAX(arr_delay), 1) AS max_arrival_delay
            ,ROUND(MIN(arr_delay), 1) AS min_arrival_delay
        FROM 
            silver_view
        GROUP BY 
            name, month
        ORDER BY 
            name;
        """
    )

    try:
        logger.info(f"\nSaving aggregated table in the Gold layer {GOLD_BUCKET_NAME} bucket...\n")
        aggregated_table_by_company.write.format("parquet")\
            .mode("overwrite")\
            .save(destination_gold_path)
    except Exception as e:
        logger.error("Failed to save the file in the Gold layer.", exc_info=True)
        raise
    
    logger.info("\nFinishing silver_to_gold.py application with SUCCESS status...\n")

except Exception as e:
    logger.error("Unexpected error in silver_to_gold pipeline.", exc_info=True)
    raise