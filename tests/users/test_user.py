from flask_login import current_user

from news_website import bcrypt
from news_website.users.forms import LoginForm, RegistrationForm, PasswordResetRequestForm
from tests.base import ConfigDB
from tests.database.create_database import CreateDatabase


class TestUser(ConfigDB, CreateDatabase):
    render_templates = False

    def insert_user_data(self):
        user_type = self.insert_into_model_user_type("user")
        user = self.insert_into_model_user("test", "test", "male", "test1@t1.in", 9234567890, 20, "testing",
                                           bcrypt.generate_password_hash("Test@123").decode('utf-8'), False,
                                           user_type.user_type_id)

    def test_login_success(self):
        self.insert_user_data()
        form = LoginForm()
        form.email.data = 'test1@t1.in'
        form.password.data = 'Test@123'
        data = form.data
        res = self.client.post('/login', data=data, follow_redirects=False)
        self.assert_message_flashed('Login Successful', 'success')
        self.assertEqual(res.status_code, 302)

    def test_login_failed(self):
        self.insert_user_data()
        form = LoginForm()
        form.email.data = 'abc@gmail.com'
        form.password.data = 'Test@12345'
        data = form.data
        res = self.client.post('/login', data=data, follow_redirects=False)
        self.assert_message_flashed('Login Unsuccessful. Please check email and password', 'danger')
        self.assertEqual(res.status_code, 200)

    def test_get_login_page(self):
        self.client.get('/login')
        self.assert_template_used('login.html')

    def registration_form_data(self):
        form = RegistrationForm()
        form.user_type.data = "user"
        form.first_name.data = "Test"
        form.last_name.data = "Test"
        form.gender.data = "male"
        form.email.data = "abc@gmail.com"
        form.phone.data = '9879878987'
        form.age.data = 23
        form.address.data = "addressssssssssssss"
        form.password.data = "Abc@123"
        form.confirm_password.data = "Abc@123"
        return form.data

    def test_register_success(self):
        self.insert_into_model_user_type("user")
        data = self.registration_form_data()
        res = self.client.post('/registration', data=data, follow_redirects=False)
        self.assert_message_flashed('Your account has been created! Now you can login to your account', 'success')
        self.assertEqual(res.status_code, 302)

    def test_registration_failed(self):
        self.insert_into_model_user_type("user")
        data = self.registration_form_data()
        data['first_name'] = "abc123"
        res = self.client.post('/registration', data=data, follow_redirects=False)
        self.assert_message_flashed('Please, Enter details correctly', 'warning')
        self.assertEqual(res.status_code, 200)

    def test_get_registration_fail(self):
        self.client.post('/registration')
        self.assert_template_used('registration.html')

    def test_registration_with_existing_email(self):
        user_type = self.insert_into_model_user_type("user")
        self.insert_into_model_user("test", "test", "male", "abc@gmail.com", 9234567890, 20, "testing",
                                    bcrypt.generate_password_hash("Abc@123"), False,
                                    user_type.user_type_id)
        data = self.registration_form_data()

        res = self.client.post('/registration', data=data, follow_redirects=False)
        self.assert_message_flashed('Please, Enter details correctly', 'warning')
        self.assertEqual(res.status_code, 200)

    def test_registration_with_existing_phone(self):
        user_type = self.insert_into_model_user_type("user")
        self.insert_into_model_user("test", "test", "male", "abcd@gmail.com", 9879878987, 20, "testing",
                                    bcrypt.generate_password_hash("Abc@123"), False,
                                    user_type.user_type_id)
        data = self.registration_form_data()
        res = self.client.post('/registration', data=data, follow_redirects=False)
        self.assert_message_flashed('Please, Enter details correctly', 'warning')
        self.assertEqual(res.status_code, 200)

    # def test_that_something_works(self):
    #     with self.client:
    #         form = LoginForm()
    #         form.email.data = "abc@gmail.com"
    #         form.password.data = "abc"
    #         response = self.client.post('/login', {email: 'James', password: '007'})
    #
    #         # success
    #         self.assertEqual(current_user.username, 'James')

    def test_get_profile_page_success(self):
        self.test_login_success()
        res = self.client.get('/profile/1', follow_redirects=False)
        self.assert_template_used('profile.html')

    def test_get_profile_page_fail(self):
        res = self.client.get('/profile/1', follow_redirects=False)
        self.assert_message_flashed('Please log in to access this page.', 'info')
