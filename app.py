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

@app.route('/busperfil',methods=["post","get"])
def busperfil(nombre=None, imagen=None, nombreusuario=None, steamid2=None, idioma=None):
	if request.method == "GET":
		return render_template('busperfil.html')
	else:
		nombre = request.form.get("nombre")
		payload={"key":"42F6A0CFD74A7E1A887BD94BEC654B62","vanityurl":nombre}
		r=requests.get("http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/",params=payload)
		if r.status_code==200:
			res=r.json()
			ide=res["response"]["steamid"]
			payload2={"key":"42F6A0CFD74A7E1A887BD94BEC654B62","steamids":ide}
			r2=requests.get("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/",params=payload2)
			if r.status_code==200:
				resultado=r2.json()
				try:
					nombre=resultado["response"]["players"][0]["realname"]
					idioma=resultado["response"]["players"][0]["loccountrycode"]
				except KeyError:
					nombre="Nombre no disponible"
					idioma="El idioma no esta disponible"

				imagen=resultado["response"]["players"][0]["avatarfull"]
				nombreusuario=resultado["response"]["players"][0]["personaname"]
				steamid2=resultado["response"]["players"][0]["steamid"]
				
				return render_template('perfil.html',nombre=nombre,imagen=imagen,nombreusuario=nombreusuario,steamid2=steamid2, idioma=idioma)


@app.route('/reportes')
def reportes():
	return render_template('formulario.html')

@app.route('/juegos')
def juegos():
	return render_template('pagina1.html')

app.run('0.0.0.0',int(port), debug=True)