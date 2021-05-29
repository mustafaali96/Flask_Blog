from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, DateTimeField, SelectField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User, Collection
# from flaskblog.cmodels import Customer

class UserRegistrationForm(FlaskForm):
	firstname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
	lastname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
	shop_name = StringField('Shop Name', validators=[Length(min=2, max=20)])
	number = StringField('Contact Number', validators=[DataRequired(), Length(min=2, max=20)])
	address = StringField('Address', validators=[DataRequired(), Length(min=2, max=20)])
	password = PasswordField('Password', validators=[DataRequired()])
	user_type = SelectField(u'User Type', choices=[('0', 'Customer'), ('1', 'Tailor')])
	embroidery = BooleanField('Embroidery')
	partywear = BooleanField('Party Wear')
	dailywear = BooleanField('Daily Wear')
	modestwear = BooleanField('Modest Wear')
	submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
	password = PasswordField('Password',validators=[DataRequired()])
	remember = BooleanField('Remeber Me')
	submit = SubmitField('Login')
	

class CustomerLoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
	password = PasswordField('Password',validators=[DataRequired()])
	remember = BooleanField('Remeber Me')
	submit = SubmitField('Login')



class UpdateTailorAccountForm(FlaskForm):
	firstname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
	lastname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
	# picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', ])])
	image = FileField('Profile Image')
	shop_name = StringField('Shop Name', validators=[DataRequired(), Length(min=2, max=20)])
	number = StringField('Contact Number', validators=[DataRequired(), Length(min=2, max=20)])
	address = StringField('Address', validators=[DataRequired(), Length(min=2, max=20)])
	# password = PasswordField('Password',validators=[DataRequired()])
	embroidery = BooleanField('Embroidery')
	partywear = BooleanField('Party Wear')
	dailywear = BooleanField('Daily Wear')
	modestwear = BooleanField('Moodest Wear')
	submit = SubmitField('Update')

class UpdateCustomerAccountForm(FlaskForm):
	firstname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
	lastname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
	# picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', ])])
	image = FileField('Profile Image') 
	number = StringField('Contact Number', validators=[DataRequired(), Length(min=2, max=20)])
	address = StringField('Address', validators=[DataRequired(), Length(min=2, max=20)])
	# password = PasswordField('Password',validators=[DataRequired()])
	submit = SubmitField('Update')

class AddCollectionForm(FlaskForm):
	price = StringField('Product Price', validators=[DataRequired(), Length(min=2, max=20)])
	# created_at = StringField('Created Time', validators=[DataRequired(), Length(min=2, max=20)])
	# product_picture = FileField('Update Picture', validators=[FileAllowed(['jpg', 'png', ])])
	product_image = FileField('Product Image')
	fabric = StringField('Fabric', validators=[DataRequired(), Length(min=2, max=20)])
	# updated_at = DateTimeField('Date', format='%m/%d/%y')
 # description = StringField('Description', validators=[DataRequired(), Length(min=2, max=20)])
	category = SelectField('Collection Type', choices=[('0', 'Abaya'), ('1', 'Hijab'), ('2', 'Hijab Caps'), ('3', 'Pins')])
	description = StringField('Description', validators=[DataRequired(), Length(min=2, max=20)])
	title = StringField('Product Name', validators=[DataRequired(), Length(min=2, max=20)])
	# uploaded_by = IntegerField('TailorId')


	embroidery = BooleanField('Embroidery')
	partywear = BooleanField('Party Wear')
	dailywear = BooleanField('Daily Wear')
	modestwear = BooleanField('Modest Wear')
	submit = SubmitField('Add')	


# class UpdateCustomerAccountForm(FlaskForm):
# 	firstname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
# 	lastname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
# 	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
# 	picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', ])])
# 	image = FileField('Profile Image', validators=[DataRequired()])
# 	number = StringField('Contact Number', validators=[DataRequired(), Length(min=2, max=20)])
# 	address = StringField('Address', validators=[DataRequired(), Length(min=2, max=20)])
# 	tailor_type = SelectField(u'User Type', choices=[('0', 'Customer'), ('1', 'Tailor')])
# 	submit = SubmitField('Update')

# 	def validate_username(self, username):
# 		if username.data != current_user.username:
# 			user = User.query.filterby(username=username.data).first()
# 			if user:
# 				raise ValidationError('That Customer password is taken. Please chose a different one.')


	# product_type = StringField('Product Type', validators=[DataRequired(), Length(min=2, max=20)])		
	# title = StringField('Product Title', validators=[DataRequired(), Length(min=2, max=20)])
	# fabric = StringField('Product Fabric', validators=[DataRequired(), Length(min=2, max=20)])
	# date_posted = DateField('Post Date', format='%Y-%m-%d')
	


    
	


# class RegistrationFormC(FlaskForm):
# 	firstname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
# 	lastname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
# 	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
# 	number = StringField('Contact Number', validators=[DataRequired(), Length(min=2, max=20)])
# 	address = StringField('Address', validators=[DataRequired(), Length(min=2, max=20)])
# 	password = PasswordField('Password', validators=[DataRequired()])
# 	tailor_type = SelectField(u'User Type', choices=[('0', 'Customer'), ('1', 'Tailor')])
# 	submit = SubmitField('Sign Up')

# 	def validate_username(self, username):
# 		customer = Customer.query.filterby(username=username.data).first()
# 		if customer:
# 			raise ValidationError('That Customer name is taken. Please chose a different one.')
