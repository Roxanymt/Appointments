from flask import render_template, redirect, request, session, flash
from flask_app import app

#importacion modelo
from flask_app.models.users import User
from flask_app.models.tasks import Task

#importacion de BCrypt
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.valida_usuario(request.form):
        return redirect('/')

    pwd = bcrypt.generate_password_hash(request.form['password']) #encriptando contraseña del usuario y guardandola en variable (pwd = password encriptado)
    
    formulario = {
    "first_name": request.form['first_name'],
    "last_name": request.form['last_name'],
    "email": request.form['email'],
    "password": pwd
    }

    id = User.save(formulario) #Recibir el identificador del nuevo usuario

    session['user_id'] = id #Guardamos en sesión el identificador del usuario

    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    #verificar que e-mail existe en la base de datos
    user = User.get_by_email(request.form) #se recibe instancia de usuario o False

    if not user: #si user = False
        flash('E-mail no encontrado', 'login')
        return redirect('/')

    if not bcrypt.check_password_hash(user.password, request.form ['password']):
        flash('Contraseña incorrecta', 'login')
        return redirect('/')

    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')

    formulario = {"id": session['user_id']}
    user = User.get_by_id(formulario) #recibo instancia de usuario en base a su id

    
    tasks = Task.get_all()

    return render_template('dashboard.html', user=user, tasks=tasks)


@app.route('/logout')
def logout():
    session.clear() #elimina los datos de la sesión
    return redirect('/')