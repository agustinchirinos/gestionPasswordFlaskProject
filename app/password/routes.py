from flask import render_template, request, redirect, url_for

import app
from . import password
from .models import Usuario
from .forms import UsuarioForm, LoginForm
from .auxiliar import encriptar_password, desencriptar_password
from .. import db

PEEPER = "ClaveSecretaPeeper"


@password.route('/')
def index():  # put application's code here
    return render_template('index.html')

@password.route("/welcome/")
def welcome():
    return render_template("welcome.html")

@password.route("/loginenclaro/", methods=["GET","POST"])
def loginenclaro():
    error = ""
    form = LoginForm(request.form)
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        usuario = Usuario.get_by_username(username)
        if usuario and usuario.password == password:
            return redirect(url_for("password.welcome"))
        else:
            error = "Usuario y/o contraseña incorrecta"
    return render_template("loginenclaro.html", form=form, error=error)

@password.route("/enclaro/", methods=["GET","POST"])
def enclaro():
    error = ""
    form = UsuarioForm(request.form)
    if form.validate_on_submit():
        try:
            usuario = Usuario()
            usuario.username = form.username.data
            usuario.password = form.password.data
            usuario.nombre = form.nombre.data
            usuario.apellidos = form.apellidos.data
            usuario.dni = form.dni.data
            usuario.create()
            return redirect(url_for('password.loginenclaro'))
        except Exception as e:
            error = "No se ha podido dar de alta "+ e.__str__()
    return render_template("enclaro.html", form=form, error=error)


@password.route("/logincifrado/", methods=["GET","POST"])
def logincifrado():
    error = ""
    form = LoginForm(request.form)
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        usuario = Usuario.get_by_username(username)
        if usuario and \
                str(desencriptar_password(usuario.passwordcifrada)).replace("b'","").replace("'","") == password:
            return redirect(url_for("password.welcome"))
        else:
            error = "Usuario y/o contraseña incorrecta"
    return render_template("logincifrado.html", form=form, error=error)

@password.route("/cifrado/", methods=["GET","POST"])
def cifrado():
    error = ""
    form = UsuarioForm(request.form)
    if form.validate_on_submit():
        try:
            usuario = Usuario()
            usuario.username = form.username.data
            usuario.passwordcifrada = encriptar_password(form.password.data)
            usuario.nombre = form.nombre.data
            usuario.apellidos = form.apellidos.data
            usuario.dni = form.dni.data
            usuario.create()
            return redirect(url_for('password.logincifrado'))
        except Exception as e:
            error = "No se ha podido dar de alta "+ e.__str__()
    return render_template("cifrado.html", form=form, error=error)



@password.route("/hasheada/", methods=["GET","POST"])
def hasheada():
    error = ""
    form = UsuarioForm(request.form)
    if form.validate_on_submit():
        try:
            usuario = Usuario()
            usuario.username = form.username.data
            usuario.set_password(form.password.data)
            usuario.nombre = form.nombre.data
            usuario.apellidos = form.apellidos.data
            usuario.dni = form.dni.data
            usuario.create()
            return redirect(url_for('password.loginhasheado'))
        except Exception as e:
            error = "No se ha podido dar de alta " + e.__str__()
    return render_template("hasheada.html", form=form, error=error)

@password.route("/loginhasheado/", methods=["GET","POST"])
def loginhasheado():
    error = ""
    form = LoginForm(request.form)
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        usuario = Usuario.get_by_username(username)
        if usuario and usuario.check_password(password):
            return redirect(url_for("password.welcome"))
        else:
            error = "Usuario y/o contraseña incorrecta"
    return render_template("loginhasheado.html", form=form, error=error)


@password.route("/hasheadapeeper/", methods=["GET","POST"])
def hasheadapeeper():
    error = ""
    form = UsuarioForm(request.form)
    return render_template("hasheadapeeper.html", form=form, error=error)

@password.route("/loginhasheadopeeper/", methods=["GET","POST"])
def loginhasheadopeeper():
    error = ""
    form = LoginForm(request.form)
    return render_template("loginhasheadopeeper.html", form=form, error=error)
