# coding: utf-8

from flask import render_template, request, Response, redirect
from app import app
from app.forms import *
from app.helper import *

from email.mime.text import MIMEText
import smtplib

import sys, os

from tempfile import NamedTemporaryFile

import datetime

@app.route('/', methods=['GET', 'POST'])
def upload():
  form = FileForm()
  if form.validate_on_submit():
#    print(form.file.data.filename, file=sys.stderr)

    # Add a row with the date and conversion type for each use for statistics.
    with open("/srv/django/viiteaineisto/log.txt", "a") as statfile:
      statfile.write(str(datetime.date.today()) + ";" + form.type.data)

    # Apparently we need to save the contents to a file to open the stream
    # in text mode for the csv reader. Create a tmp file to generate a
    # secure file and remember to remove it after usage.
    tmpfile = NamedTemporaryFile(delete=False)
    tmpfilename = tmpfile.name
    tmpfile.close()
    form.file.data.save(tmpfilename)
    # Doesn't work because it's in binary mode, not text.
#    f = form.file.data.stream

    account = form.account.data
    transfer = form.transfer.data
    if (account[:2] == 'FI'):
      account = iban_to_bban(account)

    if form.type.data == 'op':
      f = open(tmpfilename, 'rt', encoding='utf-8')
      output = transform_op(f, account, transfer)
    elif form.type.data == 'nordea':
      f = open(tmpfilename, 'rt', encoding='utf-8')
      output = transform_nordea(f, account, transfer)
    elif form.type.data == 'tito':
      f = open(tmpfilename, 'rt', encoding='iso-8859-15')
      output = transform_tito(f, account, transfer)
    elif form.type.data == 'saastopankki':
      f = open(tmpfilename, 'rt', encoding='iso-8859-15')
      output = transform_saastopankki(f, account, transfer)
    elif form.type.data == 'kuksa':
      f = open(tmpfilename, 'rt', encoding='utf-8')
      output = transform_kuksa(f, account, transfer)

    # Remove the tmp file.
    os.unlink(tmpfilename)
    # Figure out a nice name
    filename = form.file.data.filename.split('.')[0]
    return Response(output.encode('iso-8859-15'), mimetype='text/plain', headers={
      "Content-Disposition": "attachment;filename=%s.txt" % filename
    })

  if request.args.get('account'):
    form.account.data = request.args.get('account')
  return render_template('form.html', form=form)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
  form = FeedbackForm()
  if form.validate_on_submit():
    body = u"""Viitemuuntimen palautelomakkeella tullut viesti:

Nimi: %s
Sahkopostiosoite: %s
Viesti:
%s""" % (form.name.data, form.email.data, form.message.data)
    msg = MIMEText(body)
    msg['From'] = app.config['EMAIL_FROM']
    msg['To'] = app.config['FEEDBACK_TO']
    msg['Subject'] = "Viitemuunninpalaute"

    server = smtplib.SMTP(app.config['SMTP_SERVER'])
    server.send_message(msg)
    return redirect('/success')

  return render_template('feedback.html', form=form)

@app.route('/success')
def success():
  return render_template('success.html')
