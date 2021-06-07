from flask import Blueprint

views=Blueprint('views',__name__);

@views.route('/')
def home():
    return"<h1>Test<h1>" 

@views.route('/logout')
def logout():
    return"<h1>Testeeeee<h1>" 

@views.route('/')
def sign_up():
    return"<h1>Tesxxxt<h1>" 

