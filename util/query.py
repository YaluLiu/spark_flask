from pyspark.sql import SparkSession, SQLContext
from pyspark.sql.functions import *
from pyspark.sql.types import *
import pyspark.sql.functions as F
from pyspark.sql import Window
import sys
import numpy as np
import pandas as pd
import json
import os
from pymongo import MongoClient
from sshtunnel import SSHTunnelForwarder

MONGO_HOST = "192.168.200.45"
MONGO_DB = "DATABASE_NAME"
MONGO_USER = "boli"
MONGO_PASS = "123456"

def trafficLight(DF):
    DF = DF.select("timestamp", 
                   "signal",
                   "frameID")
    DF = DF.withColumn("indicator", F.when(DF.signal != "None", 1).otherwise(0))
    
    DF = DF.withColumn("id", F.monotonically_increasing_id())
    globalWindow = Window.partitionBy(lit(0)).orderBy(DF.id)
    upToThisRowWindow = globalWindow.rowsBetween(-sys.maxsize-1, 0)
    
    DF = DF.withColumn("section_start", 
                       F.when(F.lag("indicator", 1).over(globalWindow) != DF.indicator, 1).otherwise(0))\
            .withColumn("section_end", 
                        F.when(F.lag("indicator", -1).over(globalWindow) != DF.indicator, 1).otherwise(0))
    min_id, max_id = DF.select(F.min(DF.id), F.max(DF.id)).first()
    
    DF = DF.filter(((DF.indicator == 1) & (DF.section_start == 1) & (DF.id != max_id)) | 
                          ((DF.indicator == 1) & (DF.section_end == 1) & (DF.id != min_id)) | 
                          ((DF.indicator == 1) & (DF.section_start == 0) & (DF.id == max_id)) | 
                          ((DF.indicator == 1) & (DF.section_end == 0) & (DF.id == min_id)))\
                    .select("timestamp", "frameID")\
                    .withColumn("timestamp_datetime", 
                                F.from_unixtime(F.col("timestamp"),'yyyy-MM-dd HH:mm:ss'))\
                    .select("timestamp_datetime", "frameID")
    
    df = DF.toPandas()
    df = pd.concat([df.add_suffix('1'), df.shift(-1).add_suffix('2')], axis=1)
    df = df.loc[::2, :]
    df = df.rename(columns={"timestamp_datetime1": "start_time", "timestamp_datetime2": "end_time", 
                            "frameID1": "start_frame", "frameID2": "end_frame"}).astype({'end_frame': 'int64'})
    
    return {"traffic_light_time": df.to_dict(orient='records'), "traffic_light_count": df.shape[0]}

def objectStat(DF):
    DF = DF.select("object", "frameID")
    DF = DF.withColumn("new", F.explode("object"))\
            .select("new.id", "new.type", "new.timestampSec", "frameID")\
            .dropna()
    w = Window.partitionBy("id", "type")
    DF = DF.withColumn('max_timestamp', F.max('timestampSec').over(w))\
            .withColumn('min_timestamp', F.min('timestampSec').over(w))\
            .withColumn('start_frameID', F.min('frameID').over(w))\
            .withColumn('end_frameID', F.max('frameID').over(w))
    DF = DF.filter((DF.frameID == DF.start_frameID) & (DF.start_frameID != DF.end_frameID))
    DF = DF.select("id", "type", "max_timestamp", "min_timestamp", "start_frameID", "end_frameID")\
            .withColumn("start_time", 
                        F.from_unixtime(F.col("min_timestamp"),'yyyy-MM-dd HH:mm:ss'))\
            .withColumn("end_time", 
                        F.from_unixtime(F.col("max_timestamp"),'yyyy-MM-dd HH:mm:ss'))\
            .select("id", "type", "start_time", "end_time", "start_frameID", "end_frameID")
    return DF

def objectQuery(DF, object_type):
    DF = DF.filter(DF.type == object_type)\
            .select("id", "start_time", "end_time", "start_frameID", "end_frameID")
    return {object_type.lower() + "_time": DF.toPandas().to_dict(orient='records'), 
            object_type.lower() + "_count": DF.count()}


def init(server, record_json_name):
    pipeline = [{'$project': {'timestamp': '$autoDrivingCar.timestampSec', 
                              'signal': '$trafficSignal.currentSignal', 
                              'frameID': '$sequenceNum', 
                              'object': '$object'}}]
    
    input_uri = 'mongodb://localhost:' + str(server.local_bind_port) + '/apollo.' + record_json_name
    output_uri = 'mongodb://localhost:' + str(server.local_bind_port) + '/apollo.statistics'
    spark = SparkSession \
            .builder \
            .appName(record_json_name) \
            .config("spark.mongodb.input.uri", 
                    input_uri) \
            .config("spark.mongodb.output.uri", 
                    output_uri) \
            .config("spark.jars.packages", 
                    "org.mongodb.spark:mongo-spark-connector_2.12:3.0.0") \
            .getOrCreate()
    return spark, pipeline

def stat(spark, pipeline, record_json_name, collection):
    DF = spark.read.format("mongo").option("pipeline", pipeline).load()
    
    traffic = trafficLight(DF)
    Objects = objectStat(DF)
    pedestrian = objectQuery(Objects, "PEDESTRIAN")
    vehicle = objectQuery(Objects, "VEHICLE")
    bicycle = objectQuery(Objects, "BICYCLE")
        
    collection.insert_one({'record_name': record_json_name, 
                           'stat': dict(traffic, **pedestrian, **vehicle, **bicycle)})

if __name__ == "__main__":
    server = SSHTunnelForwarder(
        MONGO_HOST,
        ssh_username=MONGO_USER,
        ssh_password=MONGO_PASS,
        remote_bind_address=('127.0.0.1', 27017))
    
    server.start()
    client = MongoClient('mongodb://localhost:' + str(server.local_bind_port) + '/')
    stats = client.apollo.statistics
    
    records_list = ['0','1','20201130152636','record_35']
    for record_json_name in records_list:
        spark, pipeline = init(server, record_json_name)
        stat(spark, pipeline, record_json_name, stats)
        spark.stop()
    
    client.close()
    server.stop()

#     datas = json.dumps(ans, indent=4)
#     from solve_json import write_json
#     write_json(ans,"datas/query_res.json")