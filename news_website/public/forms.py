from flask_wtf import FlaskForm
from wtforms import SubmitField


class CategoryFilterForm(FlaskForm):
    """form for category filtering

     Attributes
    ----------
    search: button
        button for searching the category of the news selected
    """
    search = SubmitField('Search')
