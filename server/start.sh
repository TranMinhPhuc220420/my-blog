#!/bin/bash
source environments/my_env/bin/activate

systemctl start mongod

# fastapi dev main.py
uvicorn main:app --reload --reload-exclude server.log

systemctl stop mongod
deactivate