#!/usr/bin/env python
import csv
import argparse
import sys
import datetime

parser = argparse.ArgumentParser(description='Display totals from WePay csv dump.')
parser.add_argument('filename', metavar='csv_file', type=argparse.FileType('r'),
                   default=sys.stdin,
                   help='transaction csv file from WePay')
parser.add_argument('-m', dest='month', type=str,
                   help='only display totals for the month')
parser.add_argument('-y', dest='year', type=str,
					help='only display totals for the year')
parser.add_argument('-e', dest='email', type=str,
					help='search for payments by email')

args = parser.parse_args()
total = 0
now = datetime.datetime.now()
with args.filename as csvfile:
	content = csv.DictReader(csvfile)
	if args.email:
		for row in content:
			if row['Email'] == args.email and row['Status'] == 'Complete':
				amountwithfee = float(row['Amount']) + float(row['Fee'])
				print row['Date'] , amountwithfee , row['Type']
				total += amountwithfee
	if args.month:
		for row in content:
			if row['Date'].startswith(args.month) and row['Status'] == 'Complete':
				if row['Date'].endswith(str(now.year)):
					if row['Type'] == 'invoice payment':
						print row['Date'] , row['From/To'] , row['Email'] , row['Amount']
						total += float(row['Amount'].replace(',', ''))
	else:
		for row in content:	
			if row['Type'] != 'withdrawal' and row['Status'] == 'Complete':
				if row['Date'].endswith(str(now.year)):
					print row['Date'] , row['From/To'] , row['Email'] , row['Amount'], 				row['Type']
					total += float(row['Amount'].replace(',', ''))
args.filename.close()
print total
