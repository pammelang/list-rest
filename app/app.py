from flask import Flask, request, render_template, redirect, url_for, json, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms import SignupForm, NoteForm, CommentForm
from flask_sqlalchemy import SQLAlchemy
from json2html import *
import tempfile
import os.path

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
#if using mac os:
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

#if using windows:
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(tempfile.gettempdir(), 'test.db')
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

users = []
notes = []


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
                newuser = User(form.email.data, form.password.data, form.username.data)
                db.session.add(newuser)
                db.session.commit()
                login_user(newuser)
                new_user = {'id': newuser.id, 'username': form.username.data,
                'password': form.password.data, 'email': form.email.data,
                'following': [], 'messages': []}
                users.append(new_user)
                return json2html.convert(json = {'user created': users})
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

@app.route("/profile")
@login_required
def get_current_user():
    for user in users:
        if user['id'] == current_user.id:
            return json2html.convert(json = {'my profile': user})
    return 'Profile not found'


@app.route("/notes", methods = ['GET','POST'])
@login_required
def routes():
    form = NoteForm()
    id = current_user.id
    user_notes=[]
    if request.method == 'GET':
        for note in notes:
            if note['userid'] == id:
                user_notes.append(note)
        return render_template('notes.html', context=user_notes, form = form)

    elif request.method == 'POST':
        if form.private.data != "" and form.title.data != "" and form.text.data != "":
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
            return redirect(url_for('routes'))
        elif form.noteid1.data != "" and form.title1.data != "" and form.note1.data !="" and form.private1.data !="":
            for note in notes:
                if note['noteid'] == form.noteid1.data:
                    note['title'] = form.title1.data
                    note['text'] = form.note1.data
                    note['private'] = form.private1.data
            return redirect(url_for('routes'))
        elif form.noteid.data != "":
            ctr = 0
            val = 1
            for note in notes:
                for noteid, value in note.items():
                    if value == form.noteid.data:
                        val = ctr
                        break
                ctr+=1
            del notes[val]
            return redirect(url_for('routes'))

@app.route("/viewnotes", methods = ['GET','POST'])
@app.route("/viewnotes/<int:userid>", methods = ['GET', 'POST'])
def viewnotes(userid=None):
    form = CommentForm()
    if request.method == 'GET':
        user_notes = []
        if userid != None:
            for note in notes:
                if note['userid'] == userid and note['private'] == 'False':
                    user_notes.append(note)
        else:
            for note in notes:
                if note['private'] == 'False':
                    user_notes.append(note)
        return render_template('viewnotes.html', form=form, context=user_notes)
    elif request.method == 'POST':
        noteid = form.noteid.data
        comment = form.comment.data
        temp = [{'userid': current_user.id, 'text': comment}]
        user_notes=[]
        for note in notes:
            if note['noteid']==noteid:
                note['comments'].append(temp)
            if note['private'] == 'False':
                user_notes.append(note)
        return redirect(url_for('viewnotes'))
    return render_template('viewnotes.html', form=form, context = "")

@app.route('/<string:username>/follow', methods = ['GET'])
@login_required
def follow(username):
    the_user = {}
    to_follow = {}
    for user in users:
        if user['id'] == current_user.id:
            user_index = users.index(user)
            the_user = user
        if user['username'] == username:
            to_follow = user
    if to_follow:
        if to_follow['id'] not in the_user['following']:
            the_user['following'].append(to_follow['id'])
            users[user_index] = the_user
            return json2html.convert(json = {'Now following': users[user_index]})
        else:
            return json2html.convert(json={'Already following!': to_follow})
    return json2html.convert(json={'Error': 'There is no user with that username',
        'users': users,
        'current_user': the_user}), 400

@app.route('/dashboard', methods = ['GET'])
@login_required
def get_notes():
    for user in users:
        if user['id'] == current_user.id:
            the_user = user
    # the_user = [user for user in users if user['id'] == current_user.id]
    followed_notes = []
    for note in notes:
        if note['userid'] in the_user['following'] and note['private'] == 'False':
            followed_notes.append(note)
    return json2htm.convert(json = {'followed notes': followed_notes, 'current profile': the_user}), 201

@app.route('/notes/<int:noteid>/share/<int:userid>', methods = ['GET'])
@login_required
def share_with(noteid, userid):
    the_user = [user for user in users if user['id'] == current_user.id]
    for user in users:
        if user['id'] == userid:
            person = user
            person_index = users.index(person)
    note = [note for note in notes if note['noteid'] == noteid]
    if person and note:
        message = {
            'userid': current_user.id,
            'noteid': noteid
        }
        users[person_index]['messages'].append(message)
        return 'message sent!', 201
    else:
        return 'User or note not found', 400

    return json2html.convert(json={'followed': followed_notes, 'current profile': the_user}), 201

# purely for authentication
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)

    def __init__(self, email, password, username):
        self.email = email
        self.password = password
        self.username = username

    def __repr__(self):
        return '<User %r>' % self.email

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.email

if __name__ == '__main__':
    db.create_all()
    app.run(port=5000, host='localhost', debug=True, threaded=True)
