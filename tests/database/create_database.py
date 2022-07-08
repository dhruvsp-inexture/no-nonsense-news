from news_website import db
from news_website.models import UserType, User, NewsCategory, News, JournalistNewsMapping, NewsImageMapping, \
    PremiumUserMapping


class CreateDatabase:

    def insert_into_model_user_type(self, user_type):
        user_type = UserType(type=user_type)
        db.session.add(user_type)
        db.session.commit()
        return user_type

    def insert_into_model_user(self, test_first_name, test_last_name, test_gender, test_email, test_phone, test_age,
                               test_address, test_password, test_has_premium, test_user_type_id):
        user = User(first_name=test_first_name, last_name=test_last_name, gender=test_gender, email=test_email,
                    phone=test_phone, age=test_age, address=test_address, password=test_password,
                    has_premium=test_has_premium,
                    user_type_id=test_user_type_id)
        db.session.add(user)
        db.session.commit()
        return user

    def insert_into_news_category(self, test_category):
        news_category = NewsCategory(category=test_category)
        db.session.add(news_category)
        db.session.commit()
        return news_category

    def insert_into_news(self, test_news_heading, test_news_info, test_news_date, test_is_approved, test_checked,
                         test_scraped_data, test_news_category_id):
        news = News(news_heading=test_news_heading,
                    news_info=test_news_info, news_date=test_news_date, is_approved=test_is_approved,
                    checked=test_checked,
                    scraped_data=test_scraped_data, news_category_id=test_news_category_id)
        db.session.add(news)
        db.session.commit()
        return news

    def insert_into_journalist_news_mapping(self, test_journalist_id, test_news_id):
        journalist_news_mapping = JournalistNewsMapping(journalist_id=test_journalist_id, news_id=test_news_id)
        db.session.add(journalist_news_mapping)
        db.session.commit()
        return journalist_news_mapping

    def insert_into_news_image_mapping(self, test_news_id, test_image):
        news_image_mapping = NewsImageMapping(news_id=test_news_id, image=test_image)
        db.session.add(news_image_mapping)
        db.session.commit()
        return news_image_mapping

    def insert_into_premium_user_mapping(self, test_user_id):
        premium_user_mapping = PremiumUserMapping(user_id=test_user_id)
        db.session.add(premium_user_mapping)
        db.session.commit()
        return premium_user_mapping
