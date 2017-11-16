#!/usr/bin/python
from flask import Flask, jsonify, make_response, jsonify, url_for, redirect
import json
import requests
import subprocess

############## Intranet Pasarela #############################
def doRequest():
	url = 'http://lit-anchorage-86748.herokuapp.com/get_tasks'
	headers = {'content-type': 'application/json'}
	response = requests.get(url, headers=headers)
	return response.text
###############################################################


def startDownload():
	tasks_json = json.loads(doRequest())
	tasks =  tasks_json['tasks']
	if len(tasks) > 0:
		for task in tasks:
			start_download = subprocess.check_output(['transmission-remote', '-a', task['link']])
			print start_download

startDownload()