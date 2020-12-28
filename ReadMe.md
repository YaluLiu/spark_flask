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

#### 目录结构

    .
    ├── assets                 # 效果图片
    ├── cfg                    # 配置文件，用于连接mongodb
    ├── datas                  # 放置json格式的record文件
    ├── docker                 # 生成镜像，制作docker容器的脚本
    ├── util                   # 经常被调用的python模块
    └── README.md              # readme


mask.npy 可由[show_mask.py](tools/show_mask.py)显示

#### mongo配置文件
```json
{
    "host":"localhost",
    "port":27017,
    "user":"你的用户名",
    "pwd":"你的密码",
    "records_database":"records",
    "spark_database":"spark" 
}
```
*  非特殊情况下,只有host,user,pwd需要修改，设置为自己部署的mongodb参数.

#### mongodb搭建方法（下面为在本机搭建mongodb）

```
# 下载mongo镜像
sudo bash docker/dev_mongo.sh create
# 启动docker容器
sudo bash docker/dev_mongo.sh start
# 清空
sudo bash docker/dev_mongo.sh clean
```
搭建好数据库环境后，使用[record_worker.py](record_worker.py)写入数据库，使用[record_reader.py](record_reader.py)测试是否能够成功读取

#### docker脚本使用方法

```
# 创建spark_sever镜像
sudo bash docker/dev_start.sh create
# 启动spark_sever容器
sudo bash docker/dev_start.sh start
# 清空spark_sever容器
sudo bash docker/dev_start.sh clean
```

#### 完整步骤

1. 搭建mongodb数据库环境，测试可用
2. 启动spark容器
3. 启动前端网页