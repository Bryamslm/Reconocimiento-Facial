from tkinter import *
import tkinter as tk
from PIL import ImageTk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image
from tkinter import filedialog
import sys
import requests
import json
import cognitive_face as CF
from PIL import Image, ImageDraw, ImageFont
import pickle
import io
from io import BytesIO
subscription_key = None
SUBSCRIPTION_KEY = 'd691bbd350ab47948e784cb8df0e72d8'
BASE_URL = 'https://misclases.cognitiveservices.azure.com/face/v1.0/'
CF.BaseUrl.set(BASE_URL)
CF.Key.set(SUBSCRIPTION_KEY)

"""
Students:
Rose Yesenia Campos Carvajal
Bryam Steven López Miranda

"""
class Persona():
	"""Create a person with basic information"""
	def __init__(self, identificacion, personId,
		nombre, edad, genero, image_path):
		"""Create a person.
		Arguments:
		identificacion: identification of the person to create
		personId: identification that Microsoft Azure gives to each person
		nombre: person name
		edad: age of the person
		genero: gender of person
		image_path: path of the person's image

		"""
		self.identificacion=identificacion
		self.personId= personId
		self.nombre=nombre
		self.edad=edad
		self.genero=genero
		self.image_path=image_path

class Familia(Persona):
	"""Create a person with characteristics of a relative"""
	def __init__(self, identificacion, personId,
		nombre, edad, genero, image_path, arg_1, arg_2):
		"""Create a family member, inherits from the Persona class.
		Arguments:
		identificacion: identification of the person to create
		personId: identification that Microsoft Azure gives to each person
		nombre: person name
		edad: age of the person
		genero: gender of person
		image_path: path of the person's image
		arg_1: relationship with the relative, for example: uncle
		arg_2: Where the relative lives

		"""
		super().__init__(identificacion, personId,
		nombre, edad, genero, image_path)
		self.cercania=arg_1
		self.residencia=arg_2


class Amigos(Persona):
	"""Create a person with characteristics of a friend"""
	def __init__(self, identificacion, personId,
		nombre, edad, genero, image_path, arg_1, arg_2):
		"""Create a friend, inherits from the Persona class.
		Arguments:
		identificacion: identification of the person to create
		personId: identification that Microsoft Azure gives to each person
		nombre: person name
		edad: age of the person
		genero: gender of person
		image_path: path of the person's image
		arg_1: Friendship time
		arg_2: The friends they have in common

		"""
		super().__init__(identificacion, personId,
		nombre, edad, genero, image_path)
		self.tiempo_amistad=arg_1
		self.amigos_comun=arg_2

class Famosos(Persona):
	"""Create a person with characteristics of a famous"""
	def __init__(self, identificacion, personId,
		nombre, edad, genero, image_path, arg_1, arg_2):
		"""Create a famous, inherits from the Persona class.
		Arguments:
		identificacion: identification of the person to create
		personId: identification that Microsoft Azure gives to each person
		nombre: person name
		edad: age of the person
		genero: gender of person
		image_path: path of the person's image
		arg_1: what does the famous
		arg_2: know if it is the famous favorite

		"""
		super().__init__(identificacion, personId,
		nombre, edad, genero, image_path)
		self.actividad=arg_1
		self.favorito=arg_2

def crea_persona(identificacion, nombre, image_path, arg_1, arg_2, grupo, na, nc, nd, ng):
	"""Create a new person.
	Arguments: Nothing
	Return: Nothing

	"""
	# The group the new person belongs to
	# The function ingresa_informacion is called to determine the information of the new person
	# The information depends on the group where the person belongs
	# The emotion function is called to determine the age and
	# gender of the new person from the entered image.
	global guarda_direcc
	guarda_direcc=''
	image_path=str(image_path.name)
	edad, genero= emotion(image_path, True)
	# The create_person function is called to add the new person
	# in Microsoft Azure and also get their personId
	personId=create_person(str(nombre), str(image_path), int(grupo))
	# The new person is created according to the group to which it belongs
	if int(grupo)==100:
		# a family member is created
		persona=Familia(identificacion, personId, nombre, edad, genero, image_path, arg_1, arg_2)
		# Personas_en_archivo function is called to add object to binaio file
		Personas_en_archivo(persona)
		tk.messagebox.showinfo('éxito', 'Se agregó persona al grupo de Familia exitosamente')	
	elif int(grupo)==200:
		# a friend member is created
		persona=Amigos(identificacion, personId, nombre, edad, genero, image_path, arg_1, arg_2)
		# Personas_en_archivo function is called to add object to binaio file
		Personas_en_archivo(persona)
		tk.messagebox.showinfo('éxito', 'Se agregó persona al grupo de Amigos exitosamente')
	elif int(grupo)==300:
		# a famous member is created
		persona=Famosos(identificacion, personId, nombre, edad, genero, image_path, arg_1, arg_2)
		# Personas_en_archivo function is called to add object to binaio file
		Personas_en_archivo(persona)
		tk.messagebox.showinfo('éxito', 'Se agregó persona al grupo de Famosos exitosamente')
	else:
		# A person with only basic characteristics is created.
		persona=Persona(identificacion, personId, nombre, edad, genero, image_path)
		# Personas_en_archivo function is called to add object to binaio file
		Personas_en_archivo(persona)
		tk.messagebox.showinfo('éxito', 'Se agregó persona al grupo exitosamente')

