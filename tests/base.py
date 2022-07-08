from flask_testing import TestCase

from run import app
from news_website import db


class ConfigDB(TestCase):
    render_templates = False

    def setUp(self):
        print("Creating test database...")
        db.create_all()

    def tearDown(self):
        print("Removing test database...")
        db.session.remove()
        db.drop_all()

    def create_app(self):
        # app = create_app()
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_TEST_DATABASE_URI'] = "sqlite:////tmp/test.db"
        return app
