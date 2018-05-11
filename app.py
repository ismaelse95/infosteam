from flask import Flask, render_template, url_for
import os

app = Flask(__name__)
port = os.environ['PORT']

@app.route('/')
def inicio():
	return render_template('index.html')

@app.route('/contacta')
def contacta():
	return render_template('contacta.html')

@app.route('/busperfil')
def busperfil():
	return render_template('busperfil.html')

@app.route('/formulario')
def formulario():
	return render_template('formulario.html')

@app.route('/pagina1')
def pagina1():
	return render_template('pagina1.html')

app.run('0.0.0.0',int(port), debug=True)