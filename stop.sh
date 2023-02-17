#!/bin/sh
ps -ef |grep devchat-api-server.py | grep -v grep | awk '{print $2}' | xargs kill -9
