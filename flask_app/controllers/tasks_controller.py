from flask import render_template, redirect, session, request, flash
from flask_app import app

#Importación de modelos
from flask_app.models.users import User
from flask_app.models.tasks import Task

@app.route('/new/task')
def new_task():
    if 'user_id' not in session: #Comprobamos que inicia sesión
        return redirect('/')

    #Yo sé que en sesión tengo el id de mi usuario (session['user_id'])
    #Queremos una función que en base a ese id me regrese una instancia del usuario
    formulario = {"id": session['user_id']}

    user = User.get_by_id(formulario) #Recibo la instancia de usuario en base a su ID

    return render_template('new_task.html', user=user)
    
@app.route('/create/task', methods=['POST'])
def create_task():
    if 'user_id' not in session:
        return redirect('/')
    
    #Validación
    if not Task.valida_tarea(request.form):
        return redirect('/new/task')

    #Guardar
    Task.save(request.form)

    return redirect('/dashboard')

@app.route('/edit/task/<int:id>')
def edit_task(id):
    if 'user_id' not in session:
        return redirect('/')

    #Yo sé que en sesión tengo el id de mi usuario (session['user_id'])
    #Queremos una función que en base a ese id me regrese una instancia del usuario
    formulario = {"id": session['user_id']}

    user = User.get_by_id(formulario) #Recibo la instancia de usuario en base a su ID

    #Cuál se va a editar
    formulario_task = {"id": id}
    task = Task.get_by_id(formulario_task)

    return render_template('edit_task.html', user=user, task=task)

@app.route('/update/task', methods=['POST'])
def update_task():
    if 'user_id' not in session:
        return redirect('/')
    
    #Validación
    if not Task.valida_tarea(request.form):
        return redirect('/edit/task/'+request.form['id']) #/edit/task/1
    
    Task.update(request.form)

    return redirect('/dashboard')

@app.route('/delete/task/<int:id>')
def delete_task(id):
    if 'user_id' not in session:
        return redirect('/')

    formulario = {"id": id}
    Task.delete(formulario)

    return redirect('/dashboard')
