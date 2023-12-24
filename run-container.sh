#!/usr/bin/bash

export PYTHONPATH=backend:.
poetry run uvicorn --host 0.0.0.0 --port 5000 backend.app:app