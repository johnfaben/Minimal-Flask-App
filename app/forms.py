from flask_wtf import FlaskForm
from flask import flash

from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired
from app.models import Answer,Hipe

class LoginForm(FlaskForm):
    openid = StringField('openid',validators=[DataRequired()])
    remember_me = BooleanField('remember_me',default=False)


class AnswerForm(FlaskForm):
    answer = StringField('answer',validators=[DataRequired()])
    def __init__(self, hipe, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.hipe = hipe 


    def validate(self):
        letters = self.hipe.letters
       

        if not FlaskForm.validate(self):
            return False

        if letters not in self.answer.data.lower():
            self.answer.errors.append('The letters "%s" are not in the word "%s", try again.' %(letters,self.answer.data))
            return False

        if self.answer.data.lower() in self.hipe.answers:
          return True
        else: 
            self.answer.errors.append('I do not think that "%s" is a word. Am I wrong?' %self.answer.data)
            return False
