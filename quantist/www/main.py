from flask import Blueprint, render_template, request

bp = Blueprint('main', __name__)


@bp.route('/', methods=['GET', 'POST'])
def index():
    """
    Main landing page - Wall Street image, button
    :return: to invest
    """
    # TODO: invest button
    return render_template('index.html')


@bp.route('/about', methods=['GET', 'POST'])
def about():
    """
    Describe strategy and post button,
    :return: to report
    """
    if request.method == 'POST':
        # TODO: Add request
        return render_template('report.html', data=None)
    return render_template('about.html')
