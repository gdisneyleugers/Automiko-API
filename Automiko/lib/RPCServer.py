import Execute as Execute

__author__ = 'gregorydisney'
import zerorpc


class ServerCmd(object):
    def key_exec(self, key, test_name, result_query, test_detail, log_file):
        stdout = Execute.exec_key(key=key, test_name=test_name, result_query=result_query, test_detail=test_detail, log_file=log_file, host="localhost", port=6379, db=0)
        data = "{0}".format(stdout)
        d = data.replace('\\n', " ")
        return d

    def file_exec(self, script, test_name, result_query, test_detail, log_file):
        stdout = Execute.exec_file(script=script, test_name=test_name, result_query=result_query, test_detail=test_detail, log_file=log_file)
        data = "{0}".format(stdout)
        d = data.replace('\\n', " ")
        return d

    def key_cmd(self, key, cmd):
        stdout = Execute.key_cmd(key=key, cmd=cmd, host="localhost", port=6379, db=0)
        return stdout

    def schedule_key_exec(self, key, test_name, result_query, test_detail, exec_time, log_file):
        stdout = Execute.schedule_exec_key(key=key, test_name=test_name, result_query=result_query, test_detail=test_detail, exec_time=exec_time, log_file=log_file, host="0.0.0.0", port=6379, db=0)
        data = "{0}".format(stdout)
        d = data.replace('\\n', " ")
        return d

    def schedule_exec_file(self, script, test_name, result_query, test_detail, exec_time, log_file):
        stdout = Execute.schedule_exec_file(script=script, test_name=test_name, result_query=result_query, test_detail=test_detail, exec_time=exec_time, log_file=log_file)
        data = "{0}".format(stdout)
        d = data.replace('\\n', " ")
        return d

    def remote_key_exec(self, key, test_name, result_query, test_detail, log_file):
        dbhost  = "127.0.0.1"
        dbport = 6379
        dbnum = 0
        host = Execute.db_get("host", dbhost, dbport, dbnum)
        port = Execute.db_get("port", dbhost, dbport, dbnum)
        user = Execute.db_get("user", dbhost, dbport, dbnum)
        password = Execute.db_get("password", dbhost, dbport, dbnum)
        stdout = Execute.remote_exec_key(key, host=host, port=int(port), user=user, password=password, test_name=test_name, result_query=result_query, test_detail=test_detail, log_file=log_file, db_host=dbhost, db_port=dbport, db=dbnum)
        print stdout
        data = "{0}".format(stdout)
        d = data.replace('\\n', " ")
        return d

    def remote_exec_file(self, script, test_name, result_query, test_detail, log_file):
        host = Execute.db_get("host", "localhost", 6379, 0)
        port = Execute.db_get("port", "localhost", 6379, 0)
        user = Execute.db_get("user", "localhost", 6379, 0)
        password = Execute.db_get("password", "localhost", 6379, 0)
        stdout = Execute.remote_exec_file(script, host=host, port=int(port), user=user, password=password, test_name=test_name, result_query=result_query, test_detail=test_detail, log_file=log_file)
        data = "{0}".format(stdout)
        d = data.replace('\\n', " ")
        return d

    def set_user(self, user):
        stdout = Execute.set_user(user, db_host="localhost", port=6379, db=0)
        data = "{0}".format(stdout)
        d = data.replace('\\n', " ")
        return d

    def set_host(self, host):
        stdout = Execute.set_remote_host(host, db_host="localhost", db_port=6379, db=0)
        data = "{0}".format(stdout)
        d = data.replace('\\n', " ")
        return d

    def set_password(self, password):
        stdout = Execute.set_user_pass(password, db_host="localhost", port=6379, db=0)
        data = "{0}".format(stdout)
        d = data.replace('\\n', " ")
        return d

    def set_port(self):
        stdout = Execute.set_remote_port(db_host="localhost", db_port="6379", db=0)
        data = "{0}".format(stdout)
        d = data.replace('\\n', " ")
        return d

    def tally_count(self, logfile, resultfile, test_pass=True, test_fail=True):
        stdout = Execute.tally_counter(logfile, resultfile, test_pass=True, test_fail=True)
        data = "{0}".format(stdout)
        d = data.replace('\\n', " ")
        return d

    def help(self):
        a = "Available commands: key_exec, file_exec, key_cmd, schedule_key_exec, schedule_exec_file, cmd_help, remote_file_exec, remote_key_exec, tally_count, schedule_remote_key_exec, schedule_remote_file_exec"
        return a

    def cmd_help(self, cmd):
        if cmd in "key_exec":
            a = "key_exec/'key'/'test_name'/'result_query'/'test_detail'/'log_file'"
            return a
        if cmd in "file_exec":
            a = "file_exec/'script'/'test_name'/'result_query'/'test_detail'/'log_file'"
            return a
        if cmd in "key_cmd":
            a = "key_cmd/'key'/'cmd'"
            return a
        if cmd in "schedule_key_exec":
            a = "schedule_key_cmd/'key'/'test_name'/'result_query'/'test_detail'/'exec_time'/'log_file'"
            return a
        if cmd in "schedule_key_exec":
            a = "schedule_key_exec/'key'/'test_name'/'result_query'/'test_detail'/'exec_time'/'log_file'"
            return a
        if cmd in "remote_file_exec":
            a = "remote_file_exec/'script'/'test_name'/'result_query'/'test_detail'/'log_file'"
            return a
        if cmd in "remote_key_exec":
            a = "remote_key_exec/'key'/'test_name'/'result_query'/'test_detail'/'log_file'"
            return a
        if cmd in "schedule_remote_key_exec":
            a = "remote_key_exec/'key'/'test_name'/'result_query'/'test_detail'/'exec_time'/log_file'"
            return a
        if cmd in "schedule_remote_file_exec":
            a = "remote_key_exec/'script'/'test_name'/'result_query'/'test_detail'/'exec_time'/log_file'"
            return a
        else:
            a = "command not know, Available commands: key_exec, file_exec, key_cmd, schedule_key_exec, schedule_exec_file, cmd_help"
            return a

s = zerorpc.Server(ServerCmd())
s.bind("tcp://0.0.0.0:8888")
s.run()