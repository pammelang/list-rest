from functools import wraps
from flask import Flask, Response, request, json, jsonify, abort, make_response, redirect, url_for
import time
app = Flask(__name__)
app.debug = True

# login_manager = LoginManager()
# login_manager.init_app(app)

# postgres
# user: networks
# password: 123456789

users = [
    {
        'id': 1,
        'username': 'pamm',
        'password': '12345',
        'email': 'pamm@gmail.com',
        'following': [2, 3],
        'messages': []
    },
    {
        'id': 2,
        'username': 'val',
        'password': '12345',
        'email': 'val@gmail.com',
        'following': [1, 3],
        'messages': []
    },
    {
        'id': 3,
        'username': 'tom',
        'password': '12345',
        'email': 'tom@gmail.com',
        'following': [1, 2],
        'messages': []
    },
    {
        'id': 4,
        'username': 'dan',
        'password': '12345',
        'email': 'dan@gmail.com',
        'following': [2],
        'messages': []
    }
]

notes = [
    {
        'noteid': 1,
        'userid': 1,
        'title': 'this is a todo list',
        'text': 'need to do ml & networks & db',
        'private': False,
        'comments': [{'userid': 2, 'text': 'wow that\'s alot'}, {'userid': 3, 'text': 'how to do ml?'}]
    },
    {
        'noteid': 2,
        'userid': 1,
        'title': 'grocery list',
        'text': 'buy detergent and broccoli',
        'private': False,
        'comments': [{'userid': 2, 'text': 'can you help me buy milk'}]
    },
    {
        'noteid': 3,
        'userid': 3,
        'title': 'reminder',
        'text': 'meet val at 3pm tomorrow',
        'private': True,
        'comments': []
    }
]

def auth(username, password):
    for user in users:
        if (username == user['username']):
            print("yes i come here")
            global own_id, current_user
            own_id = user['id']
            current_user = user
            return username == user['username'] and password == user['password']

#produces the authentication required pop up box
def authenticate():
    message = {'message': "Please authenticate."}
    resp = jsonify(message)
    resp.status_code=401
    resp.headers['WWW-Authenticate']='Basic realm="Please enter your User Name and Password to proceed"'
    return resp

#checks that login info is correct
def requireAuth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        autho = request.authorization
        if 'current_user' not in globals() or current_user == None:
            if not autho:
                return authenticate()
            elif not auth(autho.username, autho.password):
                return authenticate()
            else:
                return f(*args, **kwargs)
        elif not auth(current_user['username'], current_user['password']):
            return authenticate()
        else:
            return f(*args, **kwargs)
    return decorated

#sample curl method: curl -u username http://127.0.0.1:5000/login (input password as requested)
#sample curl method: curl -u username:password http://127.0.0.1:5000/login
@app.route('/')
@requireAuth
def api_root():
    return ('Create and share your notes with friends!')

# get/post own notes
#sample curl method: curl http://127.0.0.1:5000/notes
# sample curl method with plain text: 
#    curl http://127.0.0.1:5000/notes -X POST -H "Content-type: text/plain" -d "title text private"
@app.route('/notes', methods = ['GET', 'POST'])
@app.errorhandler(404)
def routes():
    if request.method == 'POST':
        if request.headers['Content-Type'] == 'text/plain':
            data = request.data.split()
            title = data[0].decode("utf-8")
            text = data[1].decode("utf-8")
            private = data[2].decode("utf-8")
            note = {
                'noteid': notes[-1]['noteid'] +1,
                'userid': own_id,
                'title': title,
                'text': text,
                'private': private
            }
            notes.append(note)
            return jsonify(notes)
        elif request.headers['Content-Type'] == 'application/json':
            data = json.loads(request.get_json())
            # data = request.get_json()
            note = {
                'noteid': notes[-1]['noteid'] +1,
                'userid': own_id,
                'title': data['title'],
                'text': data['text'],
                'private': data['private']
            }
            print("here")
            notes.append(note)
            return jsonify({'note': note}), 201
        else:
            return "415 unsupported media type"
    else:
        own_notes = []
        for note in notes:
             if note['userid'] == own_id:
                 own_notes.append(note)
        return jsonify({'notes': own_notes, 'own profile': current_user}), 201