def create_person(name, picture, group_id):
    #Create a person
    #name = "Abel Mendez"
    #user_data = 'I am professor in the ITCR'
    response = CF.person.create(group_id, name)
    #print(response)
    #En response viene el person_id de la persona que se ha creado
    # Get person_id from response
    person_id = response['personId']
    #print(person_id)
    #Sumarle una foto a la persona que se ha creado
    CF.person.add_face(picture, group_id, person_id)
    #print CF.person.lists(PERSON_GROUP_ID)
    
    #Re-entrenar el modelo porque se le agrego una foto a una persona
    CF.person_group.train(group_id)
    #Obtener el status del grupo
    response = CF.person_group.get_status(group_id)
    status = response['status']
    return person_id

def Personas_en_archivo(persona):
	"""Saves people objects in binary file.
	Arguments:
	persona: Object that contains all the information of a person
	"""

	# All person objects will be saved
	personas=list() 
	try:
		# The binary file opens in the way of adding binary information
		archivo_binario=open("archivo_rostros", "ab+")
		# Position the cursor at the beginning to move through the list
		archivo_binario.seek(0)
		#The objects are loaded into the people list
		personas=pickle.load(archivo_binario)
		# The persona object is added to the personas list
		personas.append(persona)
	except:
		# The personaobject is added to the personas list
		personas.append(persona)
		print('\nPrimera persona en el archivo...\n')
	finally:
		# The binary file opens in writing information mode
		archivo_binario=open("archivo_rostros", "wb")
		# What is in the personas list is loaded to the binary file
		pickle.dump(personas, archivo_binario)
		# Closes the binary file and removes the binary file from the program
		archivo_binario.close()
		del archivo_binario

def emotion(image_path, booleano):
	""" Returns the age and gender of a person or all their data
	of the person present in the image.
	Arguments:
	image_path: Direction of a person's image
	booleano: True or False, depending on the action you want to perform
	Return:
	ege and gender if booleano is True
	analisys if booleano is False
	"""
	image_data = open(image_path, "rb").read()
	headers = {'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY,
	'Content-Type': 'application/octet-stream'}
	params = {
    	'returnFaceId': 'true',
    	'returnFaceLandmarks': 'false',
    	'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
    }
	response = requests.post(
							BASE_URL + "detect/", headers=headers, params=params, data=image_data)
	analysis = response.json()
	# If Boolean is True, only age and gender are taken to return them
	if booleano:
		face=analysis[0]
		faceAttributes=face['faceAttributes']
		edad= faceAttributes['age']
		genero= faceAttributes['gender']
		return edad, genero
	# If Boolean is False, analysis of the person is returned
	else:
		return analysis

def leer_archivo(person_id):
	"""Read information from a binary file.
	Argumnets:
	person_id: Microsoft Azure identifier of the person object being searched for
	Return:
	Object with identified person
	"""
	# The binary file opens in read mode
	archivo_binario= open("archivo_rostros", "rb")
	archivo_binario.seek(0)
	#File information is loaded into a list
	lista=pickle.load(archivo_binario)
	archivo_binario.close()
	del archivo_binario
	for persona in lista:
		# The reference identifier and the object identifier 
		# are compared to find out if it is the person being searched
		if persona.personId==person_id:
			return persona

def mostrar_info(grupo, persona):
	"""Displays information for a person.
	Arguments:
	grupo: Group to which the person belongs
	persona: Object with the information to show
	Return:
	Nothing

	"""
	# Depending on the group to which the person belongs,
	# it will show their respective information
	if int(grupo)== 100:
		print('Cercania:', persona.cercania)
		print('Residencia:', persona.residencia)
		return persona.identificacion,  persona.personId, persona.nombre, persona.edad, persona.genero, persona.cercania, persona.residencia
	elif int(grupo)== 200:
		return persona.identificacion,  persona.personId, persona.nombre, persona.edad, persona.genero, persona.tiempo_amistad, persona.amigos_comun
	elif int(grupo)== 300:
		return persona.identificacion,  persona.personId, persona.nombre, persona.edad, persona.genero, persona.actividad, persona.favorito

def mostrar_informacion(grupo, tipo_print):
	"""
	Displays the information of all the people in
	a group descending by age and ascending by name
	Return:
	Nothing

	"""
	grupo=int(grupo)
	# A list with the personId is obtained to look for them in binary file
	try:
		personas=CF.person.lists(grupo)
	except:
		pass

	accion=int(tipo_print)
	if accion==1:
		lista=ordenar_nombre(grupo, personas, accion)
		return lista
	elif accion==2:
		lista=ordenar_edad(grupo, personas, accion)
		return lista
	elif accion==3:
		lista=ordenar_nombre(grupo, personas, accion)
		return lista
	elif accion==4:
		lista=ordenar_edad(grupo, personas, accion)
		return lista
	else:
		tk.messagebox.showinfo('Invalido', 'No se indicó un tipo de impresion válido')
		main.generar_ventana6()

