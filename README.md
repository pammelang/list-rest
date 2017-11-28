## REST API for notes sharing
This is a REST api for concurrent notes sharing between

### Features
 - Create private or public notes with a title and text.
 - Share notes with friends by sending a notification message.
 - Follow friends
 - View friends' activities as they create notes
 - Work on and edit shared notes together

### How to run
On your terminal, cd into the 'rest' folder.  

Run `pip install -r requirements.txt`

Go into the file 'app.py' and use the section of code depending on your system (Windows/MacOS)

`if using mac os:
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
if using windows:
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(tempfile.gettempdir(), 'test.db')`

Run `python app.py`

Run the following links to access the different routes available

- home page: http://localhost:5000/
- signup: http://localhost:5000/signup
- login: http://localhost:5000/login
- logout: http://localhost:5000/logout
- view own profile: http://localhost:5000/profile
- view or post own notes: http://localhost:5000/notes
- view or comment on friends' notes: http://localhost:5000/viewnotes/@userid
- follow user: http://localhost:5000/@username/follow
- view friends' activities: http://localhost:5000/dashboard
- share a note with a friend: http://localhost:5000/notes/@noteid/share/@userid

* replace the @variables with your own created user variables
* to test the cross-user functions like follow, share and dashboard:
1. first create multiple users with signup.
2. then login to different users on different browser types (eg. Safari and Chrome).
3. proceed to create notes, follow friends, and view your dashboard.
