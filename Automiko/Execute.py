__author__ = 'gregorydisney'
import os
import redis
import time
import paramiko
from scp import SCPClient
import socket

class Backend:
    def __init__(self):
        pass
        return


def test_logger(logfile, test_name, start, stop, result):
    os.system("touch {0}".format(logfile))
    logger = open(logfile, "a")
    test_results = test_name + " Start @ " + start + " Stop @" + stop + " " + result + "\n"
    logger.write(test_results)


def db_connect(host, port, db):
    r = redis.StrictRedis(host=host, port=port, db=db)
    return r

def key_cmd(key, cmd, host, port, db):
    r = db_connect(host, port, db)
    r.set(key, cmd)
    print "saved " + key + " @ " + cmd


def db_get(key, host, port, db):
    r = db_connect(host, port, db)
    keys = r.get(key)
    return keys


def exec_key(key, test_name, result_query, test_detail, log_file, host, port, db):
    start = time.asctime()
    try:
        cmd = db_get(key, host, port, db)
        r = os.popen(cmd).read()
        if result_query not in r:
            print "Failed {0}\n".format(test_name)
            print "Test detail: \n" + test_detail + "\n"
            print "Result: " + r + "\n"
            stop = time.asctime()
            test_result = "Fail"
            test_logger(log_file, test_name, start, stop, test_result)
        if result_query in r:
            print "Pass {0}\n".format(test_name)
            print "Test detail: \n" + test_detail + "\n"
            print "Result: \n" + r + "\n"
            stop = time.asctime()
            test_result = "Pass"
            test_logger(log_file, test_name, start, stop, test_result)
    except TypeError:
        print "Key doesn't exist in DB"


def exec_file(script, test_name, result_query, test_detail, log_file):
    start = time.asctime()
    chmod = os.popen("chmod +x ./{0}".format(script)).read()
    if ":sh" in chmod:
        print "Failed to chmod\n"
        stop = time.asctime()
        test_result = "Fail"
        test_logger(log_file, "Chmod", start, stop, test_result)
    if ":sh" not in chmod:
        print "Pass chmod {0}".format(test_name)
        stop = time.asctime()
        test_result = "Pass"
        test_logger(log_file, "Chmod", start, stop, test_result)
    cmd = os.popen("./{0}".format(script)).read()
    if result_query not in cmd:
        print "Failed {0}\n".format(test_name)
        print "Test detail: \n" + test_detail + "\n"
        print "Result: \n" + cmd + "\n"
        stop = time.asctime()
        test_logger(log_file, test_name, start, stop, "Fail")
    if result_query in cmd:
        print "Pass {0}".format(test_name)
        print "Test detail: \n" + test_detail + "\n"
        print "Result: \n" + cmd + "\n"
        stop = time.asctime()
        test_logger(log_file, test_name, start, stop, "Pass")


def schedule_exec_key(key, test_name, result_query, test_detail, exec_time, log_file, host, port, db):
    start = time.asctime()
    if exec_time in time.asctime():
        try:
            cmd = cmd = db_get(key, host, port, db)
            r = os.popen(cmd).read()
            if result_query not in r:
                print "Failed {0}\n".format(test_name)
                print "Test detail: \n" + test_detail + "\n"
                print "Result: " + r + "\n"
                stop = time.asctime()
                test_logger(log_file, test_name, start, stop, "Pass")
            if result_query in r:
                print "Pass {0}\n".format(test_name)
                print "Test detail: \n" + test_detail + "\n"
                print "Result: " + r + "\n"
                stop = time.asctime()
                test_logger(log_file, test_name, start, stop, "Pass")
        except TypeError:
            print "Key doesn't exist in DB"
    else:
          print "{0} ".format(test_name) + "Will run next @ {0}".format(exec_time)
          stop = time.asctime()
          test_logger(log_file, test_name, start, stop, "Command Deferred")


