#!/bin/sh
ps -ef |grep chatgpt-consumer.py | grep -v grep | awk '{print $2}' | xargs kill -9
