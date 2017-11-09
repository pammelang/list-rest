# view list of all bus stops and bus services at these locations
from functools import wraps
from flask import Flask, Response, request, json, jsonify, abort
app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'pickup': u'sutd',
        'deliverto': u'home',
        'items': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'pickup': u'orchard',
        'deliverto': u'yishun',
        'items': u'washing machine',
        'done': False
    }
]

# authentication
def check_auth(username, password):
    """This function is called to check if a username/password combination is valid."""
    return username == 'admin' and password == 'secret'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'+
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth:
            return authenticate()
        elif not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

# REST methods
@app.route('/')
def api_root():
    return 'Welcome to pamm\'s delivery service'

@app.route('/tasks', methods = ['GET', 'POST'])
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
#
#
#
# @auth.get_password
# def get_password(username):
#     if username == 'admin':
#         return 'password'
#     return None
#
# @auth.error_handler
# def unauthorized():
#     return make_response(jsonify({'error': 'Unauthorized access'}), 401)


if __name__ == '__main__':
    app.run(debug=True)
