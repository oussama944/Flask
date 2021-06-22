from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth=Blueprint('auth',__name__)


@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Vous etes bien audentifié', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Mdp faux', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html",user=current_user)


@auth.route('/sign-up',methods=['GET','POST'])
def sign_up():
    if request.method=='POST':
        email=request.form.get('email')
        firstName=request.form.get('firstName')
        password1=request.form.get('password1')
        password2=request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('L*email existe déja', category='error')
        if len(email)<4:
            flash('Email doit etre plus long que 3',category='error')
        elif len(firstName)<2:
            flash('Nom doit etre plus long que 1',category='error')
        elif password1!=password2:
            flash('Pas le meme mod de passe',category='error')
        elif len(password1)<7:
            flash('MDP trop cour',category='error')
        else:
            #add user to database
            new_user = User(email=email, first_name=firstName, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            #update database
            db.session.commit()
            login_user(user, remember=True)
            flash('Compte créer',category='success')
            return redirect(url_for('views.home'))
    return render_template("sign_up.html",user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


