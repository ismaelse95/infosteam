from flask import Flask, render_template, url_for, request,session
import requests
import os

app = Flask(__name__)
#app.secret_key="sdhaksjhdkasjdhsakjddksa" --> clave para una sesion nueva.
port = os.environ['PORT']
key = os.environ['key']
key2 = os.environ['KeyYoutube']

@app.route('/')
def inicio():
	return render_template('index.html')

@app.route('/contacta',methods=["post","get"])
def contacta():
	if request.method == "GET":
		return render_template('contacta.html')
	else:
		return render_template('contactafinal.html')


	return render_template('contacta.html')

@app.route('/busperfil',methods=["post","get"])
def busperfil(nombre=None, imagen=None, nombreusuario=None, steamid2=None, idioma=None):
	if request.method == "GET":
		return render_template('busperfil.html')
	else:
		nombre = request.form.get("nombre")
		payload={"key":key,"vanityurl":nombre}
		r=requests.get("http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/",params=payload)
		if r.status_code==200:
			res=r.json()
			try:
				ide=res["response"]["steamid"]
			#session["id"]=ide --> para iniciar una sesión.
				payload2={"key":key,"steamids":ide}
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
			except KeyError:
				ide="No existe el usuario."
			if ide == "No existe el usuario.":
				return render_template('falloperfil.html',ide=ide)
			else:
				return render_template('perfil.html',nombre=nombre,imagen=imagen,nombreusuario=nombreusuario,steamid2=steamid2, idioma=idioma)


@app.route('/todoslosjuegos',methods=["post","get"])
def todoslosjuegos(juegos=None):
	if request.method == "POST":
		return render_template('formulario.html')
	else:
		r=requests.get("http://api.steampowered.com/ISteamApps/GetAppList/v2")
		if r.status_code==200:
			res3=r.json()
			juegos_lista=[]
			for elem in res3["applist"]["apps"]:
				juegos_lista.append(elem["name"])
			return render_template("formulario.html", juegos_lista=juegos_lista)

@app.route('/juegos',methods=["post","get"])
def juegos():
	if request.method == "GET":
		return render_template('pagina1.html')
	else:
		indicador=False
		nombre2=request.form.get("nombre")
		r=requests.get("http://api.steampowered.com/ISteamApps/GetAppList/v2")
		if r.status_code==200:
			resultado=r.json()
			for elem in resultado["applist"]["apps"]:
				if elem["name"] == nombre2:
					ide=elem["appid"]
					indicador=True	
					return render_template('idjuego.html', ide=ide, nombre2=nombre2)
			if not indicador:
				return render_template('fallojuegos.html')

@app.route('/logros',methods=["post","get"])
def logros():
	if request.method == "GET":
		return render_template('logros.html')
	else:
		indicador=False
		nombre2=request.form.get("nombre")
		r=requests.get("http://api.steampowered.com/ISteamApps/GetAppList/v2")
		try:
			if r.status_code==200:
				resultado=r.json()
				for elem in resultado["applist"]["apps"]:
					if elem["name"] == nombre2:
						ide=elem["appid"]
						indicador=True
						payload={"key":key,"appid":ide}
						r=requests.get("http://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2",params=payload)
						if r.status_code==200:
							resultado=r.json()
							juegos_lista2=[]
							total=[]
							errores = 0
							for elem in resultado["game"]["availableGameStats"]["achievements"]:
								try:
									juegos_lista2.append(elem["description"])
									juegos_lista2.append(elem["icon"])
									total.append(juegos_lista2)
									juegos_lista2=[]
								except KeyError:
									errores+=1
							return render_template('logrosresultado.html',total=total)
				if not indicador:
					return render_template('fallologros.html')
			except KeyError:
				return render_template('fallologros.html')

@app.route('/juegosperfil/<idnuevo>',methods=["post","get"])
def juegosperfil(idnuevo):
	if request.method == "POST":
		#id=session["id"] --> Para usar el session
		return render_template('juegosperfil.html')
	else:
		ide=idnuevo
		payload={"key":key,"steamid":ide,"format":"json"}
		r=requests.get("http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001",params=payload)
		try:
			if r.status_code==200:
				resultado=r.json()
				juegos=[]
				for elem in resultado["response"]["games"]:
					juegos.append(elem["appid"])
					cuenta_juegos=len(juegos)
				r2=requests.get("http://api.steampowered.com/ISteamApps/GetAppList/v2")
				if r.status_code==200:
					res3=r2.json()
					juegos_lista=[]
					for elem in res3["applist"]["apps"]:
						for elem2 in juegos:
							if elem["appid"] == elem2:
								juegos_lista.append(elem["name"])
			return render_template('juegosperfil.html', cuenta_juegos=cuenta_juegos, juegos_lista=juegos_lista)
		except KeyError:
			return render_template('juegosperfilfallo.html')


@app.route('/amigos/<idnuevo>',methods=["post","get"])
def amigos(idnuevo):
	if request.method == "POST":
		return render_template('amigos.html')
	else:
		ide=idnuevo
		payload={"key":key,"steamid":ide,"relationship":"friend"}
		r=requests.get("http://api.steampowered.com/ISteamUser/GetFriendList/v0001",params=payload)
		if r.status_code==200:
			resultado=r.json()
			amigos=[]
			lista_amigos=[]
			for elem in resultado["friendslist"]["friends"]:
				amigos.append(elem["steamid"])
			for elem in amigos:
				ide2=elem
				payload2={"key":key,"steamids":ide2}
				r2=requests.get("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/",params=payload2)
				if r.status_code==200:
					resultado2=r2.json()
					nombreusuario=resultado2["response"]["players"][0]["personaname"]
					lista_amigos.append(nombreusuario)
			return render_template('amigos.html',lista_amigos=lista_amigos)

@app.route('/videos/<nombre2>',methods=["post","get"])
def videos(nombre2):
	if request.method == "POST":
		return render_template('videos.html')
	else:
		nombrejuego=nombre2
		payload={"part":"id,snippet","key": key2, "q":"", "maxResults":1, "type":"video"}
		payload["q"] = ("{0} trailer castellano").format(nombrejuego)
		r=requests.get('https://www.googleapis.com/youtube/v3/search', params=payload)
		if r.status_code==200:
			resultado=r.json()
			video2=""
			for elem in resultado["items"]:
				video2+="https://www.youtube.com/embed/{}".format(elem["id"]["videoId"])
		return render_template('videos.html',video2=video2)


app.run('0.0.0.0',int(port), debug=True)