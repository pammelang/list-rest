# view list of all bus stops and bus services at these locations
from functools import wraps
from flask import Flask, Response, request, json, jsonify, abort, make_response
from flask_httpauth import HTTPBasicAuth
app = Flask(__name__)
auth = HTTPBasicAuth()

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

# authentication
@auth.get_password
def get_password(username):
    password = [user['password'] for user in users if username == user['username']]
    return password

@auth.error_handler
def unauthorized():
    return make_response(jsonify( { 'error': 'Unauthorized access' } ), 403)
    # return 403 instead of 401 to prevent browsers from displaying the default auth dialog

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)


# REST methods
@app.route('/')
def api_root():
    return 'Create and share your notes with friends!'

# get/post own notes
@app.route('/<int:userid>/notes', methods = ['GET', 'POST'])
@auth.login_required
def routes():
    if request.method == 'POST':
        if request.headers['Content-Type'] == 'text/plain':
            data = json.loads(request.data)
            note = {
                'id': notes[-1]['id'] +1,
                'userid': userid,
                'title': data['title'],
                'text': data['text'],
                'private': data['private']
            }
            notes.append(note)
            return note, 201
        elif request.headers['Content-Type'] == 'application/json':
            note = {
                'id': notes[-1]['id'] +1,
                'userid': userid,
                'title': request.json['title'],
                'text': request.json['text'],
                'private': request.json['private']
            }
            notes.append(note)
            return jsonify({'note': note}), 201
        else:
            return "415 unsupported media type"
    else:

        # TODO - need to deal with user authentication - sessions or tokens??

        return jsonify({'notes': notes})

# view, delete, update own note
@app.route('/<int:userid>/notes/<int:noteid>', methods = ['GET', 'DELETE', 'PUT'])
@auth.login_required
def get_note(noteid):
    note = [note for note in notes if note['id'] == noteid]
    if request.method == 'DELETE':
        notes.remove(note[0])
        return 201
    elif request.method == 'PUT':
        note[0]['done'] = 'True'
        return 201
    else:
        return 'You are looking at ' + json.dumps(note)


# view other users' profiles (aka all their notes)
@app.route('/<int:userid>/notes', methods = ['GET'])
def get_other_notes(userid):
    user = [user for user in users if user['id'] == userid]
    user_notes = []
    for note in notes:
        if note['user_id'] == userid and note['private'] == False:
            user_notes.append(note)
    return jsonify({user['username'] + '\'s notes': user_notes}), 201


# post a comment on others' notes
@app.route('/<int:userid>/notes/<int:noteid>/comments', methods = ['POST'])
@auth.login_required
def comment(userid, noteid):
    return


@app.route('/notes/<int:noteid>', methods = ['DELETE', 'PUT'])
def note(noteid):
    note = [note for note in notes if note['id'] == noteid]
    if request.method == 'DELETE':
        notes.remove(note[0])
        return jsonify({'updated notes': notes})
    elif request.method == 'PUT':
        note[0]['done'] = 'True'
        return jsonify({'updated note': note})
    else:
        return 'You are looking at ' + json.dumps(note)


if __name__ == '__main__':
    app.run(debug=True)
