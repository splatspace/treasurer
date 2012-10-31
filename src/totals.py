#!/usr/bin/env python
import csv
import argparse
import sys

parser = argparse.ArgumentParser(description='Display totals from WePay csv dump.')
parser.add_argument('filename', metavar='csv_file', type=argparse.FileType('r'),
                   default=sys.stdin,
                   help='transaction csv file from WePay')
parser.add_argument('-m', dest='month', type=str,
                   help='only display totals for the month')
parser.add_argument('-y', dest='year', type=str,
					help='only display totals for the year')

args = parser.parse_args()
total = 0
with args.filename as csvfile:
	content = csv.DictReader(csvfile)
	if args.month:
		for row in content:
			if row['Date'].startswith(args.month):
				if row['Type'] == 'invoice payment':
					print row['Date'] , row['Email'] , row['Amount']
					total += float(row['Amount'].replace(',', ''))
	else:
		for row in content:	
			if row['Type'] == 'invoice payment':
				print row['Amount']
				total += float(row['Amount'].replace(',', ''))
			else:
				print row['Amount'] , ' skipped'
args.filename.close()
print total
