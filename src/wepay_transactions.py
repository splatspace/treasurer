#!/usr/bin/env python
# encoding: utf-8
"""
wepay_transactions.py

Created by Darren Boss on 2013-08-14.
"""

import argparse
import getpass
import sys
import requests
import csv
import datetime
from bs4 import BeautifulSoup

WEPAY_URL = 'https://www.wepay.com'
CSV = '/export/generate/78191/group_transactions'
LOGIN = '/login'
CSV_URL = WEPAY_URL + CSV
LOGIN_URL = WEPAY_URL + LOGIN


def download_csv(username):
    password = getpass.getpass("Password:")
    s = requests.Session()
    html_doc = s.get(LOGIN_URL)
    soup = BeautifulSoup(html_doc.text)
    csrf = soup.find('input', attrs={'name': 'csrf'})
    nonce = soup.find('input', attrs={'name': 'nonce'})
    print csrf['value']
    print nonce['value']
    payload = {'email': username, 'password': password,
               'csrf': csrf['value'], 'nonce': nonce['value']}
    r = s.post(LOGIN_URL, payload)
    #print r.text
    csv_file = s.get(url=CSV_URL)
    f = open('transactions.csv', 'w')
    f.write(csv_file.text)
    f.close()

parser = argparse.ArgumentParser(description='Download WePay transactions.')
parser.add_argument('-d', '--download', action='store_true',
                    help='download transactions')
parser.add_argument('-u', '--username', dest='username',
                    help='WePay username')
parser.add_argument('-m', dest='month', type=str,
                    help='only display totals for the month')
parser.add_argument('-y', dest='year', type=str,
                    help='only display totals for the year')
parser.add_argument('-e', dest='email', type=str,
                    help='search for payments by email')
parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'),
                    default=sys.stdout)
args = parser.parse_args()
if args.download:
    download_csv(args.username)
with open('transactions.csv', 'r') as content_file:
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
