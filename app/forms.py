from flask_wtf import FlaskForm
from flask import flash

from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired
from app.models import Model



class AnswerForm(FlaskForm):
    answer = StringField('answer',validators=[DataRequired()])
    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

    def validate(self):

        if not FlaskForm.validate(self):
            return False

        return True