from flask import Flask, render_template, url_for
import os

app = Flask(__name__)
port = os.environ['PORT']