def schedule_exec_file(script, test_name, result_query, test_detail, exec_time, log_file):
    start = time.asctime()
    if exec_time in time.asctime():
        chmod = os.popen("chmod +x ./{0}".format(script)).read()
        if ":sh" in chmod:
            print "Failed to chmod\n"
            stop = time.asctime()
            test_logger(log_file, test_name, start, stop, "Fail")
        if ":sh" not in chmod:
            print "Pass chmod {0}".format(test_name)
            stop = time.asctime()
            test_logger(log_file, test_name, start, stop, "Pass")
        cmd = os.popen("./{0}".format(script)).read()
        if result_query not in cmd:
            print "Failed {0}\n".format(test_name)
            print "Test detail: \n" + test_detail + "\n"
            print "Result: \n" + cmd + "\n"
            stop = time.asctime()
            test_logger(log_file, test_name, start, stop, "fail")
        if result_query in cmd:
            print "Pass {0}".format(test_name)
            print "Test detail: \n" + test_detail + "\n"
            print "Result: \n" + cmd + "\n"
    else:
        print "{0} ".format(test_name) + "Will run next @ {0}".format(exec_time)
        stop = time.asctime()
        test_logger(log_file, test_name, start, stop, "Command Deferred")


def remote_exec_file(script, host, port, user, password, test_name, result_query, test_detail, log_file):
    start = time.asctime()
    cl = paramiko.SSHClient()
    cl.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        cc = cl.connect(host, port=port, username=user, password=password)
    except paramiko.ssh_exception.AuthenticationException:
            print "Auth Error"
    except paramiko.ssh_exception.SSHException:
            print "Protocol Error"
    except paramiko.transport:
            print "General Error"
    except socket.error:
            print "Socket Error"
    scp = SCPClient(cl.get_transport())
    scp.put(script,script)
    cl.exec_command("chmod +x ./{0}".format(script))
    stdin, stdout, stderr =  cl.exec_command("./{0}".format(script))
    a = stdout.readlines()
    cmd = str(a)
    if result_query not in cmd:
        print "Failed {0}\n".format(test_name)
        print "Test detail: \n" + test_detail + "\n"
        print "Result: \n" + cmd + "\n"
        stop = time.asctime()
        test_logger(log_file, test_name, start, stop, "Fail")
    if result_query in cmd:
        print "Pass {0}".format(test_name)
        print "Test detail: \n" + test_detail + "\n"
        print "Result: \n" + cmd + "\n"
        stop = time.asctime()
        test_logger(log_file, test_name, start, stop, "Pass")


def remote_exec_key(key, host, port, user, password, test_name, result_query, test_detail, log_file, db_host, db_port, db):
    start = time.asctime()
    cl = paramiko.SSHClient()
    cl.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        cc = cl.connect(host, port=port, username=user, password=password)
    except paramiko.ssh_exception.AuthenticationException:
            print "Auth Error"
    except paramiko.ssh_exception.SSHException:
            print "Protocol Error"
    except paramiko.transport:
            print "General Error"
    except socket.error:
            print "Socket Error"
    func = db_get(key, db_host, db_port, db)
    stdin, stdout, stderr =  cl.exec_command(func)
    a = stdout.readlines()
    cmd = str(a)
    if result_query not in cmd:
        print "Failed {0}\n".format(test_name)
        print "Test detail: \n" + test_detail + "\n"
        print "Result: \n" + cmd + "\n"
        stop = time.asctime()
        test_logger(log_file, test_name, start, stop, "Fail")
    if result_query in cmd:
        print "Pass {0}".format(test_name)
        print "Test detail: \n" + test_detail + "\n"
        print "Result: \n" + cmd + "\n"
        stop = time.asctime()
        test_logger(log_file, test_name, start, stop, "Pass")


