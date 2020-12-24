# -*- coding: UTF-8 -*-
import json
import requests
import threading
import time
import os
from pprint import pprint


def get_frame_by_num(record_id,frame_start,frame_end):
    interface = "api_request_frame"
    port = 7010
    # host = "149.129.55.32"
    host = "192.168.200.45"
    #post网址 http://localhost:7010/api_request_frame
    # http://149.129.55.32:7010/api_request_frame
    post_url = "http://{}:{}/{}".format(host,port, interface)


    # 发送的数据
    send_data = {"record_name":"1.json",
                "frame_start":frame_start,
                "frame_end":frame_end}
    
    jsondata = requests.post(post_url,data=send_data)

    if(jsondata.status_code == 200):
        return jsondata.json()
    else:
        return None


def spark_search():
    interface = "api_spark_search"
    port = 7010
    # host = "localhost"
    host = "149.129.55.32"
    #post网址 http://localhost:7010/api_spark_search
    # http://149.129.55.32:7010/api_spark_search
    post_url = "http://{}:{}/{}".format(host,port, interface)


    # 发送的数据,send_data目前没用
    send_data = {}
    jsondata = requests.post(post_url,data=send_data)

    if(jsondata.status_code == 200):
        return jsondata.json()
    else:
        return None

if __name__ == '__main__':

    i = 1
    while True:
        record_id = 1
        frame_start = i
        frame_end = i + 1
        data = get_frame_by_num(record_id,frame_start,frame_end)
        # data = json.dumps(data, sort_keys=True, indent=4, separators=(',', ':'))
        print(i,len(data))

        i += 1
        if i == 198:
            print("haha")
            i = 0


    # result = spark_search()
    # for first_key in result.keys():
    #     print(json.dumps(result[first_key],indent=4))
    #     break
