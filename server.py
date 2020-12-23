import flask
from flask import Flask,url_for,render_template,request,redirect,send_file,jsonify,g
from flask_cors import *


# from pyspark.sql import SparkSession
from util.query import query
from util.solve_json import get_datas,read_json

app = Flask(__name__)
CORS(app, supports_credentials=True)

records_path = "datas"
jsons = get_datas(records_path)
# spark = SparkSession.builder.appName('spark').getOrCreate()
query_res = read_json("query_res.json")

@app.route('/api_spark_search' , methods=['POST'])
def api_spark_search():
    ret_json = query_res
    return jsonify(ret_json)


@app.route('/api_request_frame' , methods=['POST'])
def api_request_frame():
    record_name = request.form["record_name"]
    frame_start = int(request.form['frame_start'])
    frame_end = int(request.form['frame_end'])
    # print(record_name,frame_start,frame_end)
    ret_json = jsons[record_name][frame_start:frame_end]
    return jsonify(ret_json)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=7010,threaded=True)
