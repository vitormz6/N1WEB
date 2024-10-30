from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail, Message
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'

# Configurações do Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Por exemplo, usando Gmail
app.config['MAIL_PORT'] = 587  # Porta para TLS
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = "seuemail@email.com"
app.config['MAIL_PASSWORD'] = "suasenhagerada"
app.config['MAIL_DEFAULT_SENDER'] = ('N2 Programação WEB', app.config['MAIL_USERNAME'])

db = SQLAlchemy(app)
mail = Mail(app)

# Modelo para a tabela de usuários
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    real_name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default="ativo")
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.login}>'

# Inicialização do banco de dados
with app.app_context():
    db.create_all()

# Formulários
class UserForm(FlaskForm):
    login = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    real_name = StringField('Nome', validators=[DataRequired()])
    submit = SubmitField('Criar Usuário')

class EditUserForm(FlaskForm):
    login = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Nova Senha (deixe em branco para manter a mesma)')
    real_name = StringField('Nome', validators=[DataRequired()])
    submit = SubmitField('Editar Usuário')

class LoginForm(FlaskForm):
    login = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Login')

class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Enviar')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Nova Senha', validators=[DataRequired()])
    confirm_password = PasswordField('Confirme a Nova Senha', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Redefinir Senha')

# Funções para gerar e verificar tokens
def generate_reset_token(user):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(user.login, salt='password-reset-salt')

def verify_reset_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt='password-reset-salt',
            max_age=expiration
        )
    except Exception:
        return None
    return User.query.filter_by(login=email).first()

# Função para enviar email de redefinição de senha
def send_reset_email(user, token):
    reset_url = url_for('reset_password', token=token, _external=True)
    msg = Message('Redefinir Sua Senha',
                  sender=app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[user.login])
    msg.body = f'''Olá {user.real_name},

Para redefinir sua senha, visite o seguinte link:

{reset_url}

Se você não solicitou esta alteração, por favor ignore este email.

Atenciosamente,
Equipe de Programação WEB
'''
    mail.send(msg)

# Rotas do aplicativo
@app.route('/manage_users', methods=['GET', 'POST'])
def manage_users():
    form = UserForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(login=form.login.data).first()
        if existing_user:
            flash('Erro: Um usuário com este email já existe.', 'danger')
        else:
            try:
                hashed_password = generate_password_hash(form.password.data)
                new_user = User(
                    login=form.login.data,
                    password=hashed_password,
                    real_name=form.real_name.data,
                    status="ativo"
                )
                db.session.add(new_user)
                db.session.commit()
                flash('Usuário criado com sucesso!', 'success')
                return redirect(url_for('manage_users'))
            except Exception as e:
                flash(f'Erro ao criar usuário: {str(e)}', 'danger')

    users = User.query.all()
    return render_template('manage_users.html', form=form, users=users)

@app.route('/block_user/<int:id>')
def block_user(id):
    user = User.query.get(id)
    if user:
        user.status = 'bloqueado'
        db.session.commit()
        flash('Usuário bloqueado com sucesso', 'info')
    else:
        flash('Erro: Usuário não encontrado.', 'danger')
    return redirect(url_for('manage_users'))

@app.route('/unblock_user/<int:id>')
def unblock_user(id):
    user = User.query.get(id)
    if user:
        user.status = 'ativo'
        db.session.commit()
        flash('Usuário desbloqueado com sucesso', 'info')
    else:
        flash('Erro: Usuário não encontrado.', 'danger')
    return redirect(url_for('manage_users'))

@app.route('/edit_user/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    user = User.query.get_or_404(id)
    form = EditUserForm(login=user.login, real_name=user.real_name)

    if form.validate_on_submit():
        if form.login.data != user.login:
            existing_user = User.query.filter_by(login=form.login.data).first()
            if existing_user:
                flash('Erro: Email já em uso. Por favor, escolha outro.', 'danger')
                return redirect(url_for('edit_user', id=id))

        user.login = form.login.data
        user.real_name = form.real_name.data

        if form.password.data:
            user.password = generate_password_hash(form.password.data)

        try:
            user.updated_at = datetime.utcnow()
            db.session.commit()
            flash('Usuário editado com sucesso!', 'success')
            return redirect(url_for('manage_users'))
        except Exception as e:
            flash(f'Erro ao atualizar usuário: {str(e)}', 'danger')

    return render_template('edit_user.html', form=form, user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data).first()
        if user and user.status == "ativo" and check_password_hash(user.password, form.password.data):
            flash('Logado com sucesso!', 'success')
            return redirect(url_for('home'))
        elif user and user.status == "bloqueado":
            flash('Sua conta está bloqueada', 'danger')
        else:
            flash('Credenciais inválidas. Por favor, tente novamente.', 'danger')

    return render_template('login.html', form=form)

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.email.data).first()
        if user:
            token = generate_reset_token(user)
            send_reset_email(user, token)
            flash('Um email com instruções para redefinir sua senha foi enviado para o endereço informado.', 'info')
            return redirect(url_for('login'))
        else:
            flash('Email não encontrado no sistema.', 'danger')
    return render_template('forgot_password.html', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = verify_reset_token(token)
    if not user:
        flash('Token inválido ou expirado.', 'danger')
        return redirect(url_for('forgot_password'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user.password = hashed_password
        db.session.commit()
        flash('Sua senha foi atualizada!', 'success')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

@app.route('/')
def home():
    return render_template('base.html')

if __name__ == '__main__':
    app.run(debug=True)
