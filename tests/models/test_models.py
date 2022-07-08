from datetime import date
from news_website.models import User, UserType, NewsCategory, News, JournalistNewsMapping, NewsImageMapping, \
    PremiumUserMapping
from tests.base import ConfigDB
from tests.database.create_database import CreateDatabase


class TestModels(ConfigDB, CreateDatabase):

    def test_model_user_type(self):
        return self.insert_into_model_user_type("user")

    def test_get_user_type(self):
        user_type = self.insert_into_model_user_type("user")
        user_type_obj = UserType.query.filter_by(user_type_id=user_type.user_type_id).first()
        self.assertEqual(user_type.type, user_type_obj.type)

    def test_model_user(self):
        user_type = self.test_model_user_type()

        return self.insert_into_model_user("foo", "bar", "male", "abc@gmail.com", 9879878877, 23, "address of foobar",
                                           "123456", False, user_type.user_type_id)

    def test_get_user(self):
        user = self.test_model_user()
        user_obj = User.query.filter_by(id=user.id).first()
        self.assertEqual(user.first_name, user_obj.first_name)

    def test_model_news_category(self):
        return self.insert_into_news_category("Politics")

    def test_get_news_category(self):
        news_category = self.test_model_news_category()
        news_category_obj = NewsCategory.query.filter_by(category_id=news_category.category_id).first()
        self.assertEqual(news_category.category, news_category_obj.category)

    def test_model_news(self):
        news_category = self.test_model_news_category()
        return self.insert_into_news("This is the heading of the news", "This is the content of the news", date.today(),
                                     True, True, False, news_category.category_id)

    def test_get_news(self):
        news = self.test_model_news()
        news_obj = News.query.filter_by(news_id=news.news_id).first()
        self.assertEqual(news.news_heading, news_obj.news_heading)

    def test_model_journalist_news_mapping(self):
        user_type = self.insert_into_model_user_type("journalist")
        user = self.insert_into_model_user("foo", "bar", "male", "abc@gmail.com", 9879878877, 23, "address of foobar",
                                           "123456", False, user_type.user_type_id)
        news = self.test_model_news()
        return self.insert_into_journalist_news_mapping(user.id, news.news_id)

    def test_get_journalist_news_mapping(self):
        journalist_news_mapping = self.test_model_journalist_news_mapping()
        journalist_news_mapping_obj = JournalistNewsMapping.query.filter_by(
            journalist_id=journalist_news_mapping.journalist_id).first()
        self.assertEqual(journalist_news_mapping.news_id, journalist_news_mapping_obj.news_id)

    def test_model_news_image_mapping(self):
        news = self.test_model_news()
        return self.insert_into_news_image_mapping(news.news_id, "image.jpg")

    def test_get_news_image_mapping(self):
        news_image_mapping = self.test_model_news_image_mapping()
        news_image_mapping_obj = NewsImageMapping.query.filter_by(news_id=news_image_mapping.news_id).first()
        self.assertEqual(news_image_mapping.image, news_image_mapping_obj.image)

    def test_model_premium_user_mapping(self):
        user = self.test_model_user()
        return self.insert_into_premium_user_mapping(user.id)

    def test_get_premium_user_mapping(self):
        premium_user_mapping = self.test_model_premium_user_mapping()
        premium_user_mapping_obj = PremiumUserMapping.query.filter_by(
            premium_user_id=premium_user_mapping.premium_user_id).first()
        self.assertEqual(premium_user_mapping.user_id, premium_user_mapping_obj.user_id)
