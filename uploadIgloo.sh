#!/usr/bin/bash
# uploadIgloo.sh
# script to run on Windows machine (hcaldaq-pc)
# 1. copy json file to Linux machine (cmshcal11)
# 2. upload results to database

###################################################
#               Set Initial Data                  #
###################################################
echo "Setting initial data"

# use explicit ip address because Windows machine does not resolve host aliases
remoteHost=hep@192.168.1.11
remoteDatabase=/home/django/testing_database_hb
remoteJson=$remoteDatabase/uploader/temp_json
remoteScript=$remoteDatabase/uploader/step123.sh
jsonLoc=temp_json
jsonTag=step3_raw.json

echo "Initial data set"
echo ""

# Note: $? is the error code of the last command executed
# Use $? to check if the last command was successful

echo "    Copying json file to $remoteHost"

# 1. copy json file to Linux machine (cmshcal11)
scp $jsonLoc/*$jsonTag $remoteHost:$remoteJson
if [ $? -eq 0 ]
then
    echo "    Successfully copied json file to $remoteHost"
else
    echo "    ERROR: Failed to copy json file to $remoteHost"
    echo "ERROR: No information uploaded to database"
    exit 1
fi

# remote json files if copying was successful
rm $jsonLoc/*$jsonTag

# 2. upload results to database
# include option -w for no color ($1)
ssh $remoteHost $remoteScript $1

if [ $? -eq 0 ]
then
    echo "    Successfully uploaded results to database"
else
    echo "    ERROR: Failed to upload results to database"
    echo "ERROR: No information uploaded to database"
    exit 1
fi

echo "Successfully uploaded results to database"

echo "Finished"


