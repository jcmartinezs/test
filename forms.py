from flask_wtf import FlaskForm
from wtforms import StringField, RadioField
from wtforms.validators import DataRequired

class ContactForm(FlaskForm):
  name = StringField('Name', validators=[DataRequired()])
  fvcolor = StringField('Color', validators=[DataRequired()])
  pet = RadioField('Pet', choices=[('Cat','Cat'),('Dog','Dog')], validators=[DataRequired()])
