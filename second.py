from flask import Blueprint, render_template

second = Blueprint('second', __name__, static_folder='static', template_folder='templates')

@second.route('/about')
@second.route('/')
def view():
    return render_template('about.html')