# view, delete, update own note
#sample curl delete method: curl http://127.0.0.1:5000/notes/noteid -X DELETE
#sample curl put method: curl http://127.0.0.1:5000/notes/noteid -X PUT -d 
@app.route('/notes/<int:noteid>', methods = ['GET', 'DELETE', 'PUT'])
@app.errorhandler(404)
def get_note(noteid):
    note = [note for note in notes if note['id'] == noteid]
    if request.method == 'DELETE':
        notes.remove(note)
        return 201
    elif request.method == 'PUT':
        if request.headers['Content-Type'] == 'text/plain':
            data = json.loads(request.data)
        elif request.headers['Content-Type'] == 'application/json':
            data = request.json
        for key, value in data:
            if key in note:
                note[key] = value
        return 'You have successfully updated your note.', 201
    else:
        return jsonify({'note': note}), 201

# view other users' profiles (aka all their notes)
@app.route('/<int:userid>/notes', methods = ['GET'])
@app.errorhandler(404)
def get_other_notes(userid):
    for user in users:
        if user['id'] == userid:
            person = user
    user_notes = []
    for note in notes:
        if note['userid'] == userid and note['private'] == False:
            user_notes.append(note)
    return jsonify({ person['username'] + '\'s notes': user_notes}), 201


# post a comment on others' notes
# sample curl method: curl http://127.0.0.1:5000/userid/notes/noteid/comments -X PUT -d '{"text":"input_text_here"}'
@app.route('/<int:userid>/notes/<int:noteid>/comments', methods = ['POST','GET'])
@app.errorhandler(404)
def comment(userid, noteid):
    for note in notes:
        if note['noteid'] == noteid:
            temp = note
    if temp:
        if request.headers['Content-Type'] == 'text/plain':
            data = json.loads(request.data)
        elif request.headers['Content-Type'] == 'application/json':
            data = request.json
        else:
            return 'Unaccepted data type. Please use either json or text'
        comment = {
            'userid': own_id,
            'text': data['text']
        }
        temp['comments'].append(comment)
        return jsonify({'comment posted': note})
    else:
        return 'Note not found', 400

# follow others
# sample curl method: curl http://127.0.0.1:5000/userid/follow -X PUT
@app.route('/<int:userid>/follow', methods = ['PUT', 'GET'])
@app.errorhandler(404)
def follow(userid):
    to_follow = [user for user in users if user['id'] == userid]
    if to_follow:
        if userid not in current_user['following']:
            current_user['following'].append(userid)
            return jsonify({'Now following': current_user})
        else:
            return jsonify({'Already following!': current_user})
    else:

       return 'User not found', 400

# view following
# sample curl method: curl http://127.0.0.1:5000/dashboard
@app.route('/dashboard', methods = ['GET'])
@app.errorhandler(404)
def get_notes():
    followed_notes = []
    for note in notes:
        if note['userid'] in current_user['following'] and note['private'] == False:
            followed_notes.append(note)
    return jsonify({'followed': followed_notes, 'current profile': current_user}), 201

# share notes - send messages
# sample curl method: curl http://127.0.0.1:5000/notes/noteid/share/userid -X PUT
@app.route('/notes/<int:noteid>/share/<int:userid>', methods = ['PUT','GET'])
@app.errorhandler(404)
def share_with(noteid, userid):
    for user in users:
        if user['id'] == userid:
            person = user
    note = [note for note in notes if note['noteid'] == noteid]
    if person and note:
        message = {
            'userid': own_id,
            'noteid': noteid
        }
        person['messages'].append(message)
        return 'message sent!', 201
    else:
        return 'User or note not found', 400

# view messages
# sample curl method: curl http://127.0.0.1:5000/messages
@app.route('/messages', methods = ['GET'])
@app.errorhandler(404)
def get_messages():
    return jsonify({'messages': current_user['messages']}), 201

if __name__ == '__main__':
    app.run(debug=True)
