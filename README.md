automiko
========

Automation Engine written in python with remote execution and redis backend

setup
========
pip install redis paramiko scp Automiko

or 

pip install redis paramiko scp

cd automiko 


python setup.py build


python setup.py install

Running
========

Sample Key Execution
========

import Automiko.Execute as Execute

db_host = "localhost"

db_port = 6379

db = 0

logger = "logger.log"

results = "results.log"


Execute.key_cmd(key="py_search",
                cmd="ls",
                host=db_host,
                port=db_port,
                db=db)

Execute.exec_key(key="py_search",
                 test_name="Test Key Exec",
                 result_query=".py",
                 test_detail="DB Execute Key and locate verify .py files exist",
                 log_file=logger,
                 host=db_host,
                 port=db_port,
                 db=db)
Executing a file
========
Execute.exec_file(script="script.sh",
                  test_name="Test File Exec",
                  result_query="open port 8099",
                  test_detail="verify port 8099 is open",
                  log_file=logger)
Executing a script or key remotely
========
Execute.remote_exec_file(script="script.sh",
                         host="host ip",
                         port=22,
                         user="username",
                         password="password",
                         test_name="Remote port 22 verification",
                         result_query="open port 22",
                         test_detail="Remote execute script and verify port 22 is open",
                         log_file=logger)

Execute.remote_exec_key(key="py_search",
                        host="host ip",
                        port=22,
                        user="username",
                        password="password",
                        test_name="Remote key execution verifying python script exist",
                        result_query=".py",
                        test_detail="Verify py script exist",
                        log_file=logger,
                        db_host=db_host,
                        db_port=db_port,
                        db=db)
Scheduling Functions
========
Execute.schedule_exec_key(key="py_search",
                        test_name="Remote key execution verifying python script exist",
                        result_query=".py",
                        test_detail="Verify py script exist",
                        exec_time="15:00",
                        log_file=logger,
                        host=db_host,
                        port=db_port,
                        db=db)

Execute.schedule_exec_file(script="script.sh",
                           test_name="Port verification via nmap",
                           result_query="open port 8099",
                           test_detail="Verify port 8099 is open",
                           exec_time="Tue",
                           log_file=logger)

Execute.schedule_remote_exec_file(script="script.sh",
                                  host="host ip",
                                  port=22,
                                  user="username",
                                  password="password",
                                  test_name="Port verification via nmap",
                                  result_query="open port 22",
                                  test_detail="Verify port 22 is open",
                                  exec_time="Tue",
                                  log_file=logger)


Execute.schedule_remote_exec_key(key="py_search",
                                 host="host ip",
                                 port=22,
                                 user="username",
                                 password="password",
                                 test_name="Remote key execution on schedule",
                                 result_query=".py",
                                 test_detail="Searching for python script on remote host",
                                 exec_time="19:00",
                                 db_host=db_host,
                                 db_port=db_port,
                                 db=db,
                                 log_file=logger)

Caculate Results 
========
Execute.tally_counter(logfile=logger,
                      resultfile=results,
                      test_pass=True,
                      test_fail=True)
