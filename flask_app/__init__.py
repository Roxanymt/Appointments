from flask import Flask

app = Flask(__name__) #inicializar app

app.secret_key = "Llave secreta"