import requests
from flask import Flask, request
from database import db
from utils import make_pk

audd = 'http://localhost:3001/audd'

app = Flask(__name__)

@app.route("/user", methods=["POST"])
def s4():
	js = request.get_json()
	if js is None:
		return {"error": "Invalid JSON format or empty request body"},400 # Bad Request
	
	if "fragment" not in js:
		return {"error": "Missing required field: 'fragment'"},400 # Bad Request
	
	song_file = js['fragment']
	audd_result = requests.post(audd, json={"song_file":song_file})
	
	if audd_result.status_code != 200:
		return audd_result.json(),audd_result.status_code # Rethrow error and status code if API fails
		
	song_info = audd_result.json()

	if not song_info:
		return {"error": "Failed to retrieve song info"},500 # Internal Server Error
	
	title = song_info['title']
	artist = song_info['artist']
	pk = make_pk(title, artist)

	data = db.lookup(pk)
	if data:
		song_file = data["song_file"]
		return {'song':song_file,'title':title,'artist':artist},200 # OK
	else:
		return {"error":"Song not found in database", "song_info":{"title":title,"artist":artist}},404 # Content not found

if __name__ == "__main__":
	app.run(host="localhost",port=3003)