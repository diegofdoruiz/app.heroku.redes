#!/usr/bin/python
from flask import Flask, jsonify, make_response, jsonify, url_for, redirect
import json
import requests
import transmissionrpc
import time

############## Intranet Pasarela #############################
def doRequest(resources_json):
	url = 'http://lit-anchorage-86748.herokuapp.com/progress_tasks'
	headers = {'content-type': 'application/json'}
	response = requests.put(url, data=json.dumps(resources_json), headers=headers)
	return response.text
###############################################################


#transmission_user:diego pass:password
def getDownloadsList():
	tc = transmissionrpc.Client('localhost', port=9091)
	array_torrents = tc.get_torrents()
	tasks_status = []
	for torrent in array_torrents:
		progress = str(torrent.percentDone*100)+"%"
		status = torrent.status
		name = torrent.name
		#name = name.replace("+"," ")
		fecha = time.ctime()
		#print torrent.status+" "+torrent.name+" "+str(torrent.percentDone*100)
		task = {'progress':progress,
		    	'status':status,
		    	'name':name,
		    	'fecha': fecha}
		tasks_status.append(task)

	json_send = {'action':'Update Downloads State',
				 'data': tasks_status}
	return json_send

print doRequest(getDownloadsList())
