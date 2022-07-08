from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, RadioField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from news_website.models import User
from news_website.users.utils import valid_number, valid_password, validate_name


class RegistrationForm(FlaskForm):
    """Registration form for user registration

    Attributes
    ----------

    user_type: radio button
        for selecting the type of the user
    first_name: str
        includes the first name of the user
    last_name: str
        includes the last name of the user
    gender: radio button
        for selecting the gender of the user
    email: str
        includes the email of the user
    phone: str
        includes the phone number of the user
    age: int
        includes the age of the user
    address: str
        includes the address of the user
    password: str
        includes the password of the user
    confirm_password: str
        for retyping the password of the user to match it with the password
    submit: button
        button for submitting the registration form

    Methods
    -------
    validate_phone
        validates the phone number of the user whether it exists in the database or not
    validate_email
        validates the email of the user whether it exists in the database or not

    """

    user_type = RadioField('Who are you?', choices=[('user', 'User'), ('journalist', 'Journalist')])
    first_name = StringField('First Name', validators=[DataRequired(), validate_name, Length(min=2, max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(), validate_name, Length(min=2, max=20)])
    gender = RadioField('Select Gender', choices=[('male', 'Male'), ('female', 'Female')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired(), valid_number, Length(min=10, max=10)])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(16, 200)])
    address = TextAreaField('Address', validators=[DataRequired(), Length(min=10, max=200)])
    password = PasswordField('Password', validators=[DataRequired(), valid_password, Length(min=6, max=18)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_phone(self, phone):
        """function for validating existing phone number

        Parameters
        ----------
        phone: int
            phone number of the user passed through registration form
        """

        user = User.query.filter_by(phone=phone.data).first()
        if user:
            raise ValidationError('That phone number is taken. Please choose a different one.')

    def validate_email(self, email):
        """function for validating existing email

        Parameters
        ----------
        email: str
            email of the user passed through registration form
        """

        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    """login form for user login

    Attributes
    ----------
    email: str
        email of the user used for login
    password: str
        password of the user used for login
    remember: boolean
        remembers the data of the user
    submit: button
        submit button for submitting the login form
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    """Form for updating user details

    Attributes
    ----------

    first_name: str
        includes the first name of the user
    last_name: str
        includes the last name of the user
    gender: radio button
        for selecting the gender of the user
    email: str
        includes the email of the user
    phone: str
        includes the phone number of the user
    age: int
        includes the age of the user
    address: str
        includes the address of the user
    submit: button
        submit button for submitting the details of the update form

    Methods
    -------
    validate_phone
        validates the phone number of the user whether it exists in the database or not
    validate_email
        validates the email of the user whether it exists in the database or not

    """
    first_name = StringField('First Name', validators=[DataRequired(), validate_name, Length(min=2, max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(), validate_name, Length(min=2, max=20)])
    gender = RadioField('Select Gender', choices=[('male', 'Male'), ('female', 'Female')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired(), valid_number, Length(min=10, max=10)])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(16, 200)])
    address = TextAreaField('Address', validators=[DataRequired(), Length(min=10, max=200)])
    submit = SubmitField('Update Details')

    def validate_phone(self, phone):
        """function for validating existing phone number of other user


        Parameters
        ----------
        phone: int
            phone number of the user passed while updating the details
        """

        user = User.query.filter_by(phone=phone.data).first()
        if user:
            if user.phone != current_user.phone:
                raise ValidationError('That phone number is taken. Please choose a different one.')

    def validate_email(self, email):
        """function for validating existing email of other user

        Parameters
        ----------
        email: str
            email of the user passed while updating the details
        """

        user = User.query.filter_by(email=email.data).first()
        if user:
            if user.email != current_user.email:
                raise ValidationError('That email is taken. Please choose a different one.')


class PasswordResetRequestForm(FlaskForm):
    """Password reset request form where user can request for password reset by submitting his/her email

    Attributes
    ----------
    email: str
        email of the user who is requesting to reset password
    submit: button
        button for submitting the request password request

    Methods
    -------

    validate_email
        method which checks whether the entered email exists in the database or not

    """
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        """checking if the user requesting for password change by submitting email is registered with that email or not

        Parameters
        ----------
        email: str
            email passed through the reset password request form

        """
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first')


class ResetPasswordForm(FlaskForm):
    """Password reset form for changing password after requesting for password reset

    Attributes
    ----------

    password: str
        new password of the user
    confirm_password: str
        confirm password which should be same as password entered
    submit: button
        button for submitting reset password form
    """
    password = PasswordField('Password', validators=[DataRequired(), valid_password, Length(min=6, max=18)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class changePassword(FlaskForm):
    """Change password form for changing the password

    Attributes
    ----------

    password: str
        current password of the user
    new_password: str
        new password of the user
    submit: button
        button for submitting change password form
    """
    password = PasswordField('Password',
                             validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), valid_password, Length(min=6, max=18)])
    submit = SubmitField('Change Password')
