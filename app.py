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

app.run('0.0.0.0',int(port), debug=True)