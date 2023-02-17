#!/bin/bash
cd /home/gasonzhong/chattt
source /home/gasonzhong/chattt/venv/bin/activate
nohup python -u chatgpt-consumer.py >consumer1.out 2>&1 &
