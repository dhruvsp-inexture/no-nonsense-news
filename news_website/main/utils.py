from news_website import db
from news_website.models import NewsCategory, News, NewsImageMapping, UserType


def get_latest_news_for_home_page(category_of_news):
    """function for getting latest news for home page

    Parameters
    ----------
    category_of_news: str
        category of news on which news object will be fetched and then stored accordingly in a dictionary

    Returns
    -------
    dictionary
        dictionary which contains the latest news stored from the object
    """
    news_category = NewsCategory.query.filter_by(category=category_of_news).first()
    news_data = News.query.filter_by(news_category_id=news_category.category_id, scraped_data=True).order_by(
        News.news_date.desc()).limit(3).all()
    news_dict_data = {}
    for news in news_data:
        data_news_id = news.news_id
        news_dict_data[data_news_id] = {}
        news_dict_data[data_news_id]["data"] = news
        images_data = NewsImageMapping.query.filter_by(news_id=data_news_id).first()
        news_dict_data[data_news_id]["image"] = images_data.image
    return news_dict_data, news_data


def insert_category(news_category):
    """function for inserting category into the NewsCategory table

    Parameters
    ----------
    news_category: str
        category of the news which is to be added into the NewsCategory table
    """
    category_obj = NewsCategory.query.filter_by(category=news_category).first()
    if not category_obj:
        news_category_obj = NewsCategory(category=news_category)
        db.session.add(news_category_obj)
        db.session.commit()


def insert_user_type(type_of_user):
    """function for inserting type of user into the UserType table

    Parameters
    ----------
    type_of_user: str
        user type which is to be added into the UserType table
    """
    user_type_obj = UserType.query.filter_by(type=type_of_user).first()
    if not user_type_obj:
        user_type = UserType(type=type_of_user)
        db.session.add(user_type)
        db.session.commit()
