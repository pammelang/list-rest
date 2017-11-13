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
        'email': 'pamm@gmail.com'
    },
    {
        'id': 2,
        'username': 'val',
        'password': '12345',
        'email': 'val@gmail.com'
    }
]

notes = [
    {
        'id': 1,
        'userid': 1
        'title': 'this is a todo list',
        'text': 'need to do ml & networks & db'
    },
    {
        'id': 2,
        'userid': 1
        'title': 'grocery list',
        'text': 'buy detergent and broccoli'
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

@app.route('/notes', methods = ['GET', 'POST'])
def routes():
    if request.method == 'POST':
        if request.headers['Content-Type'] == 'text/plain':
            data = json.loads(request.data)
            task = {
                'id': tasks[-1]['id'] +1,
                'pickup': data['pickup'],
                'deliverto': data['deliverto'],
                'length': data['length'],
                'price': int(data['length']) * 5
            }
            tasks.append(task)
            return task, 201
        elif request.headers['Content-Type'] == 'application/json':
            task = {
                'id': tasks[-1]['id'] +1,
                'pickup': request.json['pickup'],
                'deliverto': request.json['deliverto'],
                'length': request.json['length'],
                'price': request.json['length'] * 5
            }
            tasks.append(task)
            return jsonify({'task': task}), 201
        else:
            return "415 unsupported media type"
    else:
        return jsonify({'tasks': tasks})

@requires_auth
@app.route('/tasks/<int:taskid>', methods = ['GET', 'DELETE', 'PUT'])
def task(taskid):
    task = [task for task in tasks if task['id'] == taskid]
    if request.method == 'DELETE':
        tasks.remove(task[0])
        return jsonify({'updated tasks': tasks})
    elif request.method == 'PUT':
        task[0]['done'] = 'True'
        return jsonify({'updated task': task})
    else:
        return 'You are looking at ' + json.dumps(task)


if __name__ == '__main__':
    app.run(debug=True)
