from app.email import send_password_reset_email
from flask import render_template, flash, redirect, url_for, session
from flask_login import current_user, login_user
from app.models import Thing
from flask_login import logout_user
from flask import request
from werkzeug.urls import url_parse
from flask_login import login_required
from app import db
from app.forms import *
from datetime import datetime
from app import app


@app.route('/')
@app.route('/index')
def index():
    things = Thing.query.all()
    return render_template('index.html', title='Home', things=things)


@app.route('/filter_sex_type/<filter_sex>/<filter_type>')
def filter_sex_type(filter_sex, filter_type):
    things = Thing.query.filter_by(sex=filter_sex, type=filter_type).all()
    thing_t = Thing.query.filter_by(sex=filter_sex).all()
    thing_types = sorted(set([th.type for th in thing_t]))
    return render_template('index.html', title='Home', things=things, thing_types=thing_types, sex=filter_sex)

@app.route('/filter_index/<filter_sex>')
def filter_index(filter_sex):
    things = Thing.query.filter_by(sex=filter_sex).all()
    thing_types = sorted(set([th.type for th in things]))
    return render_template('index.html', title='Home', things=things, thing_types=thing_types, sex=filter_sex)

@app.route('/login', methods=['Get', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неправильные логин или пароль')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)


@app.route('/thing/<thing_id>', methods=['Get', 'POST'])
def thing(thing_id):
    thing = Thing.query.filter_by(id=thing_id).first()
    form = ThingForm()
    if form.validate_on_submit():
        if not session.get('cart'):
            session['cart'] = []

        session['cart'].append(thing.id)
        # flash('Шмотка добавлена в корзину.')
        return redirect(url_for('thing', thing_id=thing.id))
    return render_template('thing.html', title=thing.type, thing=thing, form=form)

@app.route('/cart_thing/<thing_id>', methods=['Get', 'POST'])
def cart_thing(thing_id):
    thing = Thing.query.filter_by(id=thing_id).first()
    return render_template('cart_thing.html', thing=thing)

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html', title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

@app.route('/cart')
def cart():
    things = []
    total_price = 0
    for i in session['cart']:
        t = Thing.query.filter_by(id=i).first()
        things.append(t)
        total_price += t.price
    return render_template("cart.html", things=things, total_price=total_price)

@app.route('/order')
def order():
    form = InformationAboutOrder()
    return render_template("order.html", form=form)
