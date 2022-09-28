#!/usr/bin/env bash
nohup python main.py api 2>&1 & &&
nohup python main.py schedule > schedule.log 2>&1 &