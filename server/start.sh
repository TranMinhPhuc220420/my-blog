#!/bin/bash
source environment/bin/activate

uvicorn main:app --reload --host 0.0.0.0 --port 8000 --reload-exclude server.log

deactivate