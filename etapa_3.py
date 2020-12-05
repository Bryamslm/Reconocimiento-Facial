import sys
import requests
import json
import cognitive_face as CF
from PIL import Image, ImageDraw, ImageFont
import pickle
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

def crea_persona():
	"""Create a new person.
	Arguments: Nothing
	Return: Nothing

	"""
	print('\nSeleccione o escriba el numero del grupo a donde desea agregar la persona:')
	print('100 --> Familia')
	print('200 --> Amigos')
	print('300 --> Famosos')
	# The group the new person belongs to
	grupo= int(input('Seleccione el grupo:'))
	# The function ingresa_informacion is called to determine the information of the new person
	# The information depends on the group where the person belongs
	identificacion, nombre, image_path, arg_1, arg_2=ingresa_informacion(grupo)
	# The emotion function is called to determine the age and
	# gender of the new person from the entered image.
	edad, genero= emotion(image_path, True)
	# The create_person function is called to add the new person
	# in Microsoft Azure and also get their personId
	personId=create_person(nombre, image_path, grupo)
	# The new person is created according to the group to which it belongs
	if grupo==100:
		# a family member is created
		persona=Familia(identificacion, personId, nombre, edad, genero, image_path, arg_1, arg_2)
		# Personas_en_archivo function is called to add object to binaio file
		Personas_en_archivo(persona)
		print('Se agregó persona a lista de familia exitosamente')	
	elif grupo==200:
		# a friend member is created
		persona=Amigos(identificacion, personId, nombre, edad, genero, image_path, arg_1, arg_2)
		# Personas_en_archivo function is called to add object to binaio file
		Personas_en_archivo(persona)
		print('Se agregó persona a lista de amigos exitosamente')
	elif grupo==300:
		# a famous member is created
		persona=Famosos(identificacion, personId, nombre, edad, genero, image_path, arg_1, arg_2)
		# Personas_en_archivo function is called to add object to binaio file
		Personas_en_archivo(persona)
		print('Se agregó persona a lista de famosos exitosamente')
	else:
		# A person with only basic characteristics is created.
		persona=Persona(identificacion, personId, nombre, edad, genero, image_path)
		# Personas_en_archivo function is called to add object to binaio file
		Personas_en_archivo(persona)

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
    print(status)
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

def ingresa_informacion(grupo):
	"""
	Function that asks the user for information according
	to the type of person they want to create
	Arguments:
	grupo: Group where the person is going to be added indicator to know
	what type of information is going to be requested from the user
	Returns: 
	identificacion, nombre, image_path, arg_1, arg_2

	"""
	# The identification of the person is requested to create
	identificacion=input('ingrese la identificación: ')
	# The name of the person is requested to create
	nombre=input('Ingrese el nombre: ')
	# The path of the image of the person to create is requested
	image_path=input('Ingrese el path de la imágen: ')
	#https://docs.microsoft.com/en-us/azure/cognitive-services/computer-vision/quickstarts/python-disk
	# Read the image into a byte array
	# Depending on the group, the corresponding information is requested:
	if grupo==100:
		arg_1=input('¿Qué familar es?: ')
		arg_2=input('¿Dónde vive tu familar?: ')
	elif grupo==200:
		arg_1=input('Hace cuántos años son amigos?: ')
		arg_2=input('¿cúantos amigos tienen en común?: ')
	elif grupo==300:
		arg_1=input('Este famoso a qué se dedica?: ')
		arg_2=input('Es tu famoso favorito?: ')
	else:
		arg_1=None
		arg_2=None

	return identificacion, nombre, image_path, arg_1, arg_2

