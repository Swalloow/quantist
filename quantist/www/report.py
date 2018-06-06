from flask import Blueprint, render_template

bp = Blueprint('report', __name__)


@bp.route('/report')
def index():
    return render_template('report.html')
