#!/bin/bash
python ../lib/RPCServer.py  >> ../log/server.log & python ../lib/APIServer.py >> ../log/server.log
