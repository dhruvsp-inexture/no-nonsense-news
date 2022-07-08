from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask.views import MethodView
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy.exc import IntegrityError

from news_website import db, bcrypt
from news_website.main.utils import insert_user_type
from news_website.users.forms import LoginForm, RegistrationForm, PasswordResetRequestForm, ResetPasswordForm, \
    UpdateAccountForm, changePassword
from news_website.models import User, UserType
from news_website.users.utils import send_reset_email

users = Blueprint("users", __name__)


class LoginPage(MethodView):
    """class for login page to get the login page and posting the data of the user for login"""

    def get(self):
        """method for getting the login page for user"""
        if current_user.is_authenticated:
            return redirect(url_for('home_page'))
        return render_template('login.html', form=LoginForm())

    def post(self):
        """method for posting the data for logging in"""
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                flash('Login Successful', 'success')
                return redirect(url_for('home_page'))
            else:
                flash('Login Unsuccessful. Please check email and password', 'danger')

        return render_template('login.html', form=form)


class RegistrationPage(MethodView):
    """class for getting registration page and posting the data of the user after registration"""

    def get(self):
        """method for getting the registration page"""
        if current_user.is_authenticated:
            return redirect(url_for('home_page'))
        return render_template('registration.html', form=RegistrationForm())

    def post(self):
        """method for posting data of the registration form and adding it to the database"""
        try:
            form = RegistrationForm()
            if form.validate_on_submit():
                type_of_user = UserType.query.filter_by(type=form.user_type.data).first()
                hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                user = User(user_type_id=type_of_user.user_type_id, first_name=form.first_name.data,
                            last_name=form.last_name.data, gender=form.gender.data, email=form.email.data,
                            phone=form.phone.data, age=form.age.data, address=form.address.data,
                            password=hashed_password)
                db.session.add(user)
                db.session.commit()

                flash('Your account has been created! Now you can login to your account', 'success')
                return redirect(url_for('login_page'))
            else:
                flash('Please, Enter details correctly', 'warning')
                return render_template('registration.html', form=form)

        except (AttributeError, IntegrityError):
            insert_user_type("admin")
            insert_user_type("journalist")
            insert_user_type("user")
            admin_user_obj = User(first_name="admin", last_name="admin", gender="male", email="admin@gmail.com",
                    phone="9876543210", age=21, address="anonymous location", password=bcrypt.generate_password_hash("Abc@123").decode('utf-8'),
                    user_type_id="1")
            db.session.add(admin_user_obj)
            print(admin_user_obj)
            db.session.commit()
            return render_template('registration.html', form=RegistrationForm())


class ProfilePage(MethodView):
    """class for getting the profile page of the user"""

    decorators = [login_required]

    def get(self, user_id):
        """method for getting the profile page of the current user

        Parameters
        ----------
        user_id: int
            id of the current user
        """
        if user_id == current_user.id:
            form = UpdateAccountForm()
            form.first_name.data = current_user.first_name
            form.last_name.data = current_user.last_name
            form.email.data = current_user.email
            form.phone.data = current_user.phone
            form.age.data = current_user.age
            form.gender.data = current_user.gender
            form.address.data = current_user.address
            type_of_user = UserType.query.filter_by(user_type_id=current_user.user_type_id).first()
            return render_template('profile.html', typeOfUser=type_of_user, form=form)
        else:
            abort(403)

    def post(self, user_id):
        """method for posting the data for updating user profile"""
        form = UpdateAccountForm()
        if form.validate_on_submit():
            current_user.first_name = form.first_name.data
            current_user.last_name = form.last_name.data
            current_user.email = form.email.data
            current_user.phone = form.phone.data
            current_user.age = form.age.data
            current_user.gender = form.gender.data
            current_user.address = form.address.data
            db.session.commit()
            flash('Your account has been updated!', 'success')
            return redirect(url_for('profile_page', user_id=current_user.id))
        type_of_user = UserType.query.filter_by(user_type_id=current_user.user_type_id).first()
        return render_template('profile.html', typeOfUser=type_of_user, form=form)


class Logout(MethodView):
    """class for user logout"""

    def get(self):
        """method for user logout and then redirecting it to home page"""
        logout_user()
        return redirect(url_for('home_page'))


class ResetPasswordRequest(MethodView):
    """class for getting the home page if user is already logged in and posting the data of password reset request
    form"""

    def get(self):
        """method for getting reset password request page for the user"""
        if current_user.is_authenticated:
            return redirect(url_for('home_page'))
        return render_template('reset_password_request.html', form=PasswordResetRequestForm())

    def post(self):
        """method for checking if the email is valid """
        form = PasswordResetRequestForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            send_reset_email(user)
            flash('An email has been sent to your id please check it to reset your password.', 'info')
            return redirect(url_for('login_page'))
        return render_template('reset_password_request.html', form=form)


class ResetToken(MethodView):
    """class for getting the home page if the user is already logged in and posting the data of the user after the
     password reset"""

    def get(self, token):
        """method for getting reset token page for the user reset password request"""
        if current_user.is_authenticated:
            return redirect(url_for('home_page'))
        return render_template('reset_token.html', form=ResetPasswordForm())

    def post(self, token):
        """method for verifying the token to reset the password and creating new password for the user"""
        user = User.verify_reset_token(token)
        if user is None:
            flash('That is an invalid or expired token', 'warning')
            return redirect(url_for('reset_password_request'))
        form = ResetPasswordForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user.password = hashed_password
            db.session.commit()
            flash('Your password has been updated! You can now log in', 'success')
            return redirect(url_for('login_page'))
        return render_template('reset_token.html', form=form)


class ChangePasswordPage(MethodView):
    """class for changing password"""

    decorators = [login_required]

    def get(self):
        """method for getting the change password page for the user"""
        form = changePassword()
        return render_template('change_password.html', form=form)

    def post(self):
        """method for changing the password for the user based on the old password"""
        form = changePassword()
        if form.validate_on_submit():

            if bcrypt.check_password_hash(current_user.password, form.password.data):
                hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
                current_user.password = hashed_password
                db.session.commit()
                flash('Password updated successfully', 'success')
                return redirect(url_for('profile_page', user_id=current_user.id))
            else:
                flash('Incorrect old password', 'danger')
        return render_template('change_password.html', form=form)
