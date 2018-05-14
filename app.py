from flask import Flask, render_template, url_for, request
import requests
import os

app = Flask(__name__)
port = os.environ['PORT']

@app.route('/')
def inicio():
	return render_template('index.html')

@app.route('/contacta')
def contacta():
	return render_template('contacta.html')

@app.route('/busperfil',methods=["POST","GET"])
def busperfil():
	if request.method == "get":
		return render_template('busperfil.html')
	else:
		nombre=requet.forms.get("nombre")
		return nombre
	#return render_template('busperfil.html')


@app.route('/reportes')
def reportes():
	return render_template('formulario.html')

@app.route('/juegos')
def juegos():
	return render_template('pagina1.html')

app.run('0.0.0.0',int(port), debug=True)