import sqlite3
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import sum as spark_sum, count, col

# 1. Init Spark
spark = SparkSession.builder.appName("KiambuRevenueETL").getOrCreate()

# 2. Extract from SQLite (your backend DB)
conn = sqlite3.connect("ecitizen.db")
print("Extracting...")

# Load tables to pandas then to spark
apps_pdf = pd.read_sql_query("SELECT * FROM applications", conn)
pays_pdf = pd.read_sql_query("SELECT * FROM payments", conn)
servs_pdf = pd.read_sql_query("SELECT * FROM services", conn)
conn.close()

# Handle empty tables
if pays_pdf.empty:
    print("No payments yet. Add some via /docs -> POST /payments")
    exit()

apps_df = spark.createDataFrame(apps_pdf)
pays_df = spark.createDataFrame(pays_pdf)
servs_df = spark.createDataFrame(servs_pdf)

# 3. Transform - JOIN and Aggregate
# Join payments -> applications -> services
joined = pays_df.join(apps_df, pays_df.application_id == apps_df.id) \
                 .join(servs_df, apps_df.service_id == servs_df.id)

revenue_summary = joined.groupBy("name").agg(
    spark_sum("amount").alias("total_collected"),
    count("payments.id").alias("total_transactions")
).orderBy(col("total_collected").desc())

# 4. Load - Show + Save
print("\n=== KIAMBU COUNTY REVENUE REPORT ===")
revenue_summary.show()

# Save as Parquet for PowerBI / Tableau later
revenue_summary.write.mode("overwrite").parquet("data_lake/revenue_summary")
print("Saved to data_lake/revenue_summary")

# Also save CSV for easy checking
revenue_summary.toPandas().to_csv("revenue_summary.csv", index=False)

spark.stop()