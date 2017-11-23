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

users = [
    {
        "id": 1,
        "username": "pamm",
        "password": "12345",
        "email": "pamm@gmail.com",
        "following": [2, 3],
        "messages": []
    },
    {
        "id": 2,
        "username": "val",
        "password": "12345",
        "email": "val@gmail.com",
        "following": [1, 3],
        "messages": []
    },
    {
        "id": 3,
        "username": "tom",
        "password": "12345",
        "email": "tom@gmail.com",
        "following": [1, 2],
        "messages": []
    },
    {
        "id": 4,
        "username": "dan",
        "password": "12345",
        "email": "dan@gmail.com",
        "following": [2],
        "messages": []
    }
]
notes = [
    {
        "noteid": 1,
        "userid": 1,
        "title": "this is a todo list",
        "text": "need to do ml & networks & db",
        "private": "False",
        "comments": [{"userid": 2, "text": "wow thats alot"}, {"userid": 3, "text": "how to do ml?"}]
    },
    {
        "noteid": 2,
        "userid": 1,
        "title": "grocery list",
        "text": "buy detergent and broccoli",
        "private": "False",
        "comments": [{"userid": 2, "text": "can you help me buy milk"}]
    },
    {
        "noteid": 3,
        "userid": 3,
        "title": "reminder",
        "text": "meet val at 3pm tomorrow",
        "private": "True",
        "comments": []
    }
]


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
            return "Form didn't validate"

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

@app.route("/notes", methods = ['GET','POST','DELETE'])
def routes():
    form = NoteForm(request.form)
    id = 1
    if request.method == 'GET':

        user_notes=[]
        for note in notes:
            if note['userid'] == id:
                user_notes.append(note)
        return render_template('notes.html', context=user_notes, form = form)
    elif request.method == 'POST':
        private = form.private.data
        title = form.title.data
        text = form.note.data
        noteid = len(notes)
        temp = {'noteid':noteid, 'userid':id,'title':title,'text':text,'private':private,'comments':[]}
        notes.append(temp)
        user_notes=[]
        for note in notes:
            if note['userid'] == id:
                user_notes.append(note)
        return render_template('notes.html', context=user_notes, form = form)

    elif request.method == 'DELETE':
        noteid = form.noteid.data
        user_notes=[]
        print("hre")
        for note in notes:
            print("in here")
            if note['noteid'] == noteid:
                print('hi')
                del note
                print(notes)
            if note['userid'] == id:
                user_notes.append(note)
        #return render_template('notes.html', context=user_notes, form=form)
    else:
        return "fail"

@app.route("/viewnotes", methods = ['GET','POST'])
@app.route("/viewnotes/<int:userid>", methods = ['GET', 'POST'])
def viewnotes(userid=None):
    form = CommentForm()
    if request.method == 'GET':
        for user in users:
            if user['id'] == userid:
                person = user
        user_notes = []
        for note in notes:
            if note['userid'] == userid and note['private'] == 'False':
                user_notes.append(note)
        return render_template('viewnotes.html', form=form, context=user_notes)
    elif request.method == 'POST':
        noteid = form.noteid.data
        comment = form.comment.data
        user_notes=[]
        for note in notes:
            if note['noteid']==noteid:
                note['comments'].append(comment)
            if note['userid'] == userid and note['private'] == 'False':
                user_notes.append(note)
        return redirect(url_for('viewnotes/1'))


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


