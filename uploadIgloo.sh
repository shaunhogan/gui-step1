#!/usr/bin/bash
# uploadIgloo.sh
# script to run on Windows machine (hcaldaq-pc)
# 1. copy json file to Linux machine (cmshcal11)
# 2. upload results to database

###################################################
#               Set Initial Data                  #
###################################################
echo -e "\e[1;34mSetting initial data"

# use explicit ip address because Windows machine does not resolve host aliases
remoteHost=hep@192.168.1.11
remoteDatabase=/home/django/testing_database_hb
remoteJson=$remoteDatabase/uploader/temp_json
remoteScript=$remoteDatabase/uploader/step123.sh
jsonLoc=temp_json
jsonTag=step3_raw.json

STATUS="\e[1;34m"   # color of status statements
ACTION="\e[1;33m"   # color of action statements
SUCCESS="\e[1;92m"  # color of success statements
FAIL="\e[1;91m"     # color of failure statements
DEF="\e[39;0m"      # default colors of text

echo -e "${STATUS}Initial data set"
echo ""

# Note: $? is the error code of the last command executed
# Use $? to check if the last command was successful

echo -e "    ${ACTION}Copying json file to $remoteHost"

# 1. copy json file to Linux machine (cmshcal11)
scp $jsonLoc/*$jsonTag $remoteHost:$remoteJson
if [ $? -eq 0 ]
then
    echo -e "    ${SUCCESS}Successfully copied json file to $remoteHost"
else
    echo -e "    ${FAIL}ERROR: Failed to copy json file to $remoteHost"
    echo -e "${FAIL}ERROR: No information uploaded to database"
    exit 1
fi
# 2. upload results to database
ssh $remoteHost $remoteScript

if [ $? -eq 0 ]
then
    echo -e "    ${SUCCESS}Successfully uploaded results to database"
else
    echo -e "    ${FAIL}ERROR: Failed to upload results to database"
    echo -e "${FAIL}ERROR: No information uploaded to database"
    exit 1
fi

echo -e "${SUCCESS}Successfully uploaded results to database"




