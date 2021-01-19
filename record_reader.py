import json
import time
import os
from util import read_json,write_json,MongoDB,init_spark,spark_work
from bson import json_util


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

        # ObjectId can not trans to json-dict
        frames = json.loads(json_util.dumps(frames))

        return frames
    
    def records_name(self):
        return self.mongo.name_records()

    def get_spark_res(self,record_name):
        spark_table = self.mongo.get_spark_table(record_name)
        spark_res = spark_table.find_one()
        spark_res.pop('_id')
        return spark_res
    
    def get_spark_merge_res(self,key_word):
        spark_table = self.mongo.get_spark_merge_table()
        spark_merge_res = list(spark_table.find().sort(key_word))
        for spark_res in spark_merge_res:
            spark_res.pop('_id')
        return spark_merge_res



if __name__ == "__main__":
    cfg_file = "cfg/default.json"
    recorder_reader = Record_Reader(cfg_file)
    records_name = recorder_reader.records_name()
    for record_name in records_name:
        # get frames_num
        frames_num = recorder_reader.get_frames_num(record_name)
        print(frames_num)

        # # get spark result
        # spark_res = recorder_reader.get_spark_res(record_name) # type(dict)
        # print(spark_res.keys())
        # # print(json.dumps(spark_res, indent=4))

        # # get frames by frame num
        frames = recorder_reader.get_frames(records_name[0],0,1)
        # print(json.dumps(frames,indent=4))
        print(frames[0].keys())
    
    sort_words = ['vehicle_count','traffic_light_count','pedestrian_count','bicycle_count']
    sort_idx = 0

    print("-----{}------".format(sort_words[sort_idx]))
    spark_merge_res = recorder_reader.get_spark_merge_res(sort_words[sort_idx])
    for spark_res in spark_merge_res:
        show_res = {
            "record_name":spark_res["record_name"],
            sort_words[sort_idx]:spark_res[sort_words[sort_idx]]
        }
        print(json.dumps(show_res,indent=4))

    recorder_reader.close_connnection()
