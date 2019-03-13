# coding: utf-8

from __future__ import print_function # In python 2.7
from flask import render_template, request, Response, redirect
from app import app
from forms import *
from helper import *

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import smtplib

import sys

@app.route('/', methods=['GET', 'POST'])
def upload():
  form = FileForm()
  if form.validate_on_submit():
    print(form.file.data.filename, file=sys.stderr)
    f = form.file.data.stream
    account = form.account.data
    transfer = form.transfer.data
    if (account[:2] == 'FI'):
      account = iban_to_bban(account)

    if form.type.data == 'op':
      output = transform_op(f, account, transfer)
    elif form.type.data == 'nordea':
      output = transform_nordea(f, account, transfer)
    elif form.type.data == 'kuksa':
      output = transform_kuksa(f, account)
    # Figure out a nice name
    filename = form.file.data.filename.split('.')[0]
    return Response(output, mimetype='text/plain', headers={
      "Content-Disposition":
      "attachment;filename=%s.txt" % filename
    })

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
    msg = MIMEMultipart()
    msg['From'] = app.config['EMAIL_FROM']
    msg['To'] = app.config['FEEDBACK_TO']
    msg['Subject'] = "Viitemuunninpalaute"
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    server = smtplib.SMTP(app.config['SMTP_SERVER'])
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    return redirect('/success')

  return render_template('feedback.html', form=form)

@app.route('/success')
def success():
  return render_template('success.html')
