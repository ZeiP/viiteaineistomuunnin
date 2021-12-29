import csv
from app.fin_ktl import ReferenceTransferLine
from datetime import datetime, date

import sys

def transform_op(data, account, transfer):
  csv_reader = csv.reader(data, delimiter=';')
  output = ''
  for row in csv_reader:
    if len(row) == 10:
      ref_no = row[7]
      archive_id = row[9]
    else:
      ref_no = row[8]
      archive_id = row[10]
    ref_no = ref_no.replace('ref=', '').replace(' ', '')
    try:
      amount = float(row[2])
    except ValueError:
      try:
        amount = float(row[2].replace(",", "."))
      except ValueError:
        continue
    if amount > 0 and (transfer == 'all' or ref_no.isnumeric()):
      line = ReferenceTransferLine()
      line.account_no = format_account(account)
      try:
        line.booking_date = datetime.strptime(row[0], '%Y-%m-%d')
        line.payment_date = datetime.strptime(row[1], '%Y-%m-%d')
      except ValueError:
        line.booking_date = datetime.strptime(row[0], '%d.%m.%Y')
        line.payment_date = datetime.strptime(row[1], '%d.%m.%Y')
      line.archive_id = archive_id
      if ref_no.isnumeric():
        line.reference_no = ref_no
      else:
        line.reference_no = '0'
      line.payer = row[5]
      line.amount = str(int(amount * 100))
      output = output + str(line) + '\n'
  return output

def transform_nordea_csv(data, account, transfer):
  csv_reader = csv.reader(data, delimiter=';')
  output = ''
  for row in csv_reader:
    try:
      amount = float(row[1].replace(',', '.'))
    except ValueError:
      continue
    if amount > 0 and (transfer == 'all' or row[6].replace(' ', '').isnumeric()):
      line = ReferenceTransferLine()
      line.account_no = format_account(account)
      line.booking_date = datetime.strptime(row[0], '%d.%m.%Y')
      line.payment_date = datetime.strptime(row[0], '%d.%m.%Y')
      if row[6].replace(' ', '').isnumeric():
        line.reference_no = row[6].replace(' ', '')
      else:
        line.reference_no = '0'
      # Use reference no as archive ID, as nothing better's available.
      line.archive_id = line.reference_no
      line.payer = row[5]
      line.amount = str(int(amount * 100))
      output = output + str(line) + '\n'
  return output

def transform_nordea(data, account, transfer):
  csv_reader = csv.reader(data, delimiter='\t')
  output = ''
  for row in csv_reader:
    if len(row) < 4:
      continue
    try:
      amount = float(row[3].replace(',', '.'))
    except ValueError:
      continue
    if amount > 0 and (transfer == 'all' or row[8].replace(' ', '').isnumeric()):
      line = ReferenceTransferLine()
      line.account_no = format_account(account)
      line.booking_date = datetime.strptime(row[0], '%d.%m.%Y')
      line.payment_date = datetime.strptime(row[2], '%d.%m.%Y')
      if row[8].replace(' ', '').isnumeric():
        line.reference_no = row[8].replace(' ', '')
      else:
        line.reference_no = '0'
      # Use reference no as archive ID, as nothing better's available.
      line.archive_id = line.reference_no
      line.payer = row[4]
      line.amount = str(int(amount * 100))
      output = output + str(line) + '\n'
  return output

def transform_tito(data, account, transfer):
  output = ''
  for row in data.readlines():
    if row[0:3] == 'T10' and (row[48:49] == '1' or row[48:49] == '3') and (transfer == 'all' or row[159:179].strip()):
      line = ReferenceTransferLine()
      line.account_no = format_account(account)
      line.booking_date = datetime.strptime(row[30:36], '%y%m%d')
      line.payment_date = datetime.strptime(row[42:48], '%y%m%d')
      line.archive_id = row[12:30]
      if row[159:179].strip().isnumeric():
        line.reference_no = row[159:179].strip()
      else:
        line.reference_no = '0'
      line.payer = row[108:143]
      line.amount = str(int(row[88:106]))
      output = output + str(line) + '\n'
  return output

def transform_saastopankki(data, account, transfer):
  csv_reader = csv.reader(data, delimiter=';')
  output = ''
  for row in csv_reader:
    try:
      amount = float(row[4].replace(',', '.'))
    except ValueError:
      continue
    if amount > 0 and (transfer == 'all' or row[2] == 'VIITESIIRTO'):
      line = ReferenceTransferLine()
      line.account_no = format_account(account)
      line.booking_date = datetime.strptime(row[0], '%d.%m.%Y')
      line.payment_date = datetime.strptime(row[0], '%d.%m.%Y')
      if row[3].replace(' ', '').replace('\'', '').isnumeric():
        line.reference_no = row[3].replace(' ', '').replace('\'', '')
      else:
        line.reference_no = '0'
      # Use reference no as archive ID, as nothing better's available.
      line.archive_id = line.reference_no
      line.payer = row[1]
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
