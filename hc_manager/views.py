"""
Archivo donde se enlazan las acciones y eventos del código con las 
vistas en html.
"""

from django.shortcuts import render
from datetime import datetime
import pyrebase
import json

# Configuración del wrap pyrebase
config = {
	    'apiKey': "AIzaSyBeSa2PSyHEtt9jPRYZXjRP4myOvGBXoGc",
	    'authDomain': "hc-manager-e2356.firebaseapp.com",
	    'databaseURL': "https://hc-manager-e2356.firebaseio.com",
	    'projectId': "hc-manager-e2356",
	    'storageBucket': "hc-manager-e2356.appspot.com",
	    'messagingSenderId': "869491009077",
	    'appId': "1:869491009077:web:35468c3d8127791a55337c",
	    'measurementId': "G-C33NC6SJCB"
}

# Inicialización de servicios de la base de datos
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()


# Rutina para añadir un nuevo documento a la base de datos
def newHC(request):
	if request.method == 'POST':
		inputs = ['nombre','edad','direccion','sexo','cedula','ips','creacion','modificacion','citas','cambios']
		cambios = ['' for _ in range(len(inputs))]
		today = datetime.today().strftime('%d-%m-%Y-%H:%M:%S')
		cedula = request.POST.get('cedula')
		for i in range(5):
			val = request.POST.get(inputs[i])
			db.child(cedula).child(inputs[i]).set(val)
			cambios[i] = (inputs[i],val)
		if request.POST.get('ips') != '':
			ips_list = request.POST.get('ips').split(',')
		else:
			ips_list = []
		db.child(cedula).child('ips').set(ips_list)
		cambios[5] = ('ips',ips_list)
		db.child(cedula).child('creacion').set(today)		# Fecha de creación
		cambios[6] = ('creacion',today)
		db.child(cedula).child('modificacion').set(today)	# Fecha de modificación
		cambios[7] = ('modificacion',today)
		db.child(cedula).child('citas').set({})					# Diccionario de citas
		cambios[8] = ('citas',{})
		db.child(cedula).child('cambios').child(today).set({'fecha':today,'valores':cambios})
		return render(request, "hc_manager/welcome.html", {'data': db.get().val()})
	return render(request, "hc_manager/creation.html")


def editHC(request, cedula):
	if request.method == 'GET':
		users = {cedula:db.child(cedula).get().val()}
		return render(request, "hc_manager/edition.html", {'data':users, 'cedula':cedula})
	elif request.method == 'POST':
		inputs = ['nombre','edad','direccion','sexo','cedula','ips','creacion','modificacion','citas','cambios']
		cambios = []
		today = datetime.today().strftime('%d-%m-%Y-%H:%M:%S')
		for i in range(5):
			dictn = {}
			val = request.POST.get(inputs[i])
			if val != '':
				dictn = {inputs[i]:val}
				db.child(cedula).update(dictn)
				cambios.append((inputs[i],val))
		if request.POST.get('ips') != '':
			ips_list = request.POST.get('ips').split(',')
			db.child(cedula).child('ips').set(ips_list)
			cambios.append(('ips',ips_list))
		else:
			ips_list = []
		if request.POST.get('modificacion') != '':
			db.child(cedula).child('modificacion').set(today)	# Fecha de modificación
			cambios.append(('modificacion',today))
		if request.POST.get('cambios') != '':
			db.child(cedula).child('cambios').child(today).set({'fecha':today,'valores':cambios})

		users = {cedula:db.child(cedula).get().val()}

		return render(request, "hc_manager/edition.html", {'data':users, 'cedula':cedula})

def logHC(request, cedula):
	if request.method == 'GET':
		dicts = db.child(cedula).child('cambios').get().val()
		cambios = json.dumps(dicts, indent=4, sort_keys=True)
		print(cambios)
		return render(request, "hc_manager/cambios.html", {'data':cambios, 'cedula':cedula})

def newCita(request, cedula):
	if request.method == 'POST':
		inputs = ['peso','estatura','actividad','dieta','enfermedades','valoracion','motivo','comentario']
		today = datetime.today().strftime('%d-%m-%Y-%H:%M:%S')
		dictn = {}
		for i in range(len(inputs)):
			val = request.POST.get(inputs[i])
			dictn[inputs[i]] = val
		db.child(cedula).child('citas').child(today).set(dictn)
		users = {cedula:db.child(cedula).get().val()}
		return render(request, "hc_manager/edition.html", {'data':users, 'cedula':cedula})
	return render(request, "hc_manager/newcita.html", {'cedula':cedula})

