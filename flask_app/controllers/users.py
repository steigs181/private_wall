from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import user
from flask_app.models import message
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

    # GET
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/wall')
def dashboard():
    user_id = session['user_id']
    one_user = user.User.get_one_user(user_id)
    messages = message.Message.get_all_messages_with_user()
    return render_template('wall.html', one_user = one_user, messages = messages)

    # POST
@app.route('/users/create', methods=['POST'])
def create_new_user():
    data = {
        'email': request.form['email']
    }
    if not user.User.validate_user(request.form):
        return redirect('/')
    if not user.User.get_by_email(data):
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password" : pw_hash
        }
        user_id = user.User.save_user(data)
        session['user_id'] = user_id
        return redirect('/wall')
    else:
        flash('User already exists')
        return redirect('/')


@app.route('/users/login', methods=['POST'])
def login():
    data = {
        'email': request.form['email']
    }
    user_in_db = user.User.get_by_email(data)
    if not user_in_db:
        flash('invalid email or password')
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Invalid password')
        return redirect('/')
    session["user_id"] = user_in_db.id
    return redirect('/wall')
