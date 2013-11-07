#!/usr/bin/python
import os
import argparse
import re
from subprocess import Popen, PIPE

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Generate timesheet from git logs")
    parser.add_argument('directory', help='directory to use (example: python git_timesheet.py ~/Code/some_repo', action='store')
    parser.add_argument('-d', '--date', help='year and month to generate summary for (example: -d 2013.10)', action='store')
    parser.add_argument('-a', '--author', help='name of author (example: -a "Murat Ayfer"', action='store')
    args = parser.parse_args()

    directory = args.directory
    date = args.date
    author = args.author

    os.chdir(directory)

    command = 'git log --date=iso --since={date}.01 --until={date}.31 --author="{author}" --pretty="format:%ad | %an | %s"'.format(date=date, author=author)

    process = Popen(command, stdout=PIPE, shell=True)
    log_output, stderr = process.communicate()

    if stderr:
        raise Exception("Error: {e}".format(e=stderr))

    lines = log_output.split('\n')
    lines.reverse()

    time_regex = r"#time( (?P<hours>\d+)h)?( (?P<minutes>\d+)m)?"

    def round_to_quarter(x):
        return round(x*4)/4

    def extract_time(text):
        pattern = re.compile(time_regex)
        match = pattern.search(text)

        hours, minutes = None, None
        if match is not None:
            hours = match.group("hours")
            minutes = match.group("minutes")

        if hours is None:
            hours = 0
        if minutes is None:
            minutes = 0

        return round_to_quarter(float(hours) + (float(minutes) / 60))

    for line in lines:
        date, author, message = line.split('|', 2)
        date = date.strip()[:10]
        author = author.strip()
        message = message.strip().replace(',', '-') # so it doesn't interfere with csv
        time = extract_time(message)
        message = re.sub(time_regex, '', message)
        print "{date},{author},{time},{message},Quiet.ly,Quiet.ly 12-189".format(date=date, author=author, time=time, message=message)


def read(filename):
    import csv
    with open(filename) as file:
        reader = csv.reader(file, delimiter=',', quotechar='"')
        return list(reader)

def total(filename):
    lines = read(filename)
    from decimal import Decimal
    total = 0
    for line in lines:
        total += Decimal(line[2])
    return total
