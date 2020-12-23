import json
import os 

def read_json(json_file):
    with open(json_file,"r") as fp:
        data = json.load(fp)
    return data


def write_json(data,json_file):
    with open(json_file, 'w') as fp:
        json.dump(data, fp, indent=4)


def get_datas(data_path):
    files = []
    ret_datas = {}

    for file in os.listdir(data_path):
        if not os.path.isdir(file): 
            file_path = os.path.join(data_path,file)
            ret_datas[file] = read_json(file_path)
    return ret_datas



if __name__ == "__main__":
    data_path = "datas"
    datas = get_datas(data_path)
    print(datas.keys())
    data = datas["1.json"]
    print(len(data),type(data))