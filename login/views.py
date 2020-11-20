"""
Archivo donde se enlazan las acciones y eventos del código con las 
vistas en html.
"""

from django.shortcuts import render
import pyrebase

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
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()


# Documentar esto mejor -- Esta función retorna la vista de inicio de sesión
def signIn(request):
	return  render(request, "login/signIn.html")


# Esta función se encarga de captar el email y la contraseña y procede 
# a realizar  el inicio se sesión através de pyrebase y retorna la vista
# correspondiente

def postSign(request):
	users = db.get().val()
	if request.method == 'POST':
		if 'cedula_search' in request.POST.keys():
			cedula = request.POST.get('cedula_search')
			users = {cedula:db.child(cedula).get().val()}
			return render(request, "hc_manager/welcome.html", {'data':users})
		else:
			email = request.POST.get('email')
			try:
				user = auth.sign_in_with_email_and_password(email,request.POST.get('pass'))
				return render(request, "hc_manager/welcome.html", {'data':users, 'email':email.split('@')[0]})
			except NameError or HTTPError:
				print("Invalid username")
	print(users)
	return render(request, "hc_manager/welcome.html", {'data':users})
		