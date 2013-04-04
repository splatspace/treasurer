#!/usr/bin/env python
import csv
import argparse
import sys
import datetime

def determine_negative(amount):
	if amount.startswith('('):
		amount = '-%s' % amount[2:-1]
	else:
		amount = amount[1:]
		
	return amount
	
parser = argparse.ArgumentParser(description='Display totals from BB&T csv dump.')
parser.add_argument('filename', metavar='csv_file', type=argparse.FileType('r'),
                   default=sys.stdin,
                   help='transaction csv file from BB&T')
parser.add_argument('-m', dest='month', type=str,
                   help='only display totals for the month')
parser.add_argument('-y', dest='year', type=str,
					help='only display totals for the year')
parser.add_argument('-c', dest='credit', type=str,
					help='only display credit')
parser.add_argument('-d', dest='debit', type=str,
					help='only display debits')

args = parser.parse_args()
total = 0
now = datetime.datetime.now()
if args.year:
	year = args.year
else:
	year = now.year
with args.filename as csvfile:
	content = csv.DictReader(csvfile)
	if args.month:
		for row in content:
			if (row['Date'].startswith(args.month) and
				row['Date'].endswith(str(year))):
					amount = determine_negative(row['Amount'])
					
					print row['Date'] , row['Transaction Type'], row['Description'], amount
					total += float(amount)
	else:
		for row in content:
			amount = determine_negative(row['Amount'])
			
			print row['Date'] , row['Transaction Type'], row['Description'], amount
			total += float(amount)
args.filename.close()
print total

