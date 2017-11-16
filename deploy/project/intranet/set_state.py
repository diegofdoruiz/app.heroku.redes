#!/usr/bin/python
from flask import Flask, jsonify, make_response, jsonify, url_for, redirect
import json
import requests
import time

############## Intranet Pasarela #############################
def doRequest(resources_json):
	url = 'http://lit-anchorage-86748.herokuapp.com/set_state'
	headers = {'content-type': 'application/json'}
	response = requests.put(url, data=json.dumps(resources_json), headers=headers)
	return response.text
###############################################################



################ Intranet RESTmonitoring ######################
def getSources():
	#Obteniendo los datos de la cpu
	fecha = time.ctime()
	url_cpu = 'http://localhost:5000/cpu/'
	route_cpu = 'us'
	cpu_us = requests.get(url_cpu+route_cpu)
	cpu_us_json = json.loads(cpu_us.text)

	route_cpu = 'sy'
	cpu_sy = requests.get(url_cpu+route_cpu)
	cpu_sy_json = json.loads(cpu_sy.text)

	route_cpu = 'id'
	cpu_id = requests.get(url_cpu+route_cpu)
	cpu_id_json = json.loads(cpu_id.text)

	route_cpu = 'wa'
	cpu_wa = requests.get(url_cpu+route_cpu)
	cpu_wa_json = json.loads(cpu_wa.text)

	route_cpu = 'st'
	cpu_st = requests.get(url_cpu+route_cpu)
	cpu_st_json = json.loads(cpu_st.text)

	#Obteniendo los datos de la memoria
	url_mem = 'http://localhost:5000/mem/'
	route_mem = 'swpd'
	mem_swpd = requests.get(url_mem+route_mem)
	mem_swpd_json = json.loads(mem_swpd.text)

	route_mem = 'free'
	mem_free = requests.get(url_mem+route_mem)
	mem_free_json = json.loads(mem_free.text)

	route_mem = 'buff'
	mem_buff = requests.get(url_mem+route_mem)
	mem_buff_json = json.loads(mem_buff.text)

	route_mem = 'cache'
	mem_cache = requests.get(url_mem+route_mem)
	mem_cache_json = json.loads(mem_cache.text)

	#Obteniendo los datos del disco duro
	url_disk = 'http://localhost:5000/partition'
	disk_free = requests.get(url_disk)
	disk_free_json = json.loads(disk_free.text)

	#Preparando datos para enviar a la pasarela
	cpu_sources = {'user': cpu_us_json['cpu us'],
			       'system': cpu_sy_json['cpu sy'],
			       'idle': cpu_id_json['cpu id'],
			       'waiting': cpu_wa_json['cpu wa'],
			       'time stolen by virtual machines': cpu_st_json['cpu st'],
			       'fecha': fecha}
	mem_sources = {'swpd': mem_swpd_json['mem swpd'],
				   'free': mem_free_json['mem free'],
				   'buff': mem_buff_json['mem buff'],
				   'cache': mem_cache_json['mem cache'],
				   'fecha': fecha}
	disk_resources = {'hdfree': disk_free_json['hdfree '],
						'fecha': fecha}
	all_sources = {'action':'Update Sources',
				   'cpu':cpu_sources,
				   'mem':mem_sources,
				   'disk':disk_resources}
	return all_sources
###############################################################
print doRequest(getSources())
