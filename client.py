# -*- coding: UTF-8 -*-
import json
import requests
import threading
import time
import os
from pprint import pprint

port = 7010
host = "localhost"

# host = "http://flower-boli0.tpddns.cn"
# port = 58888
def get_frame_by_num(record_id,frame_start,frame_end):
    interface = "api_request_frame"
    post_url = "http://{}:{}/{}".format(host,port, interface)

    # 发送的数据
    send_data = {"record_name":"record_35",
                "frame_start":frame_start,
                "frame_end":frame_end}
    
    jsondata = requests.post(post_url,data=send_data)

    if(jsondata.status_code == 200):
        return jsondata.json()
    else:
        return None


def spark_search(sort_key):
    interface = "api_spark_search"
    post_url = "http://{}:{}/{}".format(host,port, interface)

    send_data = {"sort_key":sort_key}

    # 发送的数据,send_data目前没用
    jsondata = requests.post(post_url,data=send_data)

    if(jsondata.status_code == 200):
        return jsondata.json()
    else:
        return None

def get_all_records_name():
    interface = "api_get_records_array"
    post_url = "http://{}:{}/{}".format(host,port, interface)
    jsondata = requests.get(post_url)
    if(jsondata.status_code == 200):
        return jsondata.json()
    else:
        return None

if __name__ == '__main__':
    # 发送的数据
    words = ["traffic_light","pedestrian","vehicle","bicycle"]

    # 获取所有的record名称
    name_records = get_all_records_name()
    print('--------{}------'.format("(records_name)"))
    print(name_records)

    # 获取所有的spark检索结果，按sort_key排序
    for sort_idx in range(0,len(words)):
        sort_key = words[sort_idx] + "_count"
        results = spark_search(sort_key)
        print('--------{}------'.format(sort_key))
        for result in results:
            print(result[sort_key],end = " ")
        print()


    # 按帧的起始号获取帧的内容
    print('--------{}------'.format("(frames_list)"))
    frame_start = 10
    frame_end = 12
    frames = get_frame_by_num(None,frame_start,frame_end)
    print(len(frames))
    print(frames[0].keys())
    for frame in frames:
        print(frame["_id"])
        
