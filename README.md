git_timesheet
=============

CSV Timesheet generator from git logs that use the format "#time 4h 30m" in commit messages. 
Generates the logs per month, for a particular author.

Usage:
-----

python git_timesheet.py --date=2013.10 --author="author name" ~/path/to/repo
