#!/bin/bash

#############################################################
# This script runs the log parser suite of apps on a cron job
# mails the output to a recipient, and cleans the working dir
#############################################################


# get today's date as name of reporter file
email_report=$(date +"%m-%d-%Y")


# cd to the current working directory
cd /home/mkinzler/scripts/utilities/logparser/


# runner for the sd parser
python sd_log_parser.py /path/to/log/file.log "TEMP_DATABASE" "TEMP_TABLE"


# runner for the python script which redirects output to the email report
python error_parser.py /path/to/log/file.log &> $email_report


# header for the db browser section of the email
echo "#############################################################" >> $email_report
echo "Some high runners you may want to investigate are shown below" >> $email_report
echo "#############################################################" >> $email_report
echo "[date] [order] [transfer time]" >> $email_report


# runner for the db browser specifying time greater than 600 seconds for the sql query
python db_sd_reader.py "TEMP_DATABASE.db" "TEMP_TABLE" -t 600 >> $email_report


# mailer redirects file $email_report as stdin and emails to recipients
/usr/sbin/sendmail matthew.kinzler@gmail.com < $email_report 


# make dir to store file if it doesnt exist
if [ ! -d /home/mkinzler/scripts/email_reports ]; then
      mkdir -p /home/mkinzler/scripts/email_reports; 
fi;


# move report file to backup dir 
mv $email_report /users/home/mkinzler/scripts/mail_reports


# remove temp database 
rm "TEMP_DATABASE.db"


# done message
echo "runner.sh completed successfully"
