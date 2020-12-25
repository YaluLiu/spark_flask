import json
import time
import os
from util import read_json,write_json,MongoDB,init_spark,spark_work



class Record_Worker():
    def __init__(self,dir_path,cfg_file):
        self.dir_path = dir_path
        self.mongo = MongoDB(cfg_file)

    def save_record(self,record_name,record_path):
        record_table = self.mongo.get_record_table(record_name)

        with open(record_path) as f:
            frames = json.load(f)
            for frame in frames:
                record_table.insert_one(frame)

    def save_records(self):
        '''
        by the new directory,get all the new records
        '''
        self.list_records = os.listdir(self.dir_path)
        for file_name in self.list_records:
            record_name = file_name.split(".")[0]
            record_path = os.path.join(self.dir_path,file_name)
            self.save_record(record_name,record_path)
    
    def spark_solve(self):
        for record_name in self.list_records:
            spark, pipeline = init_spark(self.mongo.server, record_name)
            spark_res = spark_work(spark, pipeline, record_name)
            spark.stop()

            spark_table = self.mongo.get_spark_table(record_name)
            spark_table.insert_one(spark_res)
    
    def start(self):
        print("start to save-record")
        self.save_records()

        print("start to spark-parse")
        self.spark_solve()

        print(self.mongo.name_records())
        print(self.mongo.name_spark())
    
    def clean(self):
        """
        clean all the tables,and check
        """
        self.mongo.clean()
        print(self.mongo.name_records())
        print(self.mongo.name_spark())

    def stop(self):
        self.mongo.close()



if __name__ == "__main__":
    dir_path = "datas"
    cfg_file = "cfg/fudan.json"
    record_worker = Record_Worker(dir_path,cfg_file)
    record_worker.clean()

    record_worker.start()

    record_worker.stop()

