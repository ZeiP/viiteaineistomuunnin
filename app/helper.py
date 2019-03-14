import csv
from app.fin_ktl import ReferenceTransferLine
from datetime import datetime, date

import sys

def transform_op(data, account, transfer):
  csv_reader = csv.reader(data, delimiter=';')
  output = ''
  for row in csv_reader:
    try:
      amount = float(row[2].replace(',', '.'))
    except ValueError:
      continue
    if amount > 0 and (transfer == 'all' or row[7].replace(' ', '').isnumeric()):
      line = ReferenceTransferLine()
      line.account_no = format_account(account)
      line.booking_date = datetime.strptime(row[1], '%d.%m.%Y')
      line.payment_date = datetime.strptime(row[0], '%d.%m.%Y')
      line.archive_id = row[9]
      if row[7].replace(' ', '').isnumeric():
        line.reference_no = row[7].replace(' ', '')
      else:
        line.reference_no = '0'
      line.payer = row[5]
      line.amount = str(int(amount * 100))
      output = output + str(line) + '\n'
  return output

def transform_nordea(data, account, transfer):
  csv_reader = csv.reader(data, delimiter=';')
  output = ''
  for row in csv_reader:
    try:
      amount = float(row[3].replace(',', '.'))
    except ValueError:
      continue
    if amount > 0 and (transfer == 'all' or row[8].replace(' ', '').isnumeric()):
      line = ReferenceTransferLine()
      line.account_no = format_account(account)
      line.booking_date = datetime.strptime(row[1], '%d.%m.%Y')
      line.payment_date = datetime.strptime(row[0], '%d.%m.%Y')
      line.archive_id = ' '
      if row[8].replace(' ', '').isnumeric():
        line.reference_no = row[8].replace(' ', '')
      else:
        line.reference_no = '0'
      line.payer = row[4]
      line.amount = str(int(amount * 100))
      output = output + str(line) + '\n'
  return output

def transform_kuksa(data, account, transfer):
  csv_reader = csv.reader(data, delimiter=';')
  output = ''
  for row in csv_reader:
    try:
      amount = float(row[8].replace(',', '.'))
    except ValueError:
      continue
    if amount > 0 and (transfer == 'all' or row[4].replace(' ', '').isnumeric()):
      line = ReferenceTransferLine()
      line.account_no = format_account(account)
      line.booking_date = date.today()
      line.payment_date = date.today()
      line.archive_id = 'VIITEMUUNNIN'
      if row[4].replace(' ', '').isnumeric():
        line.reference_no = row[4].replace(' ', '')
      else:
        line.reference_no = '0'
      line.payer = row[3]
      line.amount = str(int(amount * 100))
      output = output + str(line) + '\n'
  return output

def format_account(account):
  account = account.replace(' ', '').replace('-', '')
  if account[:2] == 'FI':
    return iban_to_bban(iban)
  return account

def iban_to_bban(iban):
  if iban[4] == '4' or iban[4] == '5':
    bban = iban[4:11] + iban[12:].lstrip('0')
  else:
    bban = iban[4:10] + iban[11:].lstrip('0')
  return bban
