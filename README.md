## REST API for notes sharing

### Introduction

This is a notes sharing app where users can follow and view their friends' notes.
There can be multiple clients accessing the server simultaneously.

### Features (ideas for now)
 - Create notes with a title and text or image.
 - Share notes with friends by sending a notification or by sending an email.
 - Follow friends' activities as they create notes
 - Have a private and public repository for notes

### How to run
On your terminal, go to folder where the file is located. Type the command "python rest.py", open up your browser and access the link: http://127.0.0.1:5000/ 
Run the following links to access the different routes available

home page: http://127.0.0.1:5000/
login page: http://127.0.0.1:5000/login
get/post own notes: http://127.0.0.1:5000/notes
view/delete/update own notes: http://127.0.0.1:5000/notes/<noteid>
view other profiles: http://127.0.0.1:5000/<userid>/notes
post a comment on others notes: http://127.0.0.1:5000/<userid>/notes/<noteid>/comments
follow other people: http://127.0.0.1:5000/<userid>/follow
view those you're following: http://127.0.0.1:5000/dashboard
share notes and send messages: http://127.0.0.1:5000/notes/<noteid>/share/<userid>
view your messages: http://127.0.0.1:5000/messages
 
The sample curl messages are as stated in the code. Open a second terminal instance and type the curl commands, remember to call the curl method for the login page first before accessing other curl methods.
