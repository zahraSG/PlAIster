from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from datetime import datetime


class DeviceForm(FlaskForm):
    name = StringField ('Device Name', validators=[DataRequired()] )
    macAddress = TextAreaField ('Mac Address' , validators = [DataRequired()])
    crownID =  StringField ('Crown ID', validators = [DataRequired()] )
    startDate = StringField ('Start Date', validators = [DataRequired()], default=datetime.utcnow)
    endDate = StringField ('End Date', validators = [DataRequired()], default=datetime.utcnow)
    submit = SubmitField('ADD') # inside the submitForm is the title you want to be shown on the screen
