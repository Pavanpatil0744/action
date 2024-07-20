#!/bin/bash

superset fab create-admin \
    --username admin \
    --firstname Superset \
    --lastname Admin \
    --email admin@superset.com \
    --password admin

superset db upgrade
superset init
exec superset run --port=8088 --with-threads --reload --debugger
