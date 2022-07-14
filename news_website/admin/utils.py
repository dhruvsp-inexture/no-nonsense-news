from wtforms import ValidationError
from news_website.models import NewsCategory, News, NewsImageMapping, JournalistNewsMapping


def check_category(self, field):
    """function for checking whether the newly added category already exists or not

    Parameters
    ----------
    field: str
        it is used to check if the category already exists in the table or not

    Raises
    ------
    ValidationError
        if category_obj is not none
    """
    category_obj = NewsCategory.query.filter_by(category=field.data.title()).first()
    if category_obj:
        raise ValidationError('Category already exists please choose a different one.')


def get_distinct_news_category():
    """function for getting distinct news category id from the news table

    Returns
    -------
    list
        a list of distinct news categories
    """
    distinct_news_category = News.query.with_entities(News.news_category_id).distinct().all()
    return [i[0] for i in distinct_news_category]


def get_filtered_news(news_obj):
    """function for getting filtered news

    Parameters
    ----------
    news_obj: object
        news object is used to store data in dictionary which is obtained from the query

    Returns
    -------
    dict
        dictionary of with news data in it
    """

    news_data_dict = {}
    for data in news_obj.items:
        data_news_id = data.news_id
        news_data_dict[data_news_id] = {}
        news_data_dict[data_news_id]["data"] = data
        journalist_news_obj = JournalistNewsMapping.query.filter_by(news_id=data_news_id).first()
        news_data_dict[data_news_id]["author_id"] = journalist_news_obj.journalistnews.id
        news_data_dict[data_news_id]["author_first_name"] = journalist_news_obj.journalistnews.first_name
        news_data_dict[data_news_id]["author_last_name"] = journalist_news_obj.journalistnews.last_name
        img_obj = NewsImageMapping.query.filter_by(news_id=data_news_id).all()
        news_data_dict[data_news_id]["images"] = []
        if img_obj:
            for img in img_obj:
                # image_file = url_for('static', filename='news_images/' + img.image)
                news_data_dict[data_news_id]["images"].append(img.image)

    return news_data_dict
