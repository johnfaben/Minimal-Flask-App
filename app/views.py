from app import app
from flask import render_template,flash,url_for,redirect,Markup, request


from .forms import AnswerForm
from .models import Model

@app.route('/')
def index():
  return render_template('index.html',
   title = 'Home')

#############
#Logic for managing the HIPEs
#############

@app.route('/formpage', methods = ['GET','POST'])
def formpage():
  form = AnswerForm()
  if form.is_submitted():
    if form.validate():
      return redirect(url_for('backward',letters = form.answer.data))
  return render_template('formpage.html',
    form = form)

@app.route('/backward/<letters>')
def backward(letters):
  return render_template('backward.html',letters = letters)