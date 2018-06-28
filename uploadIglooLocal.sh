#!/bin/bash
# uploadIglooLocal.sh
# script to run on Windows machine (hcaldaq-pc)
# 1. copy json file to Linux machine (cmshcal11)
# 2. upload results to database

# use explicit ip address because Windows machine does not resolve host aliases
remoteHost=hep@192.168.1.11
remoteDatabase=/home/django/testing_database_hb
remoteJson=$remotePath/uploader/temp_json
remoteScript=$remotePath/uploader/uploadIglooRemote.sh
localJson=info.json


# 1. copy json file to Linux machine (cmshcal11)
scp $localJson $remoteHost:$remoteJson
# 2. upload results to database
ssh $remoteHost $remoteScript

