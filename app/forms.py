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
	noteid = IntegerField('Noteid: ')
	submit = SubmitField("Add note!")

class CommentForm(Form):
	comment = StringField('Comment')
	noteid = IntegerField('Noteid')
	submit = SubmitField("Add comment!")
