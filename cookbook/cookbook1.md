Automiko Cookbook
=========

Automike Redis Key Execution
=========

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
Execute.tally_counter(logfile=logger, resultfile=results, test_pass=True, test_fail=True)
Execute.store_results(logfile=logger, host=db_host, port=db_port, db=db)
Execute.store_tally(resultfile=results, host=db_host, port=db_port, db=db)                 
