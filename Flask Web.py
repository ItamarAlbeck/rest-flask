from flask import Flask, render_template, url_for, redirect, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from second import second


app = Flask(__name__)
app.register_blueprint(second, url_prefix='/admin')
app.secret_key = 'hello'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=5)

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(100))
    email = db.Column('email', db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email


@app.route('/home')
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/view')
def view():
     return render_template('view.html', values=users.query.all())

@app.route('/login', methods=["POST", "GET"])
def login():
        if request.method == 'POST':
            session.permanent = True
            user = request.form['nm']
            session['user'] = user

            found_user = users.query.filter_by(name=user).first()
            if found_user:
                session['email'] = found_user.email
            else:
                usr = users(user, '')
                db.session.add(usr)
                db.session.commit()
            flash('login succesful!')
            return redirect(url_for('user'))
        else:
            if 'user' in session:
                flash('already logged in!')
                return redirect(url_for("user"))
            return render_template("login.html")


@app.route('/user', methods=['POST', 'GET'])
def user():
    email = None
    if 'user' in session:
        user = session['user']
        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            found_user = users.query.filter_by(name=user).first()
            found_user.email = email
            flash('Email was saved!')
            db.session.commit()
        else:
            if 'email' in session:
                email = session['email']
        return render_template('user.html', email=email)
    else:
        flash('you are not logged in!')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    if 'user' in session:
        user = session['user']
        flash(f"you have been logout!, {user}", "info")
    session.pop("user", None)
    session.pop('email', None)
    return redirect(url_for("login"))

@app.route('/HackerTyper')
def Typer():
    return render_template('HackerTyper.html')


if __name__ == '__main__':
    db.create_all()
    app.run(port=5001, debug=True)