def schedule_remote_exec_file(script, host, port, user, password, test_name, result_query, test_detail, exec_time, log_file):
    start = time.asctime()
    if exec_time in time.asctime():
        cl = paramiko.SSHClient()
        cl.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            cc = cl.connect(host, port=port, username=user, password=password)
        except paramiko.ssh_exception.AuthenticationException:
            print "Auth Error"
        except paramiko.ssh_exception.SSHException:
            print "Protocol Error"
        except paramiko.transport:
            print "General Error"
        except socket.error:
            print "Socket Error"
        scp = SCPClient(cl.get_transport())
        scp.put(script,script)
        cl.exec_command("chmod +x ./{0}".format(script))
        stdin, stdout, stderr =  cl.exec_command("./{0}".format(script))
        a = stdout.readlines()
        cmd = str(a)
        if result_query not in cmd:
            print "Failed {0}\n".format(test_name)
            print "Test detail: \n" + test_detail + "\n"
            print "Result: \n" + cmd + "\n"
            stop = time.asctime()
            test_logger(log_file, test_name, start, stop, "Fail")
        if result_query in cmd:
            print "Pass {0}".format(test_name)
            print "Test detail: \n" + test_detail + "\n"
            print "Result: \n" + cmd + "\n"
            stop = time.asctime()
            test_logger(log_file, test_name, start, stop, "Pass")
    else:
        print "{0} ".format(test_name) + "Will run next @ {0}".format(exec_time)
        stop = time.asctime()
        test_logger(log_file, test_name, start, stop, "Command Deferred")


def schedule_remote_exec_key(key, host, port, user, password, test_name, result_query, test_detail, exec_time, log_file, db_host, db_port, db):
    start = time.asctime()
    if exec_time in time.asctime():
        cl = paramiko.SSHClient()
        cl.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            cc = cl.connect(host, port=port, username=user, password=password)
        except paramiko.ssh_exception.AuthenticationException:
            print "Auth Error"
        except paramiko.ssh_exception.SSHException:
            print "Protocol Error"
        except paramiko.transport:
            print "General Error"
        except socket.error:
            print "Socket Error"
        func = db_get(key, db_host, db_port, db)
        stdin, stdout, stderr =  cl.exec_command(func)
        a = stdout.readlines()
        cmd = str(a)
        if result_query not in cmd:
            print "Failed {0}\n".format(test_name)
            print "Test detail: \n" + test_detail + "\n"
            print "Result: \n" + cmd + "\n"
            stop = time.asctime()
            test_logger(log_file, test_name, start, stop, "Fail")
        if result_query in cmd:
            print "Pass {0}".format(test_name)
            print "Test detail: \n" + test_detail + "\n"
            print "Result: \n" + cmd + "\n"
            stop = time.asctime()
            test_logger(log_file, test_name, start, stop, "Pass")
    else:
        print "{0} ".format(test_name) + "Will run next @ {0}".format(exec_time)
        stop = time.asctime()
        test_logger(log_file, test_name, start, stop, "Command Deferred")

def store_results(logfile, host, port, db):
    r = db_connect(host=host, port=port, db=db)
    with open(logfile, "r") as log:
        for i, line in enumerate(log):
            test = str(i) + "-test-{0}".format(time.time())
            r.set(test, line)

def tally_counter(logfile, resultfile, test_pass=True, test_fail=True):
    with open(logfile, "r") as log:
        for i, line in enumerate(log):
            if test_pass is True:
                counts = i
                pass_str = "Pass"
                if pass_str in line:
                    r = pass_str + " Test #: " + str(counts) + "\n"
                    os.system("touch {0}".format(resultfile))
                    f = open(resultfile, "a")
                    f.write(r)
                    f.close()
                    print r
                if test_fail is True:
                    fail_str = "Fail"
                    if fail_str in line:
                        counts = i
                        r = fail_str + " Test #: " + str(counts) + "\n"
                        os.system("touch {0}".format(resultfile))
                        f = open(resultfile, "a")
                        f.write(r)
                        f.close()
                        print r


def store_tally(resultfile, host, port, db):
    r = db_connect(host=host, port=port, db=db)
    with open(resultfile, "r") as log:
        for i, line in enumerate(log):
            test = str(i) + "-result-{0}".format(time.time())
            r.set(test, line)
