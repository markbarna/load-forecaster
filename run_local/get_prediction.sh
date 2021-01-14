#!/usr/bin/env bash

#    usage: predict.py [-h] date time {PE,PEP} url
#
#    Predict load for date, time, and area zone.
#
#    positional arguments:
#      date        the date in common string format
#      time        the time in UTC 24hr HH:MM
#      {PE,PEP}    the PJM area code (one of PE, PEP)
#      url         POST request endpoint url
#
#    optional arguments:
#      -h, --help  show this help message and exit

python -m predict 2021-02-1 12:00 PEP http://localhost:8080/invocations