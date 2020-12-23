from pymongo import MongoClient
from sshtunnel import SSHTunnelForwarder
import json

MONGO_HOST = "192.168.200.45"
MONGO_DB = "DATABASE_NAME"
MONGO_USER = "boli"
MONGO_PASS = "123456"


def get_conn():
    server = SSHTunnelForwarder(
        MONGO_HOST,
        ssh_username=MONGO_USER,
        ssh_password=MONGO_PASS,
        remote_bind_address=('127.0.0.1', 27017)
    )

    server.start()
    client = MongoClient('mongodb://localhost:' + str(server.local_bind_port) + '/')
    server.stop()

def save_records(client,file_name):
    records = client.apollo.records

    with open(file_name) as f:
        file_data = json.load(f)
        new_json = {}
        new_json["record_name"] = "1.json"
        new_json["frames"] = file_data
        records.insert_one(new_json)


def search(client):
    mycol = client["apollo"]["records"]

    datas = mycol.find()
    print(datas.count())

    for x in datas:
        print(x.keys())
        print(x["record_name"])
        print(len(x["frames"]))


if __name__ == "__main__":
    server = SSHTunnelForwarder(
        MONGO_HOST,
        ssh_username=MONGO_USER,
        ssh_password=MONGO_PASS,
        remote_bind_address=('127.0.0.1', 27017)
    )

    server.start()
    client = MongoClient('mongodb://localhost:' + str(server.local_bind_port) + '/')
    
    # save_records(client,"datas/1.json")


    search(client)

    client.close()
    server.stop()

    