def ordenar_edad(grupo, personas, accion):
	objetos=list()
	# It goes through the lists with the personId
	for persona in personas:
		# A personId is extracted from the list
		personId=persona['personId']
		# The read_file function is called to find the object associated with the personId
		objeto=leer_archivo(personId)
		if objeto != None:
			# The object is added to an object list
			objetos.append(objeto)
	objetos_orden_edad=list()

	# Descending objects are sorted by age using insert
	while len(objetos) != 0:
		edad_mayor= 0
		temporal=object()
		for ob in objetos:
			# The object with the highest age is identified
			if ob.edad > edad_mayor:
				edad_mayor=ob.edad     #cycle saved by the oldest person.
				temporal=ob
		# The object is put in a new list in an orderly way
		if accion==4:
			objetos_orden_edad.append(temporal)
		else:
			objetos_orden_edad.insert(0, temporal)
		# The object is removed from the object list
		objetos.remove(temporal)
	return objetos_orden_edad

def ordenar_nombre(grupo, personas, accion):
	objetos=list()
	# It goes through the lists with the personId
	for persona in personas:
		# A personId is extracted from the list
		personId=persona['personId']
		# The read_file function is called to find the object associated with the personId
		objeto=leer_archivo(personId)
		if objeto != None:
			# The object is added to an object list
			objetos.append(objeto)
	objetos_orden_edad=list()

	# Descending objects are sorted by age using insert
	while len(objetos) != 0:
		nombre_mayor= ''
		temporal=object()
		for ob in objetos:
			# The object with the highest age is identified
			if ob.nombre > nombre_mayor:
				nombre_mayor=ob.nombre     #cycle saved by the oldest person.
				temporal=ob
		# The object is put in a new list in an orderly way
		if accion==3:
			objetos_orden_edad.append(temporal)
		else:
			objetos_orden_edad.insert(0, temporal)
		# The object is removed from the object list
		objetos.remove(temporal)
	return objetos_orden_edad

def create_group(*args):
	"""Create a new group in Microsoft Azure.
	Return:
	Nothing
	"""
	try:
		group_id = int(args[0])
		group_name = args[1]
		# Create a group with an ID and name created by the user
		CF.person_group.create(group_id, group_name)
		tk.messagebox.showinfo('éxito', 'Se creó el grupo éxitosamente')

	except:
		tk.messagebox.showinfo('Mal', 'algo ha ido mal, prueba con otro id')

