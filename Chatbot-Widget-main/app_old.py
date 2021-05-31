from flask import Flask, make_response, render_template, request, jsonify, session, abort, flash, redirect, url_for
from flask_cors import CORS, cross_origin
import json,os,datetime,time
import traceback
from passlib.apps import custom_app_context as pwd_context
from flask_sqlalchemy import SQLAlchemy
from random import randrange
from itsdangerous import URLSafeTimedSerializer
# from flask_mail import Message, Mail
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

app = Flask(__name__)
# initialization
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
app.config['SECURITY_PASSWORD_SALT'] = 'my_precious_two'
CORS(app)
# mail = Mail(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['Access-Control-Allow-Credentials'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_SERVER'] = 'mail.rintez.com'

app.config['MAIL_PORT'] = 587
# app.config['MAIL_PORT'] = 465

app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = 'cselakshmanan@gmail.com'  # enter your email here
app.config['MAIL_USERNAME'] = 'noreply@rintez.com'  # enter your email here

# app.config['MAIL_DEFAULT_SENDER'] = 'cselakshmanan@gmail.com' # enter your email here
app.config['MAIL_DEFAULT_SENDER'] = 'noreply@rintez.com' # enter your email here

# app.config['MAIL_PASSWORD'] = '8494@Bhuji' # enter your password here
app.config['MAIL_PASSWORD'] = 'A%vgaqf_JXYk' # enter your password here

app.config['MASTER_URL'] = "http://localhost:5000"

# extensions
db = SQLAlchemy(app)

class User(db.Model):
    """"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, nullable=False)
    password_hash = db.Column(db.String(64), nullable=False)
    email_id = db.Column(db.String(100), unique=True, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email

def send_email(to, subject, mail_content):
    # msg = Message(
    #     subject,
    #     recipients=[to],
    #     html=template,
    #     sender=app.config['MAIL_DEFAULT_SENDER']
    # )
    # mail.send(msg)
    message = MIMEMultipart()
    message['From'] = app.config['MAIL_DEFAULT_SENDER']
    message['To'] = to
    message['Subject'] = subject
    # message.attach(MIMEText(mail_content, 'plain'))
    message.attach(MIMEText(mail_content, 'html'))
    session = smtplib.SMTP(app.config['MAIL_SERVER'], app.config['MAIL_PORT']) #use gmail with port
    session.starttls() #enable security
    session.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD']) #login with mail_id and password
    text = message.as_string()
    try:
        session.sendmail(app.config['MAIL_DEFAULT_SENDER'], to, text)
        print('Email to {} successfully sent!\n\n'.format(to))
    except Exception as e:
        print('Email to {} could not be sent :( because {}\n\n'.format(to, str(e)))

    session.quit()

@app.route("/")
def home():
    print(session.get('logged_in'))
    if not session.get('logged_in'):
        return render_template('form.html')
    else:
        return render_template('index.html', username=session['username'])

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST":
        username_or_emailid = request.form['username']
        password = request.form['password']
        print(username_or_emailid, password)
        user = User.query.filter_by(username=username_or_emailid).first()
        if not user:
            user = User.query.filter_by(email_id=username_or_emailid).first()
        if not user or not user.verify_password(password):
            session['logged_in'] = False
            session.clear()
            flash("Wrong username or password..", "error")
        elif user and not user.confirmed:
            session['logged_in'] = False
            session.clear()
            flash('Please confirm your account!', 'error')
        else:
            session['logged_in'] = True
            session['username'] = user.username
            flash("Login Successful..", "success")
    return redirect(url_for('home'))

@app.route('/guestlogin', methods=['GET','POST'])
def guestlogin():
    if request.method == "POST":
        username = "Guest" + str(randrange(1000))
        session['logged_in'] = True
        session['username'] = username
        print("guest", username)
        flash("Login Successful..", "success")
    return redirect(url_for('home'))


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    if request.method == "POST":
        session['logged_in'] = False
        session.clear()
        flash("Logged Out Successfully..", "success")
        return jsonify(status="success")
    return redirect(url_for('home'))

@app.route('/confirm/<token>', methods=['GET','POST'])
def confirm_email(token):
    if request.method == "GET":
        try:
            email = confirm_token(token)
        except:
            flash('The confirmation link is invalid or has expired.', 'error')
        user = User.query.filter_by(email_id=email).first_or_404()
        if user.confirmed:
            flash('Account already confirmed. Please login.', 'success')
        else:
            user.confirmed = True
            user.confirmed_on = datetime.datetime.now()
            db.session.add(user)
            db.session.commit()
            flash('You have confirmed your account. Thanks!', 'success')
        return redirect(url_for('home'))

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        username = request.form['usernamesignup']
        password = request.form['passwordsignup']
        password_confirm = request.form['passwordsignup_confirm']
        emailId = request.form['emailsignup']
        if password != password_confirm:
            session['logged_in'] = False
            session.clear()
            flash("Password didn't not match. Please try again..", "error")
        elif User.query.filter_by(username=username).first() is not None:
            flash("Username already exists", "error")    # existing user
        elif User.query.filter_by(email_id=emailId).first() is not None:
            flash("EmailId already exists", "error")
        else:
            user = User(username=username, email_id= emailId, confirmed=False, registered_on = datetime.datetime.now())
            user.hash_password(password)
            db.session.add(user)
            db.session.commit()
            token = generate_confirmation_token(user.email_id)
            confirm_url = app.config['MASTER_URL'] + "/confirm/" + str(token)
            html = """\
            <html>
            <body>
                <p>Hi """+user.username+""",<br>
                Greetings from Rintez Medical Companion. The email ["""+user.email_id+"""] has been added as a contact detail to our database.<br><br>
                Please confirm the email by clicking the below button. If wasn't you please ignore this message and rest assured you will not be included in Rintez Medical Companion database or email listings.</p>
                <p><a href='"""+confirm_url+"""' style="background-color: Green;color: white;padding: 10px 20px;text-align: center;font-size: 20px;text-decoration: none;
            display: inline-block;border-radius: 15px;" target="_blank">Confirm</a></p>
                <p>Thank you,<br>Rintez Medical Companion<br>www.rintez.com</p>
            </body>
            </html>
            """
            subject = "[Rintez] Please confirm your email"
            send_email(user.email_id, subject, html)
            # flash("Successfully registered.", "success")
            flash('A confirmation email has been sent via email.', 'success')
    return redirect(url_for('home'))


port = os.getenv('PORT', '5000')
if __name__ == "__main__":
    if not os.path.exists('db.sqlite'):
        db.create_all()
    app.run(host='0.0.0.0', port=int(port),debug=True)