import flask
from flask import Flask,url_for,render_template,request,redirect,send_file,jsonify,g
from flask_cors import *
import os


from record_reader import Record_Reader

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.config["cfg_file"] = "cfg/default.json"
app.config["record_reader"] = Record_Reader(app.config["cfg_file"])

@app.route('/api_get_records_array' , methods=['GET'])
def api_get_records_array():
    records_name = app.config["record_reader"].records_name()
    return jsonify(records_name)

@app.route('/api_spark_search' , methods=['POST'])
def api_spark_search():
    sort_key = request.form["sort_key"]
    spark_merge_res = app.config["record_reader"].get_spark_merge_res(sort_key)
    return jsonify(spark_merge_res)


@app.route('/api_request_frame' , methods=['POST'])
def api_request_frame():
    record_name = request.form["record_name"]
    frame_start = int(request.form['frame_start'])
    frame_end = int(request.form['frame_end'])
    frames = app.config["record_reader"].get_frames(record_name,frame_start,frame_end) # type <list>
    return jsonify(frames)


if __name__ == '__main__':
    app.run()
    # app.run(debug=False, host='0.0.0.0', port=7010,threaded=True)
