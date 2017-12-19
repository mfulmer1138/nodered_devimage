#!/usr/bin/env sh
python3 ./merge_subflows.py
docker build -t devimage:latest .