def adminHC(request):
	users = db.get().val()
	if request.method == 'POST':
		if 'cedula_search' in request.POST.keys():
			cedula = request.POST.get('cedula_search')
			users = {cedula:db.child(cedula).get().val()}
			#return render(request, "hc_manager/welcomeAdmin.html", {'data':users})
			#print(users)
		else:
			email = request.POST.get('email')
			try:
				user = auth.sign_in_with_email_and_password(email,request.POST.get('pass'))
				print(email)
				if email == 'admin@jmail.com':
					return render(request, "hc_manager/welcomeAdmin.html", {'data':users, 'email':email.split('@')[0]})
			except NameError or HTTPError:
				print("Invalid username")
	return render(request, "hc_manager/welcomeAdmin.html", {'data':users})

def admin(request):
	return render(request, "login/adminSign.html")

def adminUser(request):
	users = db.get().val()
	if request.method == 'POST':
		email = request.POST.get('email')
		auth.create_user_with_email_and_password(email, request.POST.get('pass'))
		return render(request, "hc_manager/welcomeAdmin.html", {'data':users})
	return render(request, "hc_manager/newUser.html")

def adminCreate(request):
	if request.method == 'POST':
		inputs = ['nombre','edad','direccion','sexo','cedula','ips','creacion','modificacion','citas','cambios']
		cambios = ['' for _ in range(len(inputs))]
		today = datetime.today().strftime('%d-%m-%Y-%H:%M:%S')
		cedula = request.POST.get('cedula')
		for i in range(5):
			val = request.POST.get(inputs[i])
			db.child(cedula).child(inputs[i]).set(val)
			cambios[i] = (inputs[i],val)
		if request.POST.get('ips') != '':
			ips_list = request.POST.get('ips').split(',')
		else:
			ips_list = []
		db.child(cedula).child('ips').set(ips_list)
		cambios[5] = ('ips',ips_list)
		db.child(cedula).child('creacion').set(today)		# Fecha de creación
		cambios[6] = ('creacion',today)
		db.child(cedula).child('modificacion').set(today)	# Fecha de modificación
		cambios[7] = ('modificacion',today)
		db.child(cedula).child('citas').set({})					# Diccionario de citas
		cambios[8] = ('citas',{})
		db.child(cedula).child('cambios').child(today).set({'fecha':today,'valores':cambios})
		return render(request, "hc_manager/welcomeAdmin.html", {'data': db.get().val()})
	return render(request, "hc_manager/adminCreate.html")

def adminEdit(request,cedula):
	if request.method == 'GET':
		users = {cedula:db.child(cedula).get().val()}
		return render(request, "hc_manager/adminEdit.html", {'data':users, 'cedula':cedula})
	elif request.method == 'POST':
		inputs = ['nombre','edad','direccion','sexo','cedula','ips','creacion','modificacion','citas','cambios']
		cambios = []
		today = datetime.today().strftime('%d-%m-%Y-%H:%M:%S')
		for i in range(5):
			dictn = {}
			val = request.POST.get(inputs[i])
			if val != '':
				dictn = {inputs[i]:val}
				db.child(cedula).update(dictn)
				cambios.append((inputs[i],val))
		if request.POST.get('ips') != '':
			ips_list = request.POST.get('ips').split(',')
			db.child(cedula).child('ips').set(ips_list)
			cambios.append(('ips',ips_list))
		else:
			ips_list = []
		if request.POST.get('modificacion') != '':
			db.child(cedula).child('modificacion').set(today)	# Fecha de modificación
			cambios.append(('modificacion',today))
		if request.POST.get('cambios') != '':
			db.child(cedula).child('cambios').child(today).set({'fecha':today,'valores':cambios})

		users = {cedula:db.child(cedula).get().val()}

		return render(request, "hc_manager/adminEdit.html", {'data':users, 'cedula':cedula})

def adminLog(request, cedula):
	if request.method == 'GET':
		dicts = db.child(cedula).child('cambios').get().val()
		cambios = json.dumps(dicts, indent=4, sort_keys=True)
		print(cambios)
		return render(request, "hc_manager/adminCambios.html", {'data':cambios, 'cedula':cedula})

def adminCita(request, cedula):
	if request.method == 'POST':
		inputs = ['peso','estatura','actividad','dieta','enfermedades','valoracion','motivo','comentario']
		today = datetime.today().strftime('%d-%m-%Y-%H:%M:%S')
		dictn = {}
		for i in range(len(inputs)):
			val = request.POST.get(inputs[i])
			dictn[inputs[i]] = val
		db.child(cedula).child('citas').child(today).set(dictn)
		users = {cedula:db.child(cedula).get().val()}
		return render(request, "hc_manager/adminEdit.html", {'data':users, 'cedula':cedula})
	return render(request, "hc_manager/adminCita.html", {'cedula':cedula})

def adminDelHC(request, cedula):
	users = db.get().val()
	db.child(cedula).remove()
	return render(request, "hc_manager/welcomeAdmin.html", {'data':users})

def help(request):
	return render(request, "hc_manager/help.html")
