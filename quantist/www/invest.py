from flask import Blueprint, render_template

bp = Blueprint('invest', __name__)


@bp.route('/invest')
def index():
    return render_template('invest.html', posts=posts)
