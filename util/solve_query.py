import json

def get_value(word,json):
    words = ["traffic_light","pedestrian","vehicle","bicycle"]
    if word not in words:
        return 201,"Error,word must be in " + words
    
    time_key = word + "_time"
    count_key = word + "_count"

    ret_json = {key:json[key] for key in [time_key, count_key]}
    ret_json[time_key].sort(key=lambda x:x["start_frameID"])

    return ret_json

if __name__ == "__main__":
    from solve_json import read_json
    data = read_json("query_res.json")
    print(data["1.json"].keys())
    data_0 = data["1.json"]

    word = "vehicle"
    time_key = word + "_time"
    part_data = get_value(word,data_0)
    
    print(json.dumps(part_data, indent=4, sort_keys=True))