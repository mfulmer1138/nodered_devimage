#!/usr/bin/env sh
mkdir data
python3 ./merge_subflows.py
docker build -t devimage:latest .
