# SPARK_FLASK

#### 介绍
根据apollo项目将record转化成json文件，发送给前端网页渲染。
<!-- ![效果图](assets/default.gif) -->

#### 主要工作文件

  * [server.py](server.py)  作为flask服务器与前端网页交互
  * [record_reader.py](record_reader.py) 与mongodb交互，读取数据
  * [record_worker.py](record_worker.py) 与mongodb交互，读取json格式数据，连同spark解析结果一起存储到数据库
  * [query.py](util/query.py)  spark工作模块
  * [mongo_manager.py](util/mongo_manager.py)  连接mongodb的模块
  * [default.cfg](cfg/default.cfg)  默认的连接mongodb的配置，需要修改host，user,pwd三个参数

#### 目录结构

    .
    ├── assets                 # 效果图片
    ├── cfg                    # 配置文件，用于连接mongodb
    ├── datas                  # 放置json格式的record文件
    ├── docker                 # 生成镜像，制作docker容器的脚本
    ├── util                   # 经常被调用的python模块
    └── README.md              # readme



#### 服务器端接口说明

见[API_interface.md](API_interface.md)




#### 完整步骤

1. 下载压缩后的datas目录，里面放置了两个测试用json格式record文件。
```
链接：https://pan.baidu.com/s/1jMfC484-7by6HnR4WaV_PA 提取码：5o4l 
```
2. 搭建mongodb数据库环境，测试可用

```
# 启动mongo容器
sudo bash docker/dev_mongo.sh start
```
3. 修改配置文件，

[default.cfg](cfg/default.cfg)
```json
{
    "host":"主机host", 
    "port":27017,
    "user":"主机的用户名",
    "pwd":"主机密码",
    "records_database":"records",
    "spark_database":"spark" 
}
```
其中，host,user,pwd按照部署mongodb数据库的主机进行修改，如：
```json
{
    "host":"192.168.200.201", 
    "port":27017,
    "user":"root",
    "pwd":"admin",
    "records_database":"records",
    "spark_database":"spark" 
}
```


4. 启动spark_server容器
```
sudo bash docker/dev_start.sh start
```
5. 将record和解析结果写入数据库
```
#进入spark_server容器
sudo bash docker/dev_into.sh
python record_worker.py
```

6. 继续停留在spark_server容器内，运行读取程序，测试是否写入成功
```
python record_worker.py
```

7. 启动网页