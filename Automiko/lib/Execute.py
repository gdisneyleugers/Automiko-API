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
    return "saved " + key + " @ " + cmd


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
            a = "Failed: {0}\n".format(test_name)
            b = "Test detail: \n" + test_detail + "\n"
            c = "Result: " + r + "\n"
            stop = time.asctime()
            test_result = "Fail"
            test_logger(log_file, test_name, start, stop, test_result)
            store_detail(test_detail=test_detail, test_name=test_name, host=host, port=port, db=db)
            return a, b, c
        if result_query in r:
            a = "Pass: {0}\n".format(test_name)
            b = "Test detail: \n" + test_detail + "\n"
            c = "Result: \n" + r + "\n"
            stop = time.asctime()
            test_result = "Pass"
            test_logger(log_file, test_name, start, stop, test_result)
            store_detail(test_detail=test_detail, test_name=test_name, host=host, port=port, db=db)
            return a, b, c
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
        a = "Failed: {0}\n".format(test_name)
        b = "Test detail: \n" + test_detail + "\n"
        c = "Result: \n" + cmd + "\n"
        stop = time.asctime()
        test_logger(log_file, test_name, start, stop, "Fail")
        return  a, b, c
    if result_query in cmd:
        a = "Pass: {0}".format(test_name)
        b =  "Test detail: \n" + test_detail + "\n"
        c = "Result: \n" + cmd + "\n"
        stop = time.asctime()
        test_logger(log_file, test_name, start, stop, "Pass")
        return  a, b, c


def schedule_exec_key(key, test_name, result_query, test_detail, exec_time, log_file, host, port, db):
    start = time.asctime()
    if exec_time in time.asctime():
        try:
            cmd = cmd = db_get(key, host, port, db)
            r = os.popen(cmd).read()
            if result_query not in r:
                a =  "Failed: {0}\n".format(test_name)
                b =  "Test detail: \n" + test_detail + "\n"
                c = "Result: " + r + "\n"
                stop = time.asctime()
                test_logger(log_file, test_name, start, stop, "Fail")
                store_detail(test_detail=test_detail, test_name=test_name, host=host, port=port, db=db)
                return a, b, c
            if result_query in r:
                a =  "Pass {0}\n".format(test_name)
                b = "Test detail: \n" + test_detail + "\n"
                c =  "Result: " + r + "\n"
                stop = time.asctime()
                test_logger(log_file, test_name, start, stop, "Pass")
                store_detail(test_detail=test_detail, test_name=test_name, host=host, port=port, db=db)
                return a, b, c
        except TypeError:
            return "Key doesn't exist in DB"
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
            a = "Failed: {0}\n".format(test_name)
            b = "Test detail: \n" + test_detail + "\n"
            c = "Result: \n" + cmd + "\n"
            stop = time.asctime()
            test_logger(log_file, test_name, start, stop, "fail")
            return a, b, c
        if result_query in cmd:
            a =  "Pass: {0}".format(test_name)
            b =  "Test detail: \n" + test_detail + "\n"
            c =  "Result: \n" + cmd + "\n"
            return a, b, c

    else:
        a =  "{0} ".format(test_name) + "Will run next @ {0}".format(exec_time)
        stop = time.asctime()
        test_logger(log_file, test_name, start, stop, "Command Deferred")
        return a


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
        a = "Failed: {0}\n".format(test_name)
        b = "Test detail: \n" + test_detail + "\n"
        c = "Result: \n" + cmd + "\n"
        stop = time.asctime()
        test_logger(log_file, test_name, start, stop, "Fail")
        return a, b, c
    if result_query in cmd:
        a =  "Pass {0}".format(test_name)
        b =  "Test detail: \n" + test_detail + "\n"
        c = "Result: \n" + cmd + "\n"
        stop = time.asctime()
        test_logger(log_file, test_name, start, stop, "Pass")
        return a, b, c

