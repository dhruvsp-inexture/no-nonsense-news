from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
    """function for rendering error 404 template if 404 error is occurred

    Returns
    -------
    template
        shows the 404 error
    """
    return render_template('errors/404.html'), 404


@errors.app_errorhandler(403)
def error_403(error):
    """function for rendering error 403 template if 403 error is occurred

    Returns
    -------
    template
        shows the 403 error
    """
    return render_template('errors/403.html'), 403


@errors.app_errorhandler(500)
def error_500(error):
    """function for rendering error 500 template if 500 error is occurred

    Returns
    -------
    template
        shows the 500 error
    """
    return render_template('errors/500.html'), 500
