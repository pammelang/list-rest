from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, DataRequired

class SignupForm(Form):
    email = StringField('email',validators=[DataRequired(),Email()])
    password = PasswordField('password', validators=[DataRequired()])
    username = StringField(u'username', validators=[DataRequired()])
    
    submit = SubmitField("Sign In")

class NoteForm(Form):
	note = StringField('Note:', validators = [DataRequired()])
	submit = SubmitField("Add note!")

class CommentForm(Form):
	comment = StringField('comment', validators = [DataRequired()])
	submit = SubmitField("Add comment!")