# Databricks notebook source
# Auto Loader with schema evolution mode addNewColumns.
# When a new column shows up, this stream fails once, saves the new schema,
# and the task retry (max_retries in resources/orders_job.yml) succeeds.

# COMMAND ----------
dbutils.widgets.text("catalog", "")
dbutils.widgets.text("schema", "")
dbutils.widgets.text("landing_path", "")
dbutils.widgets.text("checkpoint_root", "")

catalog = dbutils.widgets.get("catalog")
schema = dbutils.widgets.get("schema")
landing_path = dbutils.widgets.get("landing_path")
checkpoint_root = dbutils.widgets.get("checkpoint_root")

target_table = f"{catalog}.{schema}.orders_job"
print("reading from:", landing_path)
print("writing to:  ", target_table)

# COMMAND ----------
query = (
    spark.readStream.format("cloudFiles")
    .option("cloudFiles.format", "json")
    .option("cloudFiles.schemaLocation", f"{checkpoint_root}/schema")
    .option("cloudFiles.inferColumnTypes", "true")
    .option("cloudFiles.schemaEvolutionMode", "addNewColumns")
    .load(landing_path)
    .writeStream
    .option("checkpointLocation", f"{checkpoint_root}/chk")
    .option("mergeSchema", "true")
    .trigger(availableNow=True)
    .toTable(target_table)
)
query.awaitTermination()
