from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy import PrimaryKeyConstraint
from . import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    """function for loading the user"""
    return User.query.get(user_id)


class UserType(db.Model):
    """model for storing different types of user along with their ids"""

    __tablename__ = "user_type"
    user_type_id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), unique=True, nullable=False)
    type_of_user = db.relationship('User', backref='usertype', lazy=True)


class User(db.Model, UserMixin):
    """model for storing user information and user id"""

    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    age = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String, nullable=False)
    has_premium = db.Column(db.Boolean, default=False, nullable=False)
    user_type_id = db.Column(db.Integer, db.ForeignKey('user_type.user_type_id'))
    journalist_news = db.relationship('JournalistNewsMapping', backref='journalistnews', lazy=True)
    premium_user = db.relationship('PremiumUserMapping', backref='premiumusermapping', cascade="all, delete-orphan",
                                   lazy="joined")

    def get_reset_token(self, expires_sec=1800):
        """function to get the reset token which will expire in 30 minutes

        Parameters
        ----------
        expires_sec: int
            time to expire the token in seconds

        Returns
        -------
        string
            contains the token by converting json to string
        """

        serializer = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return serializer.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        """function for verifying the reset token

        Parameters
        ----------
        token: str
            token which is generated while requesting reset password is loaded here
        Returns
        -------
        object
            contains the user object from given user_id
        """

        serializer = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = serializer.loads(token)['user_id']
        except (KeyError, Exception):
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.first_name}', '{self.email}')"


class NewsCategory(db.Model):
    """model for different categories of news"""

    __tablename__ = "news_category"
    category_id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(30), unique=True, nullable=False)
    category_type = db.relationship('News', backref='categorytype', lazy=True)


class News(db.Model):
    """model for news and its information"""

    __tablename__ = "news"
    news_id = db.Column(db.Integer, primary_key=True)
    news_heading = db.Column(db.String, nullable=False)
    news_info = db.Column(db.String, nullable=False)
    news_date = db.Column(db.DateTime)
    is_approved = db.Column(db.Boolean)
    checked = db.Column(db.Boolean)
    scraped_data = db.Column(db.Boolean)
    news_category_id = db.Column(db.Integer, db.ForeignKey('news_category.category_id'))
    news_journalist = db.relationship('JournalistNewsMapping', backref='newsjournalist', lazy=True)
    news_image = db.relationship('NewsImageMapping', backref='newsimage', cascade="all, delete-orphan", lazy="joined")


class JournalistNewsMapping(db.Model):
    """model for mapping journalist(user) id and news id"""

    __tablename__ = "journalist_news_mapping"
    __table_args__ = (
        PrimaryKeyConstraint('journalist_id', 'news_id'),
    )
    journalist_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    news_id = db.Column(db.Integer, db.ForeignKey('news.news_id'), nullable=False)


class NewsImageMapping(db.Model):
    """model for news id and images mapping"""

    __tablename__ = "news_image_mapping"
    __table_args__ = (
        PrimaryKeyConstraint('news_id', 'image'),
    )
    news_id = db.Column(db.Integer, db.ForeignKey('news.news_id'))
    image = db.Column(db.String)


class PremiumUserMapping(db.Model):
    """model for premium user mapping who buys subscription"""

    __tablename__ = "premium_user_mapping"
    premium_user_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    purchase_date = db.Column(db.DateTime)
