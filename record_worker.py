import json
import time
import os
from util import read_json,write_json,MongoDB,init_spark,spark_work



class Record_Worker():
    def __init__(self,dir_path,cfg_file):
        self.dir_path = dir_path
        self.list_records = os.listdir(self.dir_path)
        self.mongo = MongoDB(cfg_file)


    def save_record(self,record_name,record_path):
        record_table = self.mongo.get_record_table(record_name)

        with open(record_path) as f:
            frames = json.load(f)
            record_table.insert_many(frames)

    def save_records(self):
        '''
        by the new directory,get all the new records
        '''
        for file_name in self.list_records:
            record_name = file_name.split(".")[0]
            record_path = os.path.join(self.dir_path,file_name)
            self.save_record(record_name,record_path)
    
    def spark_solve(self):
        for file_name in self.list_records:
            record_name = file_name.split(".")[0]
            spark, pipeline = init_spark(self.mongo.port, self.mongo.records_database_name, record_name)
            spark_res = spark_work(spark, pipeline, record_name)
            spark.stop()
            print(spark_res.keys())

            spark_table = self.mongo.get_spark_table(record_name)
            spark_table.insert_one(spark_res)

            spark_merge_table = self.mongo.get_spark_merge_table()
            spark_res["record_name"] = record_name
            spark_merge_table.insert_one(spark_res)

    
    def clean(self):
        """
        clean all the tables,and check
        """
        self.mongo.clean()
        print(self.mongo.name_records())
        print(self.mongo.name_spark())

    def close_connnection(self):
        self.mongo.close()



if __name__ == "__main__":
    dir_path = "datas"
    cfg_file = "cfg/default.json"
    record_worker = Record_Worker(dir_path,cfg_file)
    record_worker.clean()

    print("start to save-record into mongo db.records")
    record_worker.save_records()

    print("start to spark-parse by record frames, and save to db.spark")
    record_worker.spark_solve()

    print(record_worker.mongo.name_records())
    print(record_worker.mongo.name_spark())

    record_worker.close_connnection()

