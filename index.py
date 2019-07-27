from flask import Flask, render_template, request, redirect, url_for, flash, json
from flask import make_response
from flask import session
from flask_mysqldb import MySQL 
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import check_password_hash
from config import DevelopmentConfig

from models import db
from models import User
from models import Coment
from helper import date_format

from flask_mail import Mail
from flask_mail import Message

import forms

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()
mail = Mail()

@app.before_request #esto se ejcuta antes de "/", por ejemplo aca chequeamos si el usuario se ha chequeado
def before_request():
    if 'username' not in session and request.endpoint in ['inicio','coment','reviews'] :
        return redirect(url_for('login'))
    elif 'username' in session and request.endpoint in ['login','nuevo_registro']:
        return redirect(url_for('inicio'))

@app.after_request
def after_request(response):
    return response

@app.route("/")
def inicio():
    form = forms.formulario_coment(request.form) 
    if 'username' in session:           #se chequea si username esta dentro del dicionario de session
        username = session['username']  # se asigna a una variable la session
        print('variable de session: ',username) #se imprime en el terminal
    return render_template('inicio.html', form = form, titulo = "Inicio",user = username)

@app.route("/nuevo_registro", methods=[ 'GET' ,'POST'])
def nuevo_registro():
    form = forms.formulario_registro(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.username.data, form.email.data, form.password.data)
        db.session.add(user)
        db.session.commit()
        success_message = 'Usuario creado existosamente'   
        flash(success_message)
    else:
        print(form.errors)
        print(form.username.errors)
    return render_template('form_registro.html', form = form)

@app.route("/login", methods=[ 'GET' ,'POST'])
def login():
    form = forms.formulario_login(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username = username).first()
        if user and user.verify_password(password):
            session['username'] = username
            session['user_id']  = user.id #se toma el id del username y se crea la session, esto se hixo para poder registrar los comentarios posteriomente
            success_message = 'Bienvenido al sistema, {}'.format(username) 
            flash(success_message)
            return redirect(url_for('inicio'))        
        else:
            error_message = 'Usuario o contraseña no valida'
            flash(error_message)
    return render_template('login.html', form = form)

@app.route("/coment", methods=[ 'GET' ,'POST'])
def coment():
    form = forms.formulario_coment(request.form)
    user_id = session['user_id']
    username = session['username']
    if request.method == 'POST' and form.validate():
        coment = Coment(user_id = user_id,text = form.coment.data)
        db.session.add(coment)
        db.session.commit()
        success_message = 'Comentario creado existosamente'   
        flash(success_message)
    return render_template('coment.html', form = form, user = username)

@app.route("/reviews/", methods=[ 'GET' ])
@app.route("/reviews/<int:pagina>", methods=[ 'GET' ])
def reviews(pagina=1):
    usuario = session['username']
    #conecto las tablas Coment y User utilizando join, la cual es posible ya que en el modelo ya esta definida la relacion entre las 2 tablas mediante el id
    Coment_list = Coment.query.join(User).add_columns(User.username, Coment.text, Coment.created_date).paginate(pagina,4,False)
    return render_template('reviews.html', coments =  Coment_list, date_format = date_format, user = usuario)

@app.route('/logout')
def logout():  
    username_sesion = session['username']
    if 'username' in session:   #se chequea si username esta dentro del dicionario de session
        session.pop('username') #elimina la session  
        session.pop('user_id')
        print ('Salida del sistema por: '+username_sesion)
    return redirect(url_for("login"))

@app.route('/cookie')
def cookie():
    response = make_response(render_template('cookie.html')) #se asigna con la instruccion make_response el render_template
    response.set_cookie('custome_cookie','Andrea')           #se crea la cookie; se le asigna el nombre 'custome_cookie' y el valor de la misma 'Andrea'
    return response

@app.errorhandler(404)
def error_404(e):
    return render_template('error_404.html'), 404

@app.route("/hola")
def hello():
    custome_cookie = request.cookies.get('custome_cookie')
    print ('cookie:',custome_cookie)
    return render_template('hola.html')

if __name__ == '__main__':
    csrf.init_app(app) 
    db.init_app(app)
    with app.app_context():
     db.create_all()
    app.run()

    
    
    



    
