#!/usr/local/bin/python
from flask import Flask, jsonify, abort, make_response, request, url_for, redirect, render_template
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from cgi import parse_header
import psycopg2
import sys
import json

#instanciar un objeto.
app = Flask(__name__)

##################################################################
#########             Pagina principal               #############
##################################################################
#Indicar al servidor cual es la ruta a cceder
#index() funcion que regesa un string cuando se acceda a esta ruta
#Luego se debe configurar otro tipo de contenido front end
#visualizar desde el navegador en internet
@app.route("/")
#index() funcion que regesa un string cuando se acceda a esta ruta
#Luego se debe configurar otro tipo de contenido front end
#visualizar desde el navegador en internet
def index(): 
    return "Bienvenido A esta web CAMBIADA"

@app.route("/index")
def show_index():
	return render_template('index.html')

##################################################################
#########        Manejo del lado de internet         #############
##################################################################

@app.route("/show_tasks")
def show_tasks():
	#Define our connection string
	conn_string = "host='ec2-50-19-118-164.compute-1.amazonaws.com' dbname='d5h7i7drfj4m9r' user='jnixinbaeyslyd' password='e7b9ee1226683bb5c5725f8aaa298cc0d3b7670cb1c88f5ee206f21583d39419'"

	# get a connection, if a connect cannot be made an exception will be raised here
	conn = psycopg2.connect(conn_string)
 
 	# conn.cursor will return a cursor object, you can use this cursor to perform queries
	cursor = conn.cursor()

	# execute our Query
	cursor.execute("SELECT * FROM tasks ORDER BY id")

	# retrieve the records from the database
	records = cursor.fetchall()

	cursor.close()
	conn.close()

	return render_template('show_tasks.html', registers=records)

@app.route("/show_state")
def show_state():
	#Define our connection string
	conn_string = "host='ec2-50-19-118-164.compute-1.amazonaws.com' dbname='d5h7i7drfj4m9r' user='jnixinbaeyslyd' password='e7b9ee1226683bb5c5725f8aaa298cc0d3b7670cb1c88f5ee206f21583d39419'"

	# get a connection, if a connect cannot be made an exception will be raised here
	conn = psycopg2.connect(conn_string)
 
 	# conn.cursor will return a cursor object, you can use this cursor to perform queries
	cursor = conn.cursor()

	# execute our Query
	cursor.execute("SELECT * FROM cpu")

	# retrieve the records from the database
	records = cursor.fetchall()

	# execute our Query
	cursor.execute("SELECT * FROM mem")

	# retrieve the records from the database
	records1 = cursor.fetchall()

	# execute our Query
	cursor.execute("SELECT * FROM disk")

	# retrieve the records from the database
	records2 = cursor.fetchall()

	cursor.close()
	conn.close()

	return render_template('show_state.html', registers=records, registers1=records1, registers2=records2)


#Metodo que crea un nuevo registro en una tabla de la base de datos con la nueva 
#tarea
#recibe un json como parametro con los datos suficientes para generar la tarea
@app.route("/set_task",  methods=['GET', 'POST'])
def crearNuevaTarea():
	if request.method == 'POST':
		description = request.form['description']
		link = request.form['magnet']
		date = request.form['date']
		state = request.form['state']
		progress = request.form['progress']
		
		name = link.split("&dn=")[1].replace("+", " ")
		name = name.replace("%28", "(")
		name = name.replace("%29", ")")
		name = name.replace("%5\B", "[")
		name = name.replace("%5\D", "]")
		#Define our connection string
		conn_string = "host='ec2-50-19-118-164.compute-1.amazonaws.com' dbname='d5h7i7drfj4m9r' user='jnixinbaeyslyd' password='e7b9ee1226683bb5c5725f8aaa298cc0d3b7670cb1c88f5ee206f21583d39419'"

		# get a connection, if a connect cannot be made an exception will be raised here
		conn = psycopg2.connect(conn_string)
	 
	 	# conn.cursor will return a cursor object, you can use this cursor to perform queries
		cursor = conn.cursor()
	
		query =  "INSERT INTO tasks (name, magnet_link, data_time, state, progress, description) VALUES (%s, %s, %s, %s, %s, %s);"
		data = (name, link, date, state, progress, description)

		# execute our Query
		cursor.execute(query, data)
		conn.commit()
		result = cursor.rowcount

		if result >= 1:
			# execute our Query
			cursor.execute("SELECT * FROM tasks ORDER BY id")

			# retrieve the records from the database
			records = cursor.fetchall()

			# retrieve the records from the database
			cursor.close()
			conn.close()
			return render_template('show_tasks.html', registers=records)
		else: 
			# retrieve the records from the database
			cursor.close()
			conn.close()
			return "No se ha guardado hubo un problema"

	else:
		return render_template('create_task.html') 


##################################################################
#########       Manejo del lado de la intranet       #############
##################################################################

