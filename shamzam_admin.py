from flask import Flask, request
from database import db
from utils import make_pk

audd = 'http://localhost:3001/audd'

app = Flask(__name__)

@app.route("/admin/songs",methods=["POST"])
def s1_add_song():
	js = request.get_json()
	if not js:
		return {"error": "Invalid JSON format or empty request body"},400 # Bad request
	
	if "song_file" not in js:
		return {"error": "Missing required field: 'song_file'"},400 # Bad request
	elif "artist" not in js:
		return {"error": "Missing required field: 'artist'"},400 # Bad request
	elif "title" not in js:
		return {"error": "Missing required field: 'title'"},400 # Bad request
	
	song_file = js['song_file']
	artist = js['artist']
	title = js['title']

	if not song_file:
		return {"error": "Field may not be none: 'song_file'"},400 # Bad request
	elif not artist:
		return {"error": "Field may not be none: 'artist'"},400 # Bad request
	elif not title:
		return {"error": "Field may not be none: 'title'"},400 # Bad request
	
	pk = make_pk(title, artist)

	db_js = {'title':title, 'artist':artist, 'song_file':song_file}

	if db.lookup(pk) != None:
		if db.update(db_js):
			return {"message": "Song updated successfully", "id": pk},200 # OK
		else:
			return {"error": "Failed to update song"},500 # Internal Server Error
	else:
		if db.insert(db_js):
			return {"message": "Song added successfully", "id": pk},201 # Resource Created 
		else:
			return {"error": "Failed to insert song"},500 # Internal Server Error


@app.route("/admin/songs", methods=["DELETE"])
def s2_remove_song():
	js = request.get_json()
	if js is None:
		return {"error": "Invalid JSON format or empty request body"},400 # Bad request
	
	if "title" not in js:
		return {"error": "Missing required field: 'title'"},400 # Bad request
	elif "artist" not in js:
		return {"error": "Missing required field: 'artist'"},400 # Bad request
	
	title = js["title"]
	artist = js["artist"]
	
	if not title or not artist:
		return {"error": "Both 'title' and 'artist' fields must be provided and not None"},400 # Bad request
	
	pk = make_pk(title, artist)

	if db.lookup(pk) != None:
		if db.remove(pk):
			return "",204 # Success - nothing to return
		else:
			return {"error":"Failed to remove song from database"},500 # Internal Server Error
	else:
		return {"error":"Song not found in database - check title and artist correct"},404 # Content not found


@app.route("/admin/songs",methods=["GET"])
def s3_list_songs():
	songs = db.read_songs()
	if songs:
		return songs,200 # Successful
	else:
		return {"error":"Failed to access list of song titles"},500 # Internal Server Error

if __name__ == "__main__":
	app.run(host="localhost",port=3002)