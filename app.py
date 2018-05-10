from flask import Flask, render_template, url_for
import os

app = Flask(__name__)
#port = os.environ['PORT']

@app.route('/')
def inicio():
	return render_template('index.html')

app.run('0.0.0.0', debug=True)