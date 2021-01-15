import sys
sys.path.append("..")

from pyspark.sql import SparkSession, SQLContext
from pyspark.sql.functions import *
from pyspark.sql.types import *
import pyspark.sql.functions as F
from pyspark.sql import Window


import json
import os



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
                    .withColumn("timestamp", 
                                F.from_unixtime(F.col("timestamp"),'yyyy-MM-dd HH:mm:ss'))\
                    .withColumn("row_num", F.monotonically_increasing_id())
    
    D1 = DF.withColumn("encounter", (col("row_num") / 2).cast('int'))\
            .filter(col("row_num") % 2 == 0)\
            .select("timestamp", "frameID", "encounter")\
            .withColumnRenamed("timestamp", "start_time")\
            .withColumnRenamed("frameID", "start_frame")
    
    D2 = DF.withColumn("encounter", (col("row_num") / 2).cast('int'))\
            .filter(col("row_num") % 2 == 1)\
            .select("timestamp", "frameID", "encounter")\
            .withColumnRenamed("timestamp", "end_time")\
            .withColumnRenamed("frameID", "end_frame")
    
    return D1.join(D2, ("encounter")).drop("encounter")

def objectStat(DF):
    DF = DF.select("object", "frameID")
    DF = DF.withColumn("new", F.explode("object"))\
            .select("new.id", "new.type", "new.timestampSec", "frameID")\
            .dropna()
    w = Window.partitionBy("id", "type")
    DF = DF.withColumn('end_time', F.max('timestampSec').over(w))\
            .withColumn('start_time', F.min('timestampSec').over(w))\
            .withColumn('start_frame', F.min('frameID').over(w))\
            .withColumn('end_frame', F.max('frameID').over(w))
    DF = DF.filter((DF.frameID == DF.start_frame) & (DF.start_frame != DF.end_frame))
    DF = DF.select("id", "type", "start_time", "end_time", "start_frame", "end_frame")\
            .withColumn("start_time", 
                        F.from_unixtime(F.col("start_time"),'yyyy-MM-dd HH:mm:ss'))\
            .withColumn("end_time", 
                        F.from_unixtime(F.col("end_time"),'yyyy-MM-dd HH:mm:ss'))
    return DF

def objectQuery(DF, object_type):
    if object_type != "traffic_light":
        DF = DF.filter(DF.type == object_type)\
                .select("id", "start_time", "end_time", "start_frame", "end_frame")
    DF = DF.sort("start_frame", "end_frame")
    return {object_type.lower() + "_time": DF.toPandas().to_dict(orient='records'), 
            object_type.lower() + "_count": DF.count()}


def init_spark(server, records_database_name,record_name):
    pipeline = [{'$project': {'timestamp': '$autoDrivingCar.timestampSec', 
                              'signal': '$trafficSignal.currentSignal', 
                              'frameID': '$sequenceNum', 
                              'object': '$object'}}]
    
    input_uri = 'mongodb://localhost:{}/{}.{}'.format(server.local_bind_port,records_database_name,record_name) 
    spark = SparkSession \
            .builder \
            .appName(record_name) \
            .config("spark.mongodb.input.uri",
                    input_uri) \
            .config("spark.jars.packages", 
                    "org.mongodb.spark:mongo-spark-connector_2.12:3.0.0") \
            .getOrCreate()
    return spark, pipeline

def spark_work(spark, pipeline, record_name):
    DF = spark.read.format("mongo").option("pipeline", pipeline).load()
    
    frame_count = {"frame_count": DF.count()}
    traffic = objectQuery(trafficLight(DF), "traffic_light")
    Objects = objectStat(DF)
    pedestrian = objectQuery(Objects, "PEDESTRIAN")
    vehicle = objectQuery(Objects, "VEHICLE")
    bicycle = objectQuery(Objects, "BICYCLE")
    object_encounter_count = {"object_encounter_count": 
                              pedestrian["pedestrian_count"] + vehicle["vehicle_count"] + bicycle["bicycle_count"]}
        
    return dict(traffic, **pedestrian, **vehicle, **bicycle, **frame_count, **object_encounter_count)



if __name__ == "__main__":
    from mongo_manager import MongoDB

    mongo = MongoDB("../cfg/fudan.json")
    records_list = mongo.name_records()
    print(records_list)
    spark_list = mongo.name_spark()
    print(spark_list)

    # res = mongo.client.spark[spark_list[0]].find_one()
    # # print(res)

    for record_name in records_list:
        print(mongo.records_database_name, record_name)
        spark, pipeline = init_spark(mongo.server, mongo.records_database_name, record_name)
        spark_res = spark_work(spark, pipeline, record_name)
        spark.stop()


        print(spark_res)
        # spark_table = mongo.client.spark[record_name]
        # spark_table.insert_one(spark_res)
        
    
    mongo.close()


