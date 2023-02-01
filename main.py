from flask import Flask, render_template, session, request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from datetime import datetime
import json

with open('config.json', 'r') as f:
    config_parameters = json.load(f)["parameters"]

local_server = True

app = Flask(__name__)

# session_time = session.permanent.time(day=3)

app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = config_parameters['sender_email'],
    MAIL_PASSWORD=  config_parameters['sender_email_password']
)

mail = Mail(app)

if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = config_parameters['local_server_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = config_parameters['host_server_uri']

db = SQLAlchemy(app)

class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    message = db.Column(db.String(120), nullable=False
    )

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/projects")
def projects():
    return render_template("projects.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods = ['GET', 'POST'])
def contact():
    if(request.method=='POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        entry = users(name=name, message = message, email = email)
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New message from ' + name,
                        sender = email,
                        recipients = [config_parameters['sender_email']],
                        body = message + "\n")
    return render_template("contact.html")

app.run(debug=True)