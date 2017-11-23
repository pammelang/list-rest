from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, IntegerField,validators
from wtforms.validators import Email, DataRequired

class SignupForm(Form):
    email = StringField('email',validators=[DataRequired(),Email()])
    password = PasswordField('password', validators=[DataRequired()])
    username = StringField(u'username')
    submit = SubmitField("Sign In")

class NoteForm(Form):
	note = StringField('Note: ')
	title = StringField('Title: ')
	private = StringField('Private: ')
	note1 = StringField('Note: ')
	title1 = StringField('Title: ')
	private1 = StringField('Private: ')
	noteid1 = IntegerField('Note id: ')
	noteid = IntegerField('Note id: ')
	submit = SubmitField("Add note!")

class CommentForm(Form):
	comment = StringField('Comment')
<<<<<<< HEAD
	noteid = IntegerField('Note id')
	submit = SubmitField("Add comment!")
=======
	noteid = IntegerField('Noteid')
	submit = SubmitField("Add comment!")
>>>>>>> 30bcf5974c01df917c578be535c2647f53eb522e
