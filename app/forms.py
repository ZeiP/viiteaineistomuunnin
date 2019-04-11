# coding: utf-8

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import SelectField, StringField, TextAreaField
from wtforms.validators import DataRequired

class FileForm(FlaskForm):
  account = StringField(u'Tilinumero', validators=[DataRequired()])
  file = FileField(u'Tiedosto', validators=[FileRequired()])
  type = SelectField(u'Tyyppi', choices=[('op', 'Osuuspankki'), ('nordea', 'Nordea tapahtumaluettelo'), ('tito', 'TITO (esim. Nordea yrityspankki)'), ('saastopankki', 'Säästöpankki'), ('kuksa', 'Kuksan laskulista')], validators=[DataRequired()])
  transfer = SelectField(u'Siirrettävät maksut', choices=[('only_ref', 'Vain viitenumerolliset'), ('all', 'Kaikki')], validators=[DataRequired()])

class FeedbackForm(FlaskForm):
  name = StringField(u'Nimi')
  email = StringField(u'Sähköpostiosoite')
  message = TextAreaField(u'Viesti', validators=[DataRequired()])
