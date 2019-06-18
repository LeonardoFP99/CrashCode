
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length


class LoginForm(FlaskForm):
    email = StringField(label='', validators=[InputRequired()], render_kw={"placeholder": "E-mail"})
    senha = PasswordField(label='', validators=[InputRequired()], render_kw={"placeholder": "Senha"})


class CadastroForm(FlaskForm):
    email = StringField(label='', validators=[InputRequired()], render_kw={"placeholder": "E-mail"})
    senha = PasswordField(label='', validators=[InputRequired()], render_kw={"placeholder": "Senha"})
    rsenha = PasswordField(label='', validators=[InputRequired()], render_kw={"placeholder": "Repita a senha"})

class RecuperarSenhaForm(FlaskForm):
    email = StringField(label='', validators=[InputRequired()], render_kw={"placeholder": "E-mail"})
    token = PasswordField(label='', validators=[InputRequired()], render_kw={"placeholder": "Token de segurança"})
    senha = PasswordField(label='', validators=[InputRequired()], render_kw={"placeholder": "Nova senha"})
    rsenha = PasswordField(label='', validators=[InputRequired()], render_kw={"placeholder": "Repita a senha"})
