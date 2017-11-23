from flask import Flask, request, render_template, redirect, url_for, json, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user
from forms import SignupForm, NoteForm, CommentForm
from flask_sqlalchemy import SQLAlchemy
import tempfile
import os.path



app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
#if using apple:
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

#if using windows:
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(tempfile.gettempdir(), 'test.db')
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
data = json.load(open('data.json'))

@login_manager.user_loader
def load_user(email):
    return User.query.filter_by(email = email).first()

@app.route('/')
def index():
    return "Create and share notes with your friends in awesomenotes!"

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'GET':
        
        return render_template('signup.html', form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            if User.query.filter_by(email=form.email.data).first():
                return "Email address already exists"
            else:
                newuser = User(form.email.data, form.password.data)
                db.session.add(newuser)
                db.session.commit()
                login_user(newuser)
                return "User created!!!"
        else:
            return "Form didn't validateeee"

@app.route('/login', methods=['GET','POST'])
def login():
    form = SignupForm()
    if request.method == 'GET':
        return render_template('login.html', form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                if user.password == form.password.data:
                    login_user(user)
                    return "User logged in"
                else:
                    return "Wrong password"
            else:
                return "user doesn't exist"
    else:
        return "form not validated"

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return "Logged out"

@app.route("/notes", methods = ['GET','POST'])
def notes():
    form = NoteForm()
    #id = User.get_id()
    id = 1
    print("iam here")
    if request.method == 'GET':
        context=data['users'][id-1]
        return render_template('notes.html', context=context, form = form)
    elif request.method == 'POST':
        print("here")
        if form.validate_on_submit():
            data['users'][id-1]['messages'].append("hello")
            print(data['users'][id-1])
            return render_template('notes.html', form = form)


@app.route("/viewnotes/<int:userid>", methods = ['GET'])
def viewnotes(userid):
    for user in data['users']:
        if user['id'] == userid:
            person = user
    user_notes = []
    for note in data['notes']:
        if note['userid'] == userid and note['private'] == 'False':
            user_notes.append(note)
    return jsonify({person['username'] + '\'s notes': user_notes})


#purely for authentication
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.email

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return id



if __name__ == '__main__':
    db.create_all()
    app.run(port=5000, host='localhost', debug=True)
