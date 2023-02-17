#!/bin/bash
cd /home/gasonzhong/chattt
source /home/gasonzhong/chattt/venv/bin/activate
nohup python -u devchat-api-server.py >producer.out 2>&1 &