#Metodo que recibe un json con los datos nuevos para actualizar los campos 
#de la tabla en la base de datos que contienen el estado de los recursos 
#del host de la intranet
@app.route("/set_state", methods=['PUT'])
def actualizarEstado():
	if request.method == 'PUT':
		receive_json = request.json

		cpu_json = receive_json['cpu']
		usr = cpu_json['user'].strip()
		sys = cpu_json['system'].strip()
		idl = cpu_json['idle'].strip()
		wai = cpu_json['waiting'].strip()
		vms = cpu_json['time stolen by virtual machines'].strip()
		fecha = cpu_json['fecha'].strip()

		mem_json = receive_json['mem']
		swpd = mem_json['swpd'].strip()
		free = mem_json['free'].strip()
		buff = mem_json['buff'].strip()
		cache = mem_json['cache'].strip()

		disk_json = receive_json['disk']
		hdfree = disk_json['hdfree'].strip()

		#Define our connection string
		conn_string = "host='ec2-50-19-118-164.compute-1.amazonaws.com' dbname='d5h7i7drfj4m9r' user='jnixinbaeyslyd' password='e7b9ee1226683bb5c5725f8aaa298cc0d3b7670cb1c88f5ee206f21583d39419'"

		# get a connection, if a connect cannot be made an exception will be raised here
		conn = psycopg2.connect(conn_string)

		# conn.cursor will return a cursor object, you can use this cursor to perform queries
		cursor = conn.cursor()

		query = "UPDATE cpu SET usr=(%s), sys=(%s), idl=(%s), wai=(%s), vms=(%s), data_time=(%s) WHERE id = (%s)"
		cursor.execute(query, (usr,sys,idl,wai,vms,fecha,'1'))
		conn.commit()

		query1 = "UPDATE mem SET swpd=(%s), free=(%s), buff=(%s), cache=(%s), data_time=(%s) WHERE id = (%s)"
		cursor.execute(query1, (swpd,free,buff,cache,fecha,'1'))
		conn.commit()

		query2 = "UPDATE disk SET hdfree=(%s), data_time=(%s) WHERE id = (%s)"
		cursor.execute(query2, (hdfree,fecha,'1'))
		conn.commit()

		cursor.close()
		conn.close()

		return jsonify({'data':receive_json})

# Actualiza el estado y el progreso de las descargas en curso
@app.route("/progress_tasks",  methods=['PUT'])
def progressTasks():
	if request.method == 'PUT':
		receive_json = request.json
		array_tasks = receive_json['data']
		if len(array_tasks) > 0:
			for task in array_tasks:
				name = task['name']
				progress = task['progress']
				status = task['status']
				data_time = task['fecha']
				#Define our connection string
				conn_string = "host='ec2-50-19-118-164.compute-1.amazonaws.com' dbname='d5h7i7drfj4m9r' user='jnixinbaeyslyd' password='e7b9ee1226683bb5c5725f8aaa298cc0d3b7670cb1c88f5ee206f21583d39419'"

				# get a connection, if a connect cannot be made an exception will be raised here
				conn = psycopg2.connect(conn_string)

				# conn.cursor will return a cursor object, you can use this cursor to perform queries
				cursor = conn.cursor()

				query = "UPDATE tasks SET progress=(%s), state=(%s), data_time=(%s) WHERE name = (%s)"
				cursor.execute(query, (progress,status,data_time,name))
				conn.commit()
				cursor.close()
				conn.close()

		return jsonify({'data':array_tasks})

#Metodo para retornar las nuevas tareas pedidas desde internet y que previamente no hayan sido 
#retornadas
@app.route("/get_tasks", methods=['GET'])
def retornarNuevasTareas():
	#array of tasks to return
	tareas = []

	#Define our connection string
	conn_string = "host='ec2-50-19-118-164.compute-1.amazonaws.com' dbname='d5h7i7drfj4m9r' user='jnixinbaeyslyd' password='e7b9ee1226683bb5c5725f8aaa298cc0d3b7670cb1c88f5ee206f21583d39419'"

	# get a connection, if a connect cannot be made an exception will be raised here
	conn = psycopg2.connect(conn_string)
 
 	# conn.cursor will return a cursor object, you can use this cursor to perform queries
	cursor = conn.cursor()

	# execute our Query
	cursor.execute("SELECT * FROM tasks WHERE state = 'no-enviado' ORDER BY id")

	# retrieve the records from the database
	records = cursor.fetchall()

	tarea = {}
	for row in records:
		cursor.execute("UPDATE tasks SET state=(%s) WHERE id = (%s)", ('enviado',row[0]))
		conn.commit()
		tarea = {'id':row[0],
				 'name':row[1],
				 'link':row[2]}
		tareas.append(tarea)
	cursor.close()
	conn.close()
	response = {'tasks':tareas}
	return jsonify(response)

##################################################################
#########               Manejo del error             #############
##################################################################

 #Respuesa en forma de json para manejar el error
@app.errorhandler(404)
def not_found(error):
 return make_response(jsonify({'error': 'Not found'}), 404)


##################################################################
#########        Inicializacion del servidor         #############
##################################################################
#Ejecucion del servidor por default en el puerto 5000
#se puede cambiar el puerto con app.run( debug = True, port=5005 )
if __name__ == '__main__':
    app.run(debug=True, port=5000)