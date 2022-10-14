from flask_app.config.mysqlconnection import connectToMySQL #Importación de la conexión con bd
from flask import flash #flash es el encargado de mandar mensajes/errores

from datetime import datetime  #Manipular fechas

class Task:

    def __init__(self, data):
        self.id = data['id']
        self.task = data['task']
        self.date = data['date']
        self.status = data['status']
        self.created_at = data['created_at']
        self.updated_at = data ['updated_at']
        self.user_id = data['user_id']

    @staticmethod
    def valida_tarea(formulario):
        es_valido = True

        if formulario['task'] == '':
            flash('Tarea no puede estar vacío', 'tasks')
            es_valido = False
        
        if formulario['status'] == '':
            flash('Debe ingresar un estado', 'tasks')
            es_valido = False
        
        if formulario['date'] == '':
            flash('Ingrese una fecha', 'tasks')
            es_valido = False
        else:
            fecha_obj = datetime.strptime(formulario['date'], '%Y-%m-%d') #Estamos transformando un texto a formato de fecha
            hoy = datetime.now() #Me da la fecha de hoy
            if hoy > fecha_obj:
                flash('La fecha no puede ser menor a hoy', 'tasks')
                es_valido = False
        
        return es_valido

    @classmethod
    def save(cls, formulario):
        query = "INSERT INTO tasks (task, date, status, user_id) VALUES (%(task)s, %(date)s, %(status)s, %(user_id)s)"
        result = connectToMySQL('appointments').query_db(query, formulario)
        return result
    

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM tasks"
        results = connectToMySQL('appointments').query_db(query) #Lista de Diccionarios
        tasks = []

        for task in results:
            tasks.append(cls(task))
        
        return tasks

    @classmethod
    def get_by_id(cls, formulario):
        query = "SELECT * FROM tasks WHERE id = %(id)s"
        result = connectToMySQL('appointments').query_db(query, formulario)
        task = cls(result[0])
        return task
    
    @classmethod
    def update(cls, formulario):
        query = "UPDATE tasks SET task=%(task)s, status=%(status)s, date=%(date)s, user_id=%(user_id)s WHERE id=%(id)s"
        result = connectToMySQL('appointments').query_db(query, formulario)
        return result
    

    @classmethod
    def delete(cls, formulario):
        query = "DELETE FROM tasks WHERE id = %(id)s"
        result = connectToMySQL('appointments').query_db(query, formulario)
        return result
