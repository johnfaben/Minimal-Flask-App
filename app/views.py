from app import app
from flask import render_template,flash,url_for,redirect,Markup, request
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
import requests
import json
from .models import User


GOOGLE_CLIENT_ID = app.config['GOOGLE_CLIENT_ID']
GOOGLE_CLIENT_SECRET = app.config['GOOGLE_CLIENT_SECRET']
client = WebApplicationClient(GOOGLE_CLIENT_ID)

from .forms import AnswerForm
from .models import Hipe,random_hipe,delete_hipe

@app.route('/')
def index():
  return render_template('index.html',
   title = 'Home')

#############
#Logic for managing user login
#############

@app.route('/user')
@login_required
def user():
  if current_user.is_authenticated:
    return(render_template('user.html',name=current_user.name, liked = current_user.get_liked()))
  else:
    return redirect(url_for('login'))

@app.route('/user_solved')
@login_required
def user_solved():
  if current_user.is_authenticated:
    return(render_template('solved.html',name=current_user.name, solved = current_user.get_solved()))
  else:
    return redirect(url_for('login'))

def get_google_provider_cfg():
  return requests.get(app.config['GOOGLE_DISCOVERY_URL']).json()

@app.route('/login')
def login():
  return render_template('login.html',title='Log In')


@app.route('/login_google')
def login_google():
  google_provider_cfg = get_google_provider_cfg()
  authorization_endpoint = google_provider_cfg['authorization_endpoint']

  request_uri = client.prepare_request_uri(
     authorization_endpoint,
     redirect_uri = request.base_url.replace('http','https') + '/callback',
     scope = ['openid','email','profile']
  )

  return redirect(request_uri)


@app.route("/login_google/callback")
def google_callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url.replace('http','https'),
        redirect_url=request.base_url.replace('http','https'),
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    # Create a user in your db with the information provided
    # by Google
    user = User(
        id_=unique_id, name=users_name, email=users_email
    )

    # Doesn't exist? Add it to the database.
    if not User.get(unique_id):
        User.create(unique_id, users_name, users_email)

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect(url_for("index"))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

#############
#Logic for managing the HIPEs
#############

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
      if current_user.is_authenticated:
        current_user.add_solve(hipe)
      
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

@app.route('/like/<letters>')
def like(letters):
  hipe = Hipe(letters)
  if hipe.letters is not None:
      current_user.add_like(hipe)  
  return redirect(url_for('answer',letters=letters))

