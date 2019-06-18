from flask import Flask, render_template, session, g, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from urllib.parse import urlparse, urljoin
from Token import gerarToken
import os
import Views





app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cc.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['USE_SESSION_FOR_NEXT'] = True
Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
alterando_senha = False





class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    senha = db.Column(db.String(60))
    token = db.Column(db.String(20))





class Curso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(50), unique=True)
    descricao = db.Column(db.String(150))
    vendas = db.Column(db.Integer)
    preco = db.Column(db.Numeric(5,2))
    url = db.Column(db.String(250), unique=True)





@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))





#Rota de index/home

@app.route('/')
def index():
    cursos = Curso.query.order_by(Curso.vendas.desc())
    titulo = [c.titulo for c in cursos]
    preco = [c.preco for c in cursos]
    id = [c.id for c in cursos]
    descricao = [c.descricao for c in cursos]
    vendas = [c.vendas for c in cursos]
    if not current_user.is_authenticated:
        return render_template('index.html' , u = False, titulo=titulo, preco=preco, id=id, descricao=descricao, vendas=vendas)
    else:
        return render_template('index.html' , u = True, ue = current_user.email, titulo=titulo, preco=preco, id=id, descricao=descricao, vendas=vendas)





#Rota de login

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    else:
        form = Views.LoginForm()
        session['next'] = request.args.get('next')
        cred_inc = False
        if form.validate_on_submit():
            usuario = Usuario.query.filter_by(email=form.email.data).first()
            if usuario:
                if check_password_hash(usuario.senha, form.senha.data):
                    login_user(usuario, remember=True)
                    return redirect(url_for('meus_cursos'))
                else:
                    cred_inc = True #Senha incorreta
            else:
                cred_inc = True #Email não cadastrado
        return render_template('login.html', form=form, cred_inc=cred_inc)





#Rota de cadastro de usuário

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    else:
        form = Views.CadastroForm()
        senha_dif = False
        email_usa = False
        token = gerarToken()
        usuario_cad = False
        if form.validate_on_submit():
            if form.senha.data == form.rsenha.data:
                usuario = Usuario.query.filter_by(email=form.email.data).first()
                if not usuario:
                    hashed_senha = generate_password_hash(form.senha.data, method='sha256')
                    hashed_token = generate_password_hash(token, method='sha256')
                    novo_usuario = Usuario(email=form.email.data, senha=hashed_senha, token=hashed_token)
                    db.session.add(novo_usuario)
                    db.session.commit()
                    usuario_cad = True
                    return redirect(url_for('index', usuario_cad=usuario_cad, token=token))
                else:
                    email_usa = True #Email já utilizado
            else:
                senha_dif = True #Senhas não coincidem
        return render_template('cadastro.html', form=form, email_usa=email_usa, senha_dif=senha_dif)





#Rota de recuperação de senha

@app.route('/recuperar_senha', methods=['GET', 'POST'])
def recuperar_senha():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    else:
        form = Views.RecuperarSenhaForm()
        cred_inc = False
        senha_dif = False
        if form.validate_on_submit():
            usuario = Usuario.query.filter_by(email=form.email.data).first()
            if usuario:
                if check_password_hash(usuario.token, form.token.data):
                    if form.senha.data == form.rsenha.data:
                        hashed_senha = generate_password_hash(form.senha.data, method='sha256')
                        usuario.senha = hashed_senha
                        db.session.commit()
                        return redirect(url_for('index', alterou_senha=True))
                    else:
                        senha_dif=True
                else:
                    cred_inc = True
            else:
                cred_inc = True
        return render_template('recuperar_senha.html', form=form, cred_inc=cred_inc, senha_dif=senha_dif)





#Rota de curso disponível para compra

@app.route('/curso/<idcurso>')
@login_required
def curso(idcurso):
    url = Curso.query.filter_by(id=idcurso)
    url = [u.url for u in url]
    return render_template('curso.html', u = True, ue = current_user.email, url=url)





#Rota de cursos comprados pelo usuário

@app.route('/meus_cursos')
@login_required
def meus_cursos():
        return render_template('meus_cursos.html', u = True, ue = current_user.email)





#Rota de logout

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))





if __name__ == '__main__':
    app.run(debug=True)
