#!/bin/bash

sleep 10

alembic upgrade heads

uvicorn src.main:app --host 0.0.0.0 --port 8000
