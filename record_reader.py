import json
import time
import os
from util import read_json,write_json,MongoDB,init_spark,spark_work



class Record_Reader():
    def __init__(self, cfg_file):
        self.mongo = MongoDB(cfg_file)

    def close_connnection(self):
        self.mongo.close()

    def get_frames_num(self,record_name):
        record_table = self.mongo.get_record_table(record_name)
        return record_table.count()

    def get_frames(self,record_name,start,end):
        '''
        record_name:  name of record file, except the file-suffix
        start: the start of frame num, include start frame
        end:   the end of frame num, include end frame
        '''
        record_table = self.mongo.get_record_table(record_name)

        frames = record_table.find({"sequenceNum":{'$gte': start,'$lte': end}}) # type <class 'pymongo.cursor.Cursor'>
        frames = list(frames)
        print(len(frames))
        print(frames[0].keys())

        return frames
    
    def records_name(self):
        return self.mongo.name_records()

    def get_spark_res(self,record_name):
        spark_table = self.mongo.get_spark_table(record_name)
        spark_res = spark_table.find_one()
        return spark_res



if __name__ == "__main__":
    cfg_file = "cfg/fudan.json"
    recorder_reader = Record_Reader(cfg_file)
    records_name = recorder_reader.records_name()
    for record_name in records_name:
        # get frames_num
        frames_num = recorder_reader.get_frames_num(record_name)
        print(frames_num)

        # get spark result
        spark_res = recorder_reader.get_spark_res(record_name)
        # print(spark_res)
        print(json.dumps(spark_res, indent=2))

        # get frames by frame num
        # frames = recorder_reader.get_frames(records_name[0],10,12)
        # print (frames)
    
    recorder_reader.close_connnection()
