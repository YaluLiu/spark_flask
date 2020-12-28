import sys
sys.path.append("..")
from util.solve_json import read_json

from pymongo import MongoClient
from bson.objectid import ObjectId 
from sshtunnel import SSHTunnelForwarder
import json

class MongoDB():
    def __init__(self,cfg_file):
        cfg = read_json(cfg_file)
        self.host = cfg["host"]
        self.port = cfg["port"]

        self.user = cfg["user"]
        self.pwd = cfg["pwd"]

        self.records_database_name = cfg["records_database"]
        self.spark_database_name = cfg["spark_database"]
        self.connect()

    def connect(self):
        self.server = SSHTunnelForwarder(
            self.host,
            ssh_username=self.user,
            ssh_password=self.pwd,
            remote_bind_address=('127.0.0.1', self.port)
        )
        self.server.start()
        self.client = MongoClient('mongodb://localhost:' + str(self.server.local_bind_port) + '/')
    
    def records_database(self):
        return self.client[self.records_database_name]

    def spark_database(self):
        return self.client[self.spark_database_name]

    def name_records(self):
        """
        return all names of records
        """
        return self.records_database().collection_names()

    def name_spark(self):
        """
        return all names of statistic
        """
        return self.spark_database().collection_names()

    def get_record_table(self,record_name):
        return self.records_database()[record_name]

    def get_spark_table(self,record_name):
        return self.spark_database()[record_name]
    
    def get_spark_merge_table(self):
        return self.spark_database()["sparks"]

    def get_table(self,record_name):
        return self.get_record_table(record_name), \
            self.get_spark_table(record_name)

    def clean(self):
        """
        delete all the tables
        """
        for record_name in self.name_records():
            self.records_database()[record_name].drop()
        for record_name in self.name_spark():
            self.spark_database()[record_name].drop()


    def close(self):
        self.client.close()
        self.server.stop()


