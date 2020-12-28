### REST API列表

API                      | 接口类型 |输入参数          | 参数格式| 返回格式         |  说明
-----------------------  | -----   | -----            |-----   | -----           | ----- 
[api_get_records_array]  | GET     |无                 |  无   |  string_array      | 获取所有已存储的record文件
[api_spark_search]       | POST    | 排序关键词        |  json  |  json_array     | 获取spark的统计结果
[api_request_frame]      | POST    | record名+帧起始号 |  json  |  json_array      | 获取帧的内容


#### api_spark_search
```
{"sort_key":"traffic_light_count"}
```
从下面4个关键词中选择一个，作为排序的关键词
```
["traffic_light_count","pedestrian_count","vehicle_count","bicycle_count"]
```


#### api_request_frame
```
{
    "record_name":"record_35",
    "frame_start":100,
    "frame_end":120
}
```

获取record_35文件中，第100帧到第120帧的内容，包含第100帧和第120帧