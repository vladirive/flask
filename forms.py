from flask_wtf import FlaskForm
from wtforms import Form
from wtforms import StringField, TextField, TextAreaField, SubmitField, FieldList, FormField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms import HiddenField
from wtforms import validators 
from werkzeug.security import check_password_hash
from models import User


def validacion_length(form, field):
    if len(field.data) > 0:
        raise validators.ValidationError('el campo debe estar vacio')

class formulario_registro(Form):
    username = TextField('Nombre', [validators.length(min = 4, max=15, message='ingrese un nombre valido'), 
                  validators.Required(message='el nombre es requerido')
                ])
    email = EmailField('Email', [validators.Required(message='El email es requerido'), 
                 validators.Email(message='Ingrese un email valido')
                 ])
    password = PasswordField('Password', [validators.length(min = 4, max=15, message='ingrese un password valido'), 
                 validators.Required(message='el password es requerido')
                 ])

    def validate_username(form, field):#esto es override, ya que la funcion se crea automatica cuando se crean los campos
      username = field.data
      user = User.query.filter_by(username = username).first()
      if user:
        raise validators.ValidationError('Este username ya se encuentra registrado en la base de datos')

    def validate_email(form, field):#esto es override, ya que la funcion se crea automatica cuando se crean los campos
      email = field.data
      mail= User.query.filter_by(email = email).first()
      if mail:
        raise validators.ValidationError('Este email ya se encuentra registrado en la base de datos')
    
    def validate_password(form,field): #esto es override, ya que la funcion se crea automatica cuando se crean los campos
      pwd = form.password.data
      for usuario in User.query.all():
        if check_password_hash(usuario.password, pwd):
          print('mismo password de:', usuario.username)
          raise validators.ValidationError('El password pertenece a otro usuario') #al ejecutarse la sentencia raise, que se refiere a declarar una exepcion, el for deja de ejecutarse


class formulario_login(Form):
    username = TextField('Nombre', [validators.length(min = 4, max=15, message='ingrese un nombre valido'), 
                  validators.Required(message='el nombre es requerido')
                ])
    password = PasswordField('Password', [validators.length(min = 4, max=15, message='ingrese un password valido'), 
                 validators.Required(message='el password es requerido')
                 ])

class formulario_coment(Form):
    coment = TextAreaField('Comentario', [validators.length(min = 4, max=150, message='ingrese un coemntario valido'), 
                  validators.Required(message='el nombre es requerido')
                ])
