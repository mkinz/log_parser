#!/bin/bash

#############################################################
# This script runs the error parser application on a cron job
# mails the output to a recipient, and cleans the working dir
#############################################################


# get today's date
mydate=$(date +"%m-%d-%Y")


# cd to the current working directory
cd /home/mkinzler/utilities


# runner for the python script and output filename as mydate
python error_parser.py /path/to/log/file/file.log &> $mydate


# mailer and redirect mydate as stdin
/usr/sbin/sendmail matthew.kinzler@gmail.com < $mydate


# make dir to store file if it doesnt exist
if [ ! -d /home/mkinzler/scripts/errors ]; then
      mkdir -p /home/mkinzler/scripts/errors; 
fi;


# move file to backup dir 
mv $mydate /home/mkinzler/scripts/errors/
