import requests
import os, sys
import base64
from flask import Flask, request

try:
	KEY = os.environ["KEY"]
except:
	print("KEY env variable has not been set - Please export AudD key at cmd line")
	sys.exit(1)

audd_api = 'https://api.audd.io/'

app = Flask(__name__)

@app.route("/audd",methods=["POST"])
def endpoint():
	js = request.get_json()
	if js is None:
		return {"error": "Invalid JSON format or empty request body"},400 # Bad request
	
	if "song_file" not in js:
		return {"error": "JSON provided did not include 'song_file'"},400 # Bad request
	
	try:
		wav = base64.b64decode(js['song_file'])
	except Exception:
		return {"error":"Invalid base64-encoded file"},400 # Bad request

	files = {'file':wav,}
	data = {'api_token':KEY}
	response = requests.post(audd_api, data=data, files=files, timeout=10)

	if response.json()['status'] == 'error':
		if response.json()['error']['error_code'] == 400:
			return {"error":"Audio file too big"},400 # Bad request
		elif response.json()['error']['error_code'] == 300:
			return {"error":"Audio file couldnt be decoded"},400 # Bad request
		
	try:
		song_info = response.json()['result']
	except:
		return {"error":"External service failed"},500 # Internal Server Error
			  
	if song_info:
		return song_info,200 # Success
	else:
		return {"error":"Song not found external in database"},404 # Resource not found


if __name__ == "__main__":
	app.run(host="localhost",port=3001)