class Ventana(tk.Frame):
    
    def __init__(self, master=None):
        Frame.__init__(self, master) #parámetros que usted quiere enviar atraves del la clase Frame
        self.master = master
        self.iniciar_menu() #Mostrar el menú
        self.config(bg='slategray')
        self.label = tk.Label(self, text="Reconocimiento facial", font='Garamond 18', bg='slategray', fg='maroon')
        self.label.place(x=95, y=50)

        self.boton1=Button(self, text="Identificar persona", font=16, command=self.generar_ventana4)
        self.boton1.place(x=45, y=100)

        self.boton1=Button(self, text="Mostrar información", font=16, command=self.generar_ventana6)
        self.boton1.place(x=200, y=100)

    def generar_ventana6(self):
    	ventana6 = tk.Toplevel()
    	ventana6.title("Mostrar un grupo")
    	ventana6.config(bg='slategray')
    	ventana6.grupo=tk.Label(ventana6, text='Grupo', font='Garamond 18', bg='slategray')
    	ventana6.grupoid=tk.Label(ventana6, text='Grupo id', font='Garamond 18', bg='slategray')
    	ventana6.grupo1=tk.Label(ventana6, text='Familia', bg='slategray', font=11)
    	ventana6.grupoid1=tk.Label(ventana6, text='100', bg='slategray', font=11)
    	ventana6.grupo2=tk.Label(ventana6, text='Amigos', bg='slategray', font=11)
    	ventana6.grupoid2=tk.Label(ventana6, text='200', bg='slategray', font=11)
    	ventana6.grupo3=tk.Label(ventana6, text='Famosos', bg='slategray', font=11)
    	ventana6.grupoid3=tk.Label(ventana6, text='300', bg='slategray', font=11)
    	ventana6.lb_codigo = tk.Label(ventana6, text="Ingrese el id del grupo a mostrar: ", bg='slategray', font=11)
    	ventana6.sv_codigo_curso = tk.StringVar()
    	ventana6.tb_codigo_curso = tk.Entry(ventana6, textvariable = ventana6.sv_codigo_curso, width=40)
    	ventana6.b_guardar = tk.Button(ventana6, text = "continuar", font=11,
                                       command = lambda: self.generar_ventana7(
                                       	ventana6.sv_codigo_curso.get(),
                                          ventana6.sv_codigo_curso.set(" ")
                                       									))
    	ventana6.b_salir = tk.Button(ventana6, text = "Salir" , 
                                     command = ventana6.destroy, font=11)

    	ventana6.grupo.grid(column=0, row=0, padx=(20, 10))
    	ventana6.grupoid.grid(column=1, row=0, padx=(20, 10))
    	ventana6.grupo1.grid(column=0, row=1, padx=(20, 10))
    	ventana6.grupoid1.grid(column=1, row=1, padx=(20, 10))
    	ventana6.grupo2.grid(column=0, row=2, padx=(20, 10))
    	ventana6.grupoid2.grid(column=1, row=2, padx=(20, 10))
    	ventana6.grupo3.grid(column=0, row=3, padx=(20, 10))
    	ventana6.grupoid3.grid(column=1, row=3, padx=(20, 10))
    	ventana6.lb_codigo.grid(column=0, row=4, padx=(20,10))
    	ventana6.tb_codigo_curso.grid(column=1, row=4,  pady=5, columnspan=2, padx=(20,10))
    	ventana6.b_guardar.grid(column=0, row=6, pady=15)
    	ventana6.b_salir.grid(column=1, row=6, pady=15)

    def generar_ventana7(self, grupo, np):
    	ventana7 = tk.Toplevel()
    	ventana7.title("Mostrar un grupo")
    	ventana7.config(bg='slategray')
    	ventana7.grupo=tk.Label(ventana7, text='Mostrar de manera: ', font='Garamond 18', bg='slategray')
    	ventana7.grupoid=tk.Label(ventana7, text='Escribir: ', font='Garamond 18', bg='slategray')
    	ventana7.grupo1=tk.Label(ventana7, text='Ascendete por nombre', bg='slategray', font=11)
    	ventana7.grupoid1=tk.Label(ventana7, text='1', bg='slategray', font=11)
    	ventana7.grupo2=tk.Label(ventana7, text='Ascendete por edad', bg='slategray', font=11)
    	ventana7.grupoid2=tk.Label(ventana7, text='2', bg='slategray', font=11)
    	ventana7.grupo3=tk.Label(ventana7, text='Descendente por nombre', bg='slategray', font=11)
    	ventana7.grupoid3=tk.Label(ventana7, text='3', bg='slategray', font=11)
    	ventana7.grupo4=tk.Label(ventana7, text='Descendente por edad', bg='slategray', font=11)
    	ventana7.grupoid4=tk.Label(ventana7, text='4', bg='slategray', font=11)
    	ventana7.lb_codigo = tk.Label(ventana7, text="Ingrese una opción: ", bg='slategray', font=11)
    	ventana7.sv_codigo_curso = tk.StringVar()
    	ventana7.tb_codigo_curso = tk.Entry(ventana7, textvariable = ventana7.sv_codigo_curso, width=40)
    	ventana7.b_guardar = tk.Button(ventana7, text = "continuar", font=11,
                                       command = lambda: self.generar_ventana8(
                                       	ventana7.sv_codigo_curso.get(),
                                       	grupo,
                                        ventana7.sv_codigo_curso.set(""),

                                       									))
    	ventana7.b_salir = tk.Button(ventana7, text = "Salir" , 
                                     command = ventana7.destroy, font=11)

    	ventana7.grupo.grid(column=0, row=0, padx=(20, 10))
    	ventana7.grupoid.grid(column=1, row=0, padx=(20, 10))
    	ventana7.grupo1.grid(column=0, row=1, padx=(20, 10))
    	ventana7.grupoid1.grid(column=1, row=1, padx=(20, 10))
    	ventana7.grupo2.grid(column=0, row=2, padx=(20, 10))
    	ventana7.grupoid2.grid(column=1, row=2, padx=(20, 10))
    	ventana7.grupo3.grid(column=0, row=3, padx=(20, 10))
    	ventana7.grupoid3.grid(column=1, row=3, padx=(20, 10))
    	ventana7.grupo4.grid(column=0, row=4, padx=(20, 10))
    	ventana7.grupoid4.grid(column=1, row=4, padx=(20, 10))
    	ventana7.lb_codigo.grid(column=0, row=5, padx=(20,10))
    	ventana7.tb_codigo_curso.grid(column=1, row=5,  pady=5, columnspan=2, padx=(20,10))
    	ventana7.b_guardar.grid(column=0, row=6, pady=15)
    	ventana7.b_salir.grid(column=1, row=6, pady=15)

    def generar_ventana8(self, tipo_print, grupo, na):
    	lista=mostrar_informacion(grupo, tipo_print)

    	ventana8=tk.Toplevel()
    	ventana8.title("Mostrar grupo")
    	ventana8.geometry('565x480')
    	ventana8.config(bg='slategray')

    	scrollbar = tk.Scrollbar(ventana8, orient="vertical")

    	listbox = tk.Listbox(ventana8, bg='slategray', font=14, justify='center', width=60, height=23, yscrollcommand=scrollbar.set)
    	scrollbar.config(command=listbox.yview)
    	scrollbar.grid(column=1, row=0, sticky='nsew')
    	listbox.grid(column=0, row=0)

    	ventana8.b_salir = tk.Button(ventana8, text = "atras" , 
                                     command = ventana8.destroy, font=11).grid(column=0, row=1)

    	if int(grupo)==100:
    		texto1='Familiar: '
    		texto2='Residencia del familiar: '
    	elif int(grupo)==200:
    		texto1='Tiempo de amistad: '
    		texto2='Amigos en común: '
    	elif int(grupo)==300:
    		texto1='Actividad: '
    		texto2='Famoso favorito: '
    	i=0
    	j=0
    	while i < len(lista):
    	 	identificacion, Id, nombre, edad, genero, arg1, arg2 =mostrar_info(grupo, lista[i])
    	 	listbox.insert(j, 'Identificación: '+ str(identificacion))
    	 	j+=1
    	 	listbox.insert(j, 'PersonId: '+ str(Id))
    	 	j+=1
    	 	listbox.insert(j, 'Nombre: '+ str(nombre))
    	 	j+=1
    	 	listbox.insert(j, 'edad: '+ str(int(edad)) + ' años')
    	 	j+=1
    	 	listbox.insert(j, 'Género: '+ str(genero))
    	 	j+=1
    	 	listbox.insert(j, texto1 + str(arg1))
    	 	j+=1
    	 	listbox.insert(j, texto2 + str(arg2))
    	 	j+=1
    	 	listbox.insert(j, '\n')
    	 	j+=1
    	 	i+=1
    def generar_ventana4(self):
        ventana4 = tk.Toplevel()
        ventana4.title("Identificar persona")
        ventana4.config(bg='slategray')
        ventana4.grupo=tk.Label(ventana4, text='Grupo', font='Garamond 18', bg='slategray')
        ventana4.grupoid=tk.Label(ventana4, text='Grupo id', font='Garamond 18', bg='slategray')
        ventana4.grupo1=tk.Label(ventana4, text='Familia', bg='slategray', font=11)
        ventana4.grupoid1=tk.Label(ventana4, text='100', bg='slategray', font=11)
        ventana4.grupo2=tk.Label(ventana4, text='Amigos', bg='slategray', font=11)
        ventana4.grupoid2=tk.Label(ventana4, text='200', bg='slategray', font=11)
        ventana4.grupo3=tk.Label(ventana4, text='Famosos', bg='slategray', font=11)
        ventana4.grupoid3=tk.Label(ventana4, text='300', bg='slategray', font=11)
        ventana4.grupo.grid(column=0, row=0, padx=(20, 10))
        ventana4.grupoid.grid(column=1, row=0, padx=(20, 10))
        ventana4.grupo1.grid(column=0, row=1, padx=(20, 10))
        ventana4.grupoid1.grid(column=1, row=1, padx=(20, 10))
        ventana4.grupo2.grid(column=0, row=2, padx=(20, 10))
        ventana4.grupoid2.grid(column=1, row=2, padx=(20, 10))
        ventana4.grupo3.grid(column=0, row=3, padx=(20, 10))
        ventana4.grupoid3.grid(column=1, row=3, padx=(20, 10))
        ventana4.lb_codigo = tk.Label(ventana4, text="Ingrese el id del grupo de la persona a identificar: ", bg='slategray', font=11)
        ventana4.sv_codigo_curso = tk.StringVar()
        ventana4.tb_codigo_curso = tk.Entry(ventana4, textvariable = ventana4.sv_codigo_curso, width=40)
        ventana4.lb_imagen= tk.Label(ventana4, text="Paht de la imagen: ", bg='slategray', font=11)
        global guarda_direcc
        guarda_direcc = tk.StringVar()
        ventana4.tb_imagen=Button(ventana4, text='Buscar', font=11, command=lambda: self.buscador())
        ventana4.b_salir = tk.Button(ventana4, text = "Salir" , 
                                     command = ventana4.destroy, font=11)
        ventana4.b_guardar = tk.Button(ventana4, text = "continuar", font=11,
                                       command = lambda: self.generar_ventana5(
                                       	 guarda_direcc,
                                       	ventana4.sv_codigo_curso.get(),
                                          ventana4.sv_codigo_curso.set(""),
                                       									))
        ventana4.lb_codigo.grid(column=0, row=4, padx=(20,10))
        ventana4.tb_codigo_curso.grid(column=1, row=4,  pady=5, columnspan=2, padx=(20,10))
        ventana4.lb_imagen.grid(column=0, row=5, pady=(20, 10))
        ventana4.tb_imagen.grid(column=1, row=5, pady=15)
        ventana4.b_salir.grid(column=1, row=6, pady=15)
        ventana4.b_guardar.grid(column=0, row=6, pady=15)

    def buscador(self):
    	global guarda_direcc
    	guarda_direcc= filedialog.askopenfile(
            initialdir = "/",title = "Selecionar archivo",
            filetypes = (("jpeg files",".jpg"),("all files",".*"))
        )
    def generar_ventana5(self, picture, group_id, na):
    	global guarda_direcc
    	guarda_direcc=''
    	picture=str(picture.name)
    	if int(group_id)==100:
    		texto1='Familiar: '
    		texto2='Residencia del familiar: '
    	elif int(group_id)==200:
    		texto1='Tiempo de amistad: '
    		texto2='Amigos en común: '
    	elif int(group_id)==300:
    		texto1='Actividad: '
    		texto2='Famoso favorito: '

    	group_id=int(group_id)
    	response = CF.face.detect(picture)
    	face_ids = [d['faceId'] for d in response]
    	#print(response)    
    	identified_faces = CF.face.identify(face_ids, group_id)
    	personas = identified_faces[0]
    	#print(personas)
    	candidates_list = personas['candidates']
    	candidates = candidates_list[0]
    	#print(candidates)
    	person = candidates['personId']
    	#print(persona)
    	person_data = CF.person.get(group_id, person)
    	#print(persona_info)
    	person_name = person_data['name']
    	response = CF.face.detect(picture)
    	#print(response)
    	dic = response[0]
    	#print(dic)
    	faceRectangle = dic['faceRectangle']
    	#print(faceRectangle)
    	width = faceRectangle['width']
    	top = faceRectangle['top']
    	height = faceRectangle['height']
    	left = faceRectangle['left']
    	image=Image.open(picture)
    	draw = ImageDraw.Draw(image)
    	draw.rectangle((left,top,left + width,top+height), outline='red')
    	font = ImageFont.truetype('c:/Users/bryam/Desktop/semana_8/Arial_Unicode.ttf', 50)
    	draw.text((50, 50), person_name, font=font,  fill="white") 
    	# The function leer_archivo is called to obtain the information of the identified person that
    	# needs to be printed, the personId is sent as an argument
    	persona=leer_archivo(person)
    	# The mostrar_info function is called to display the information of the identified person
    	identificacion, Id, nombre, edad, genero, arg1, arg2 = mostrar_info(group_id, persona)
    	edad=str(int(edad))+' años'

    	ventana5=tk.Toplevel()
    	ventana5.title("Identificar persona")
    	ventana5.config(bg='slategray')
    	image = image.resize((250,250), Image.ANTIALIAS)
    	ventana5.img = ImageTk.PhotoImage(image)
    	ventana5.canvas = Canvas(ventana5, width =250, height= 250)
    	
    	ventana5.canvas.create_image(0,0, anchor =NW, image = ventana5.img)

    	ventana5.lb_identificacion = tk.Label(ventana5, text="Identificación: ", bg='slategray', font= 11)
    	ventana5.lb_personid = tk.Label(ventana5, text="Person Id: ", bg='slategray', font= 11)
    	ventana5.lb_nombre = tk.Label(ventana5, text="Nombre: ", bg='slategray', font= 11)
    	ventana5.lb_edad = tk.Label(ventana5, text="Edad: ", bg='slategray', font= 11)
    	ventana5.lb_genero = tk.Label(ventana5, text="Género: ", bg='slategray', font= 11)
    	ventana5.lb_arg1 = tk.Label(ventana5, text= texto1, bg='slategray', font= 11)
    	ventana5.lb_arg2 = tk.Label(ventana5, text= texto2, bg='slategray', font= 11)
    	ventana5.tb_identificacion = tk.Label(ventana5, text = str(identificacion), bg='slategray', font= 11)
    	ventana5.tb_personid = tk.Label(ventana5, text=Id, bg='slategray', font= 11)
    	ventana5.tb_nombre = tk.Label(ventana5, text=nombre, bg='slategray', font= 11)
    	ventana5.tb_edad = tk.Label(ventana5, text=str(edad), bg='slategray', font= 11)
    	ventana5.tb_genero = tk.Label(ventana5, text=str(genero), bg='slategray', font= 11)
    	ventana5.tb_arg1 = tk.Label(ventana5, text=str(arg1), bg='slategray', font= 11)
    	ventana5.tb_arg2 = tk.Label(ventana5, text=str(arg2), bg='slategray', font= 11)

    	ventana5.b_salir = tk.Button(ventana5, text = "Salir", width =10, font=11,
                                     command = lambda: ventana5.destroy())
    	ventana5.canvas.grid(column=0, row=0, columnspan=2)
    	ventana5.lb_identificacion.grid(column=0, row=1)
    	ventana5.tb_identificacion.grid(column=1, row=1)
    	ventana5.lb_personid.grid(column=0, row=2)
    	ventana5.tb_personid.grid(column=1, row=2)
    	ventana5.lb_nombre.grid(column=0, row=3)
    	ventana5.tb_nombre.grid(column=1, row=3)
    	ventana5.lb_edad.grid(column=0, row=4)
    	ventana5.tb_edad.grid(column=1, row=4)
    	ventana5.lb_genero.grid(column=0, row=5)
    	ventana5.tb_genero.grid(column=1, row=5)
    	ventana5.lb_arg1.grid(column=0, row=6)
    	ventana5.tb_arg1.grid(column=1, row=6)
    	ventana5.lb_arg2.grid(column=0, row=7)
    	ventana5.tb_arg2.grid(column=1, row=7)
    	ventana5.b_salir.grid(column=0, row=8, columnspan=2, ipady=1)

    def iniciar_menu(self):
        self.master.title("Etapa 3")
        self.pack(fill=BOTH, expand=1)
        #Crear la instancia del menu
        menu = Menu(self.master)
        self.master.config(menu=menu)
        
        #Crear el objeto Archivo
        archivo = Menu(menu)
        #Agregar comandos a la opción del menú
        #Opción salir
        archivo.add_command(label="Salir", command=self.salir)
        menu.add_cascade(label="Archivo", menu=archivo)

        #Crear el objeto Ventanas
        ventanas = Menu(menu)
        ventanas.add_command(label="Crear grupo", command=self.generar_ventana1)
        ventanas.add_command(label="Crear persona", command=self.generar_ventana2)
        menu.add_cascade(label="Herramientas", menu=ventanas)
        
    def salir(self):
    	MsgBox = tk.messagebox.askquestion ('Salir de la aplicación','Estas seguro de que quieres salir?', icon = 'warning')
    	if MsgBox == 'yes':
            exit()

    def generar_ventana1(self):
        ventana1 = tk.Toplevel()
        ventana1.title("Crear grupo")
        ventana1.config(bg='slategray')

        ventana1.lb_curso = tk.Label(ventana1, text="Nombre del nuevo grupo: ", bg='slategray')
        ventana1.lb_codigo = tk.Label(ventana1, text="Código del nuevo grupo: ", bg='slategray')

        ventana1.sv_nombre_curso = tk.StringVar()
        ventana1.tb_nombre_curso = tk.Entry(ventana1, textvariable = ventana1.sv_nombre_curso, width=40)

        ventana1.sv_codigo_curso = tk.StringVar()
        ventana1.tb_codigo_curso = tk.Entry(ventana1, textvariable = ventana1.sv_codigo_curso, width=40)

        ventana1.b_salir = tk.Button(ventana1, text = "Salir" , 
                                     command = ventana1.destroy)

        ventana1.b_guardar = tk.Button(ventana1, text = "Crear grupo",
                                       command = lambda: create_group(
                                       	ventana1.sv_codigo_curso.get(),
                                          ventana1.sv_nombre_curso.get(),
                                          ventana1.sv_nombre_curso.set(""),
                                          ventana1.sv_codigo_curso.set("")
                                       									))
        ventana1.lb_curso.grid(column=0, row=0, padx=(20,10))
        ventana1.lb_codigo.grid(column=0, row=1, padx=(20,10))

        ventana1.tb_nombre_curso.grid(column=1, row=0, pady=5, columnspan=2, padx=(20,10))
        ventana1.tb_codigo_curso.grid(column=1, row=1,  pady=5, columnspan=2, padx=(20,10))

        ventana1.b_salir.grid(column=1, row=4, pady=15)
        ventana1.b_guardar.grid(column=0, row=4, pady=15)

    def generar_ventana2(self):
        ventana2 = tk.Toplevel()
        ventana2.title("Crear Persona")
        ventana2.config(bg='slategray')
        ventana2.grupo=tk.Label(ventana2, text='Grupo', font=14, bg='slategray')
        ventana2.grupoid=tk.Label(ventana2, text='Grupo id', font=14, bg='slategray')
        ventana2.grupo1=tk.Label(ventana2, text='Familia', bg='slategray')
        ventana2.grupoid1=tk.Label(ventana2, text='100', bg='slategray')
        ventana2.grupo2=tk.Label(ventana2, text='Amigos', bg='slategray')
        ventana2.grupoid2=tk.Label(ventana2, text='200', bg='slategray')
        ventana2.grupo3=tk.Label(ventana2, text='Famosos', bg='slategray')
        ventana2.grupoid3=tk.Label(ventana2, text='300', bg='slategray')
        ventana2.grupo.grid(column=0, row=0, padx=(20, 10))
        ventana2.grupoid.grid(column=1, row=0, padx=(20, 10))
        ventana2.grupo1.grid(column=0, row=1, padx=(20, 10))
        ventana2.grupoid1.grid(column=1, row=1, padx=(20, 10))
        ventana2.grupo2.grid(column=0, row=2, padx=(20, 10))
        ventana2.grupoid2.grid(column=1, row=2, padx=(20, 10))
        ventana2.grupo3.grid(column=0, row=3, padx=(20, 10))
        ventana2.grupoid3.grid(column=1, row=3, padx=(20, 10))
        ventana2.lb_codigo = tk.Label(ventana2, text="Ingres el id del grupo de la nueva persona: ", bg='slategray')
        ventana2.sv_codigo_curso = tk.StringVar()
        ventana2.tb_codigo_curso = tk.Entry(ventana2, textvariable = ventana2.sv_codigo_curso, width=40)
        ventana2.b_salir = tk.Button(ventana2, text = "Salir" , 
                                     command = ventana2.destroy)
        ventana2.b_guardar = tk.Button(ventana2, text = "continuar",
                                       command = lambda: self.generar_ventana3(
                                       	ventana2.sv_codigo_curso.get(),
                                          ventana2.sv_codigo_curso.set("")
                                       									))
        ventana2.lb_codigo.grid(column=0, row=4, padx=(20,10))
        ventana2.tb_codigo_curso.grid(column=1, row=4,  pady=5, columnspan=2, padx=(20,10))
        ventana2.b_salir.grid(column=1, row=5, pady=15)
        ventana2.b_guardar.grid(column=0, row=5, pady=15)

    def generar_ventana3(self, grupo, na):
        if int(grupo)==100:
            texto1='¿Qué familiar es?: '
            texto2='¿Dónde vive tu familar?: '
        elif int(grupo)==200:
            texto1='Hace cuántos años son amigos?: '
            texto2='¿cúantos amigos tienen en común?: '
        elif int(grupo)==300:
            texto1='Este famoso a qué se dedica?: '
            texto2='Es tu famoso favorito?: '
        ventana3 = tk.Toplevel()
        ventana3.title("Crear una persona")
        ventana3.config(bg='slategray')
        ventana3.lb_identificacion = tk.Label(ventana3, text="Identificación: ", bg='slategray')
        ventana3.lb_nombre= tk.Label(ventana3, text="Nombre: ", bg='slategray')
        ventana3.lb_imagen= tk.Label(ventana3, text="Paht de la imagen: ", bg='slategray')
        ventana3.lb_arg1= tk.Label(ventana3, text=texto1, bg='slategray')
        ventana3.lb_arg2= tk.Label(ventana3, text=texto2, bg='slategray')
        ventana3.sv_identificacion = tk.StringVar()
        ventana3.tb_identificacion = tk.Entry(ventana3, textvariable = ventana3.sv_identificacion, width=40)
        ventana3.sv_nombre = tk.StringVar()
        ventana3.tb_nombre = tk.Entry(ventana3, textvariable = ventana3.sv_nombre, width=40)
        global guarda_direcc
        guarda_direcc = tk.StringVar()
        ventana3.tb_imagen=Button(ventana3, text='Buscar', font=11, command=lambda: self.buscador())
        ventana3.sv_arg1 = tk.StringVar()
        ventana3.tb_arg1=Entry(ventana3, textvariable=ventana3.sv_arg1,
        					width=40,)
        ventana3.sv_arg2 = tk.StringVar()
        ventana3.tb_arg2=Entry(ventana3, textvariable=ventana3.sv_arg2,
        					width=40,)
        ventana3.b_salir = tk.Button(ventana3, text = "Salir" , 
                                     command = ventana3.destroy)
        ventana3.b_guardar = tk.Button(ventana3, text = "Crear persona",
                                       command = lambda: crea_persona(
                                       	ventana3.sv_identificacion.get(),
                                          ventana3.sv_nombre.get(),
                                          guarda_direcc,
                                          ventana3.sv_arg1.get(),
                                          ventana3.sv_arg2.get(),
                                          grupo,
                                          ventana3.sv_identificacion.set(''),
                                          ventana3.sv_nombre.set(''),
                                          ventana3.sv_arg1.set(''),
                                          ventana3.sv_arg2.set('')))
        ventana3.lb_identificacion.grid(column=0, row=0, padx=(20,10))
        ventana3.lb_nombre.grid(column=0, row=1, padx=(20,10))
        ventana3.lb_imagen.grid(column=0, row=4, padx=(20, 10))
        ventana3.lb_arg1.grid(column=0, row=2, padx=(20, 10))
        ventana3.lb_arg2.grid(column=0, row=3, padx=(20, 10))
        ventana3.tb_identificacion.grid(column=1, row=0, pady=5, columnspan=2, padx=(20,10))
        ventana3.tb_nombre.grid(column=1, row=1,  pady=5, columnspan=2, padx=(20,10))
        ventana3.tb_imagen.grid(column=1, row=4, pady=5, columnspan=2, padx=(20,10))
        ventana3.tb_arg1.grid(column=1, row=2, pady=5, columnspan=2, padx=(20,10))
        ventana3.tb_arg2.grid(column=1, row=3, pady=5, columnspan=2, padx=(20,10))
        ventana3.b_salir.grid(column=1, row=5, pady=15)
        ventana3.b_guardar.grid(column=0, row=5, pady=15)


if __name__=="__main__":
	guarda_direcc=''
	root = tk.Tk()
	root.geometry("400x300") 
	main = Ventana(root)
	main.pack(fill="both", expand=True) 
root.mainloop()