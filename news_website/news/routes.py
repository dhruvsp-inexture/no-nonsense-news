from flask import Blueprint, render_template

news = Blueprint("news", __name__)


@news.route('/post_article')
def post_articles_page():
    """function for posting articles by journalist"""

    return render_template('post_article.html')
