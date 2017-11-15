# view list of all bus stops and bus services at these locations
from functools import wraps
from flask import Flask, Response, request, json, jsonify, abort, make_response, g
from flask_httpauth import HTTPBasicAuth
app = Flask(__name__)
app.debug = True

auth = HTTPBasicAuth()
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
        'following': [2, 3]
    },
    {
        'id': 2,
        'username': 'val',
        'password': '12345',
        'email': 'val@gmail.com',
        'following': [1, 3]
    },
    {
        'id': 3,
        'username': 'tom',
        'password': '12345',
        'email': 'tom@gmail.com',
        'following': [1, 2]
    }
]

notes = [
    {
        'id': 1,
        'userid': 1,
        'title': 'this is a todo list',
        'text': 'need to do ml & networks & db',
        'private': False,
        'comments': [{'userid': 2, 'text': 'wow that\'s alot'}, {'userid': 3, 'text': 'how to do ml?'}]
    },
    {
        'id': 2,
        'userid': 1,
        'title': 'grocery list',
        'text': 'buy detergent and broccoli',
        'private': False,
        'comments': [{'userid': 2, 'text': 'can you help me buy milk'}]
    },
    {
        'id': 3,
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
			global own_id
			own_id = user['id']
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
		if not autho:
			return authenticate()
		elif not auth(autho.username, autho.password):
			return authenticate()
        # else:
        #     return 'weird indentation isn't working'
        # global current_user
        # current_user = [user for user in users if user['id'] == own_id]
		return f(*args, **kwargs)
	return decorated


@app.route('/')
def api_root():
    return 'Create and share your notes with friends!'

# get/post own notes
@app.route('/notes', methods = ['GET', 'POST'])
@requireAuth
def routes():
    if request.method == 'POST':
        if request.headers['Content-Type'] == 'text/plain':
            data = json.loads(request.data)
            note = {
                'id': notes[-1]['id'] +1,
                'userid': own_id,
                'title': data['title'],
                'text': data['text'],
                'private': data['private'] == 'True'
            }
            notes.append(note)
            return note, 201
        elif request.headers['Content-Type'] == 'application/json':
            note = {
                'id': notes[-1]['id'] +1,
                'userid': own_id,
                'title': request.json['title'],
                'text': request.json['text'],
                'private': request.json['private']
            }
            notes.append(note)
            return jsonify({'note': note}), 201
        else:
            return "415 unsupported media type"
    else:
        own_notes = []
        for note in notes:
             if note['userid'] == own_id:
                 own_notes.append(note)
        return jsonify({'notes': own_notes}), 201

# view, delete, update own note
@app.route('/notes/<int:noteid>', methods = ['GET', 'DELETE', 'PUT'])
@requireAuth
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
def get_other_notes(userid):
    for user in users:
        if user['id'] == userid:
            person = user
    user_notes = []
    for note in notes:
        if note['userid'] == userid and note['private'] == False:
            user_notes.append(note)
    return jsonify({ user['username'] + '\'s notes': user_notes}), 201


# post a comment on others' notes
@app.route('/<int:userid>/notes/<int:noteid>/comments', methods = ['POST'])
@requireAuth
def comment(userid, noteid):
    note = [note for note in notes if note['id'] == noteid]
    if note:
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
        note['comments'].append(comment)
        return jsonify({'comment posted': note})
    else:
        return 'Note not found', 400

# follow others
@app.route('/<int:userid>/follow', methods = ['PUT'])
@requireAuth
def follow(userid):
    to_follow = [user for user in users if user['id'] == userid]
    if to_follow:
        if to_follow not in current_user['following']:
            current_user['following'].append(userid)
        else:
            return 'Already following!'
        return jsonify({'comment posted': note})
    else:
        return 'Note not found', 400

# view following

# share notes - send notifications 

if __name__ == '__main__':
    app.run(debug=True)