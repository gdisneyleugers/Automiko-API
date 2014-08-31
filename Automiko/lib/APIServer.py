__author__ = 'gregorydisney'
from flask import Flask
import zerorpc

c = zerorpc.Client()
c.connect("tcp://127.0.0.1:8888")

app = Flask(__name__)

@app.route("/")
def index():
    a = c.help()
    return a

@app.route("/help/<cmd>")
def cmd_help(cmd):
    a = c.cmd_help(cmd)
    if cmd == "":
        a = c.help()
        return a
    return a

@app.route("/key_cmd/<key>/<cmd>")
def key_cmd(key, cmd):
    a = c.key_cmd(key, cmd)
    return a

@app.route("/file_exec/<script>/<test_name>/<result_query>/<test_detail>/<log_file>")
def file_exec(script, test_name, result_query, test_detail, log_file):
    a = c.file_exec(script, test_name, result_query, test_detail, log_file)
    return a

@app.route("/key_exec/<key>/<test_name>/<result_query>/<test_detail>/<log_file>")
def key_exec(key, test_name, result_query, test_detail, log_file):
    a = c.key_exec(key, test_name, result_query, test_detail, log_file)
    return a

@app.route("/schedule_key_exec/<key>/<test_name>/<result_query>/<test_detail>/<exec_time>/<log_file>")
def schedule_key_exec(key, test_name, result_query, test_detail, exec_time, log_file):
    a = c.schedule_key_exec(key, test_name, result_query, test_detail, exec_time, log_file)
    return a

@app.route("/schedule_file_exec/<script>/<test_name>/<result_query>/<test_detail>/<exec_time>/<log_file>")
def schedule_file_exec(script, test_name, result_query, test_detail, exec_time, log_file):
    a = c.schedule_file_exec(script, test_name, result_query, test_detail, exec_time, log_file)
    return a

@app.route("/remote_key_exec/<key>/<test_name>/<result_query>/<test_detail>/<log_file>")
def remote_key_exec(key, test_name, result_query, test_detail, log_file):
    a = c.remote_key_exec(key, test_name, result_query, test_detail, log_file)
    return a

@app.route("/remote_file_exec/<script>/<test_name>/<result_query>/<test_detail>/<log_file>")
def remote_file_exec(script, test_name, result_query, test_detail, log_file):
    a = c.remote_exec_file(script, test_name, result_query, test_detail, log_file)
    return a

@app.route("/tally_count/<logfile>/<resultfile>")
def tally_count(logfile, resultfile):
    a = c.tally_count(logfile, resultfile)
    return a

if __name__ == "__main__":
    app.run(port=8080)
