# log_parser

This application is made up of three python scripts and a bash runner. The first python script allows the user to parse a log, pull out relevant information via regular expressions, and store the parsed information as a sqlite3 table. The second python script allows the user to access the information stored in the sqlite3 table. The third python script is an automated error reporter that is called by the runner.sh shell script, and will run at regular intervals (as configured via crontab) to parse a log for arbitrary errors, perform some statistical analysis, and email a report of the analysis back to the user.

To use: download all files, and manually run at will OR configure crontab to execute runner.sh at the preferred frequency.
