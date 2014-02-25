#!/usr/bin/env python
# encoding: utf-8
"""
wepay_transactions.py

Created by Darren Boss on 2013-08-14.
"""

import argparse
import sys
import csv
import datetime

parser = argparse.ArgumentParser(description='Parse WePay transactions.')
parser.add_argument('-m', dest='month', type=str,
                    help='only display totals for the month')
parser.add_argument('-y', dest='year', type=str,
                    help='only display totals for the year')
parser.add_argument('-e', dest='email', type=str,
                    help='search for payments by email')
parser.add_argument('infile', nargs='?', type=argparse.FileType('r'))
parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'),
                    default=sys.stdout)
args = parser.parse_args()
with args.infile as content_file:
    data = content_file.read()
now = datetime.datetime.now()
year = now.year
total = 0
content = csv.DictReader(data.splitlines())
#print data
if args.email:
    for row in content:
        if row['Email'] == args.email and row['Status'] == 'Complete':
            amountwithfee = float(row['Amount']) - float(row['Fee'])
            print row['Date'], amountwithfee, row['Type']
            total += amountwithfee
if args.month:
    for row in content:
        if (row['Date'].startswith(args.month) and row['Status'] == 'Complete' and row['Date'].endswith(str(year)) and row['Type'] == 'invoice payment'):
                print row['Date'], row['From/To'], row['Email'], row['Amount']
                total += float(row['Amount'].replace(',', ''))
else:
    for row in content:
        if (row['Type'] != 'withdrawal' and row['Status'] == 'Complete' and row['Date'].endswith(str(year))):
            print row['Date'], row['From/To'], row['Email'], row['Amount'], row['Type']
            total += float(row['Amount'].replace(',', ''))
print total
