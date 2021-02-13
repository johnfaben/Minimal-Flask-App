from app import app
from flask import render_template,flash,url_for,redirect,Markup
from .forms import AnswerForm
from .models import Hipe,random_hipe,delete_hipe

@app.route('/')
def index():
  return render_template('index.html',
   title = 'Home')
   
@app.route('/hipe/<letters>', methods = ['GET','POST'])
def hipe(letters): 
  hipe = Hipe(letters.lower())
  if hipe.letters is None:
    flash(Markup('we don\'t have a HIPE for {letters} <a href = {link}>should we</a>?'.format(letters = letters, link = url_for('add_hipe'))),'question')
    return redirect(url_for('index'))
  form = AnswerForm(hipe)
  if form.is_submitted():
    if form.validate():
      flash('Well done!','success')
      return redirect(url_for('answer',letters=letters))
    else:
      flash(Markup('Not quite, to see the answers, click <a href = {link}>here</a>'.format( link = url_for('answer',letters=hipe.letters))),'failure')
  return render_template('hipe.html',
    form = form,
    hipe = hipe)

@app.route('/random')
def random():
    hipe = random_hipe()
    return redirect(url_for('hipe',letters=hipe.letters))


@app.route('/answer/<letters>')
def answer(letters):
  
  hipe = Hipe(letters)
  return render_template('answer.html',hipe = hipe)

@app.route('/add_hipe')
def add_hipe():
  return render_template('add_hipe.html')




@app.route('/delete/<letters>')
def delete(letters):
  return render_template('delete.html',hipe = Hipe(letters))

@app.route('/confirm_delete/<letters>')
def confirm_delete(letters):
  flash('{letters} has been deleted from our list of HIPEs'.format(letters = letters))
  delete_hipe(letters)
  return redirect(url_for('index'))

@app.route('/vote/<letters>')
def vote(letters):
  hipe = Hipe(letters)
  if hipe.letters is not None:
    hipe.add_vote()
  return 'nothing'