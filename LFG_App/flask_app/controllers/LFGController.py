from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.login_model import User
from flask_app.models.game_model import Game
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return render_template('login_register.html', users = User.get_all_users())

@app.route('/register', methods = ['POST'])
def register():
    if not User.validate_user(request.form): #lil weird but, this is a dubl negative technically, if it returns false then it is false for being "not" so it's true
        return redirect('/')
    print('****REQUEST FORM****', request.form)
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash
    }
    
    user_id = User.create_user(data)
    session['user_id'] = user_id
    session['user_name'] = request.form['first_name']
    
    print('*********', session)
    print('*********', pw_hash)
    print('*********', data)
    
    return redirect('/welcome')

@app.route('/login', methods = ["POST"])
def login():
    user = User.validate_login(request.form)
    session['user_name'] = user.first_name
    if not user:
        flash('Invalid Email or Login')
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    return redirect('/welcome')

@app.route('/connect')
def connect_page():
    return render_template('connect.html')

@app.route('/welcome')
def welcome():
    user_name = session.get('user_name')
    games = Game.get_all_games()
    return render_template('welcome.html', user_name = user_name, games = games)

@app.route('/edit')
def edit():
    return render_template('edit.html')

@app.route('/logout')
def logout():
    session.clear
    return render_template('login_register.html')

@app.route('/results/<int:game_id>')
def get_results(game_id):
    user_has_games = Game.get_results(game_id)
    return render_template('results.html', user_has_games=user_has_games, game_id=game_id)

@app.route('/profile')
def profile_page():
    user_id = session.get('user_id')
    games = Game.get_all_games()
    return render_template('profile_page.html', games = games, user_id = user_id)

@app.route('/add_game', methods=['POST'])
def add_game():
    user_id = session.get('user_id')
    game_name = request.form['game_name']

    Game.add_game(user_id, game_name)

    return redirect('/profile')