def remote_exec_key(key, host, port, user, password, test_name, result_query, test_detail, log_file, db_host, db_port, db):
    start = time.asctime()
    cl = paramiko.SSHClient()
    cl.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        cc = cl.connect(host, port=port, username=user, password=password)
    except socket.error:
            print "Socket Error"
    func = db_get(key, db_host, db_port, db)
    stdin, stdout, stderr =  cl.exec_command(func)
    a = stdout.readlines()
    cmd = str(a)
    if result_query not in cmd:
        a = "Failed: {0}\n".format(test_name)
        b = "Test detail: \n" + test_detail + "\n"
        c = "Result: \n" + cmd + "\n"
        stop = time.asctime()
        test_logger(log_file, test_name, start, stop, "Fail")
        store_detail(test_detail=test_detail, test_name=test_name, host=db_host, port=db_port, db=db)
        return a, b, c
    if result_query in cmd:
        a = "Pass: {0}".format(test_name)
        b = "Test detail: \n" + test_detail + "\n"
        c = "Result: \n" + cmd + "\n"
        stop = time.asctime()
        test_logger(log_file, test_name, start, stop, "Pass")
        store_detail(test_detail=test_detail, test_name=test_name, host=db_host, port=db_port, db=db)
        return a, b, c

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
            a = "Failed: {0}\n".format(test_name)
            b = "Test detail: \n" + test_detail + "\n"
            c = "Result: \n" + cmd + "\n"
            stop = time.asctime()
            test_logger(log_file, test_name, start, stop, "Fail")
            return a, b, c
        if result_query in cmd:
            a = "Pass: {0}".format(test_name)
            b =  "Test detail: \n" + test_detail + "\n"
            c = "Result: \n" + cmd + "\n"
            stop = time.asctime()
            test_logger(log_file, test_name, start, stop, "Pass")
    else:
        a = "{0} ".format(test_name) + "Will run next @ {0}".format(exec_time)
        stop = time.asctime()
        test_logger(log_file, test_name, start, stop, "Command Deferred")
        return a


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
            a = "Failed: {0}\n".format(test_name)
            b = "Test detail: \n" + test_detail + "\n"
            c = "Result: \n" + cmd + "\n"
            stop = time.asctime()
            test_logger(log_file, test_name, start, stop, "Fail")
            store_detail(test_detail=test_detail, test_name=test_name, host=host, port=port, db=db)
            return a, b, c
        if result_query in cmd:
            a = "Pass: {0}".format(test_name)
            b = "Test detail: \n" + test_detail + "\n"
            c = "Result: \n" + cmd + "\n"
            stop = time.asctime()
            test_logger(log_file, test_name, start, stop, "Pass")
            store_detail(test_detail=test_detail, test_name=test_name, host=host, port=port, db=db)
            return a, b, c
    else:
        print "{0} ".format(test_name) + "Will run next @ {0}".format(exec_time)
        stop = time.asctime()
        test_logger(log_file, test_name, start, stop, "Command Deferred")
        store_detail(test_detail=test_detail, test_name=test_name, host=host, port=port, db=db)

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
                    return r
                if test_fail is True:
                    fail_str = "Fail"
                    if fail_str in line:
                        counts = i
                        r = fail_str + " Test #: " + str(counts) + "\n"
                        os.system("touch {0}".format(resultfile))
                        f = open(resultfile, "a")
                        f.write(r)
                        f.close()
                        return r


def store_tally(resultfile, host, port, db):
    r = db_connect(host=host, port=port, db=db)
    with open(resultfile, "r") as log:
        for i, line in enumerate(log):
            test = str(i) + "-result-{0}".format(time.time())
            r.set(test, line)


def store_detail(test_detail, test_name, host, port, db):
    r = db_connect(host=host, port=port, db=db)
    test = test_name + "-" + str(time.asctime())
    r.set(test, test_detail)

def set_user(user, db_host, port, db):
    key_cmd("user", user, db_host, port, db)
    a = "User saved"
    return a

def set_user_pass(password, db_host, port, db):
    key_cmd("password", password, db_host, port, db)
    a = "Password saved"
    return a

def set_remote_host(host, db_host, db_port, db):
    key_cmd("host", host, db_host, db_port, db)
    a = "Host Set"
    return a

def set_remote_port(db_host, db_port, db):
    key_cmd("port", 22, db_host, db_port, db)
    a = "Port Set"
    return a