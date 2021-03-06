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
  * [default.json](cfg/default.json)  默认的连接mongodb的配置，需要修改host，user,pwd三个参数

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




#### 单独使用docker完整步骤（volume模式，与k8s-copy模式冲突）

1. 下载压缩后的datas目录，里面放置了两个测试用json格式record文件。目录路径与cfg,docker,目录同级。
```
链接：https://pan.baidu.com/s/1jMfC484-7by6HnR4WaV_PA 提取码：5o4l
```
2. 搭建mongodb数据库环境，测试可用

```
# 启动mongo容器
sudo bash docker/dev_mongo.sh start
```

3. 启动spark_server容器
```
sudo bash docker/dev_start.sh start
```
4. 将record和解析结果写入数据库
```
#进入spark_server容器
sudo bash docker/dev_into.sh
# 运行写入程序，将数据写入数据库
python record_worker.py
# 运行读取程序，测试是否写入成功
python record_reader.py
```

5. 启动网页

#### 基于k8s完整步骤

1. 拉取spark镜像353942829/spark
```
sudo docker pull 353942829/spark
```

2. 启动pod，分别在3台机器上进行了测试。机器A在国内并搭建了VPN，机器B在国内没有搭VPN，设置了杭州阿里云镜像库，机器C在美国。

  * [k8s_host.yaml](k8s/k8s_host.yaml) host模式，对于ABC都能成功。
```
sudo kubectl apply -f k8s/k8s_host.yaml
```
  * [k8s_port.yaml](k8s/k8s_port.yaml) 端口映射模式,需要翻墙。在翻墙的机器A和美国的服务器C成功了，设置杭州阿里云镜像库的那台机器B一直pending，原因未明。
```
sudo kubectl apply -f k8s/k8s_port.yaml
```

或者单独启动各个容器
  * 修改[spark_volume.yaml](k8s/spark_volume.yaml)中的hostpath，修改为当前项目在主机中的绝对地址。 单独启动spark
```
sudo kubectl apply -f k8s/spark_volume.yaml
```
  * [mongo.yaml](k8s/mongo.yaml) 单独启动mongo容器
```
sudo kubectl apply -f k8s/mongo.yaml
```

3. 进入spark容器,并将数据写入数据库
```
#进入spark_server容器
sudo kubectl exec -it apollo bash
# 运行写入程序，将数据写入数据库
python record_worker.py
# 运行读取程序，测试是否写入成功
python record_reader.py


