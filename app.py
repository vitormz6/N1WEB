from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'
db = SQLAlchemy(app)

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

# Formulários para criação, edição e login de usuários
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

# Rota para gerenciamento de usuários
@app.route('/manage_users', methods=['GET', 'POST'])
def manage_users():
    form = UserForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(login=form.login.data).first()
        if existing_user:
            flash('Error: A user with this email already exists.', 'danger')
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
                flash('User created successfully!', 'success')
                return redirect(url_for('manage_users'))
            except Exception as e:
                flash(f'Error creating user: {str(e)}', 'danger')

    users = User.query.all()
    return render_template('manage_users.html', form=form, users=users)

# Rota para bloquear usuário (marcá-lo como "bloqueado")
@app.route('/block_user/<int:id>')
def block_user(id):
    user = User.query.get(id)
    if user:
        user.status = 'bloqueado'
        db.session.commit()
        flash('Bloqueado com sucesso', 'info')
    else:
        flash('Error: User not found.', 'danger')
    return redirect(url_for('manage_users'))

# Rota para desbloquear usuário
@app.route('/unblock_user/<int:id>')
def unblock_user(id):
    user = User.query.get(id)
    if user:
        user.status = 'ativo'
        db.session.commit()
        flash('Desbloqueado com sucesso', 'info')
    else:
        flash('Error: User not found.', 'danger')
    return redirect(url_for('manage_users'))

# Rota para editar usuário
@app.route('/edit_user/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    user = User.query.get_or_404(id)
    form = EditUserForm(login=user.login, real_name=user.real_name)

    if form.validate_on_submit():
        # Verifica se o e-mail foi alterado e se já existe outro usuário com o mesmo e-mail
        if form.login.data != user.login:
            existing_user = User.query.filter_by(login=form.login.data).first()
            if existing_user:
                flash('Error: Email already in use. Please choose a different one.', 'danger')
                return redirect(url_for('edit_user', id=id))

        # Atualiza os dados do usuário
        user.login = form.login.data
        user.real_name = form.real_name.data

        # Se a senha for fornecida, atualiza a senha
        if form.password.data:
            user.password = generate_password_hash(form.password.data)

        try:
            user.updated_at = datetime.utcnow()
            db.session.commit()
            flash('Usuário editado com sucesso!', 'success')
            return redirect(url_for('manage_users'))
        except Exception as e:
            flash(f'Error updating user: {str(e)}', 'danger')

    return render_template('edit_user.html', form=form, user=user)

# Rota para tela de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data).first()
        if user and user.status == "ativo" and check_password_hash(user.password, form.password.data):
            flash('Logged in successfully!', 'success')
            return render_template('base.html', message="Logged in successfully!")
        elif user and user.status == "bloqueado":
            flash('Sua conta está bloqueada', 'danger')
        else:
            flash('Invalid credentials. Please try again.', 'danger')

    return render_template('login.html', form=form)

# Rota da página inicial
@app.route('/')
def home():
    return render_template('base.html')

# Executa o servidor Flask
if __name__ == '__main__':
    app.run(debug=True)