def identificar():
	"""
	Detects if a person already belongs to a group
	and prints their image with a rectangle on the face
	Returns:
	Nothing

	"""
	# The path of the image of the person to detect is requested
	picture=input('Ingrese el path de la imágen: ')
	print('\n100 --> Familia')
	print('200 --> Amigos')
	print('300 --> Famosos') 
	print('Otro --> Escribir grupo')
	# The group to which the person to be identified belongs is needed
	group_id = int(input("Dígite el id del grupo: "))
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
	image.show()
	# The function leer_archivo is called to obtain the information of the identified person that
	# needs to be printed, the personId is sent as an argument
	persona=leer_archivo(person)
	print('\n\tEsta es la información de la persona presente en la imagen\n')
	# The mostrar_info function is called to display the information of the identified person
	mostrar_info(group_id, persona)

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
	print('Identificación:', persona.identificacion)
	print('PersonId:', persona.personId)
	print('Nombre:', persona.nombre)
	print('Edad:', persona.edad)
	print('Género:', persona.genero)
	# Depending on the group to which the person belongs,
	# it will show their respective information
	if grupo== 100:
		print('Cercania:', persona.cercania)
		print('Residencia:', persona.residencia)
	elif grupo== 200:
		print('Tiempo de amistad:', persona.tiempo_amistad,'años')
		print('Amigos en común:', persona.amigos_comun)
	elif grupo== 300:
		print('Actividad:', persona.actividad)
		print('Famoso favorito:', persona.favorito,)

def mostrar_informacion():
	"""
	Displays the information of all the people in
	a group descending by age and ascending by name
	Return:
	Nothing

	"""
	print('\nSeleccione o escriba el numero del',
		'grupo que desea ver la información:')
	print('100 --> Familia')
	print('200 --> Amigos')
	print('300 --> Famosos')
	print('Otro --> Ingres el Id del grupo')
	grupo= int(input('Seleccione el grupo:'))
	# A list with the personId is obtained to look for them in binary file
	personas=CF.person.lists(grupo)

	while True:
		print('\n1 --> Ascendete por nombre')
		print('2 --> Ascendete por edad')
		print('3 --> Descendente por nombre')
		print('4 --> Descendente por edad')
		accion=int(input('\nSeleccione cómo quiere imprimir la información: '))
		if accion==1:
			ordenar_nombre(grupo, personas, accion)
			break
		elif accion==2:
			ordenar_edad(grupo, personas, accion)
			break
		elif accion==3:
			ordenar_nombre(grupo, personas, accion)
			break
		elif accion==4:
			ordenar_edad(grupo, personas, accion)
			break
		else:
			print('\nOpción invalida')

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
	print('\n>> Información de objetos de forma descendente según la edad <<\n')
	# The new list is scrolled with the ordered objects and it is printed
	for persona in objetos_orden_edad:
		mostrar_info(grupo, persona)
		print('')

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
	print('\n>> Información de objetos de forma descendente según la edad <<\n')
	# The new list is scrolled with the ordered objects and it is printed
	for persona in objetos_orden_edad:
		mostrar_info(grupo, persona)
		print('')

def create_group():
	"""Create a new group in Microsoft Azure.
	Return:
	Nothing
	"""
	group_id = int(input("\nDígite el id del nuevo grupo: "))
	group_name = input("Dígite el nombre del nuevo grupo: ")
	# Create a group with an ID and name created by the user
	CF.person_group.create(group_id, group_name)
	print("\nEl grupo fue creado con éxito")

def main():
	"""Displays the menu of actions that can be performed.
	
	"""
	while True:
		print('\t\t----Bienvenido al menú principal----\n')
		print('Seleccione la tarea a realizar:\n')
		print("Dígite 1 -> Agregar persona a un grupo")
		print("Dígite 2 -> Identificar persona")
		print('Dígite 3 -> Crear nuevo grupo')
		print("Dígite 4 -> Mostrar información de todas las personas")
		print('Dígite 0 -> Salir')
		accion=int(input('\nIngrese la opción de tarea a reliazar: '))
		if accion==1:
			crea_persona()
		elif accion==2:
			identificar()
		elif accion==3:
			create_group()
		elif accion ==4:
			mostrar_informacion()
		elif accion ==0:
			exit()
		else:
			print('\nOpción invalida\n')
main()