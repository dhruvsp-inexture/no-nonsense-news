from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import Length
from news_website.admin.utils import check_category


class AddCategoryForm(FlaskForm):
    """class for creating form for adding category

    Attributes
    ----------
    news_type: str
        category of the news
    submit: button
        for submitting the news_type
    """

    news_type = StringField('Add New Category', validators=[Length(min=2, max=20), check_category])
    submit = SubmitField('Add')


class FilterForm(FlaskForm):
    """class for filtering data for admin

    Attributes
    ----------
    filter_articles: dropdown
        used for filtering articles through a dropdown
    search: button
        used to submit the filter articles dropdown
    """

    filter_articles = SelectField('Filter By',
                                  choices=[('all_articles', 'All articles'), ('approved', 'Approved'),
                                           ('not_approved', 'Not Approved'), ('not_checked', 'Not checked'),
                                           ('checked', 'Checked')])

    search = SubmitField('Search')
