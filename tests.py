import requests
import base64
import unittest
from database import db

admin = "http://localhost:3002/admin/"
user = "http://localhost:3003/user"

class Testing(unittest.TestCase):
	
	def tearDown(self):
		"""Clears the DB after every test to ensure independance"""
		db.clear()
	
	def setUpForUserTests(self):
		"""Set up procedure to add every song to the DB"""
		songs = [("Blinding Lights", "The Weeknd"), ("Don't Look Back In Anger","Oasis"), ("Everybody (Backstreet's Back) (Radio Edit)","Backstreet Boys"), ("good 4 u","Olivia Rodrigo")]

		for title, artist in songs:
			f = open(f"./wavs/{title}.wav","rb")
			wav = f.read()
			f.close()

			song_file = base64.b64encode(wav).decode("ascii")

			js	 = {"song_file": song_file,"title":title,"artist":artist}
			requests.post(admin+"songs", json=js)

	###################################
	###### Story 1 - Happy Tests ######
	###################################
	def test_add_song_happy_1(self):
		"""Testing of adding 'Blinding Lights' """
		f = open("./wavs/Blinding Lights.wav","rb")
		wav = f.read()
		f.close()

		song_file = base64.b64encode(wav).decode("ascii")

		js = {"song_file": song_file, "title": "Blinding Lights" ,"artist": "The Weeknd"}
		rsp	= requests.post(admin+"songs",json=js)

		self.assertEqual(rsp.status_code,201)
		self.assertEqual(rsp.json()['id'], "Blinding Lights -/- The Weeknd")
		self.assertEqual(rsp.json()['message'], "Song added successfully")

	def test_add_song_happy_2(self):
		"""Testing of adding the same song twice"""
		f = open("./wavs/Blinding Lights.wav","rb")
		wav = f.read()
		f.close()
		song_file = base64.b64encode(wav).decode("ascii")

		js = {"song_file": song_file, "title": "Blinding Lights" ,"artist": "The Weeknd"}
		requests.post(admin+"songs", json=js)

		rsp	= requests.post(admin+"songs", json=js)

		self.assertEqual(rsp.status_code,200)
		self.assertEqual(rsp.json()['id'], "Blinding Lights -/- The Weeknd")
		self.assertEqual(rsp.json()['message'], "Song updated successfully")

	def test_add_song_happy_3(self):
		"""Testing of adding 'Dont Look Back In Anger' """
		f = open("./wavs/Don't Look Back In Anger.wav","rb")
		wav = f.read()
		f.close()

		song_file = base64.b64encode(wav).decode("ascii")

		js = {"song_file": song_file, "title": "Don't Look Back In Anger", "artist": "Oasis"}
		rsp	= requests.post(admin+"songs", json=js)

		self.assertEqual(rsp.status_code,201)
		self.assertEqual(rsp.json()['id'], "Don't Look Back In Anger -/- Oasis")
		self.assertEqual(rsp.json()['message'], "Song added successfully")

	def test_add_song_happy_4(self):
		"""Testing of adding 'Everybody (Backstreets Back) (Radio Edit)' """
		f = open("./wavs/Everybody (Backstreet's Back) (Radio Edit).wav","rb")
		wav = f.read()
		f.close()

		song_file = base64.b64encode(wav).decode("ascii")

		js = {"song_file": song_file, "title":"Everybody (Backstreet's Back) (Radio Edit)", "artist":"Backstreet Boys"}
		rsp	= requests.post(admin+"songs", json=js)

		self.assertEqual(rsp.status_code,201)
		self.assertEqual(rsp.json()['id'], "Everybody (Backstreet's Back) (Radio Edit) -/- Backstreet Boys")
		self.assertEqual(rsp.json()['message'], "Song added successfully")

	def test_add_song_happy_5(self):
		"""Testing of adding 'good 4 u' """
		f = open("./wavs/good 4 u.wav","rb")
		wav = f.read()
		f.close()

		song_file = base64.b64encode(wav).decode("ascii")

		js = {"song_file": song_file, "title":"good 4 u", "artist":"Olivia Rodrigo"}
		rsp	= requests.post(admin+"songs", json=js)

		self.assertEqual(rsp.status_code,201)
		self.assertEqual(rsp.json()['id'], "good 4 u -/- Olivia Rodrigo")
		self.assertEqual(rsp.json()['message'], "Song added successfully")

	#####################################
	###### Story 1 - Unhappy Tests ######
	#####################################
	def test_add_song_unhappy_1(self):
		"""Testing of not providing a title or artist"""
		f = open("./wavs/Blinding Lights.wav","rb")
		wav = f.read()
		f.close()

		song_file = base64.b64encode(wav).decode("ascii")

		js = {"song_file": song_file}
		rsp	= requests.post(admin+"songs", json=js)

		self.assertEqual(rsp.status_code,400)
		self.assertEqual(rsp.json()['error'], "Missing required field: 'artist'")

	def test_add_song_unhappy_2(self):
		"""Testing of not providing an audio file"""
		js	 = {"song_file": None, "title":"Bad request", "artist":"10x dev"}
		rsp	=requests.post(admin+"songs", json=js)

		self.assertEqual(rsp.status_code,400)
		self.assertEqual(rsp.json()['error'], "Field may not be none: 'song_file'")

	def test_add_song_unhappy_3(self):
		"""Testing of providing empty JSON """
		rsp	= requests.post(admin+"songs", json={})

		self.assertEqual(rsp.status_code,400)
		self.assertEqual(rsp.json()['error'], "Invalid JSON format or empty request body")
	
	###################################
	###### Story 2 - Happy Tests ######
	###################################
	def test_remove_song_happy_1(self):
		"""Attempting to remove 'Blinding Lights'"""
		f = open("./wavs/Blinding Lights.wav","rb")
		wav = f.read()
		f.close()

		song_file = base64.b64encode(wav).decode("ascii")
		title = "Blinding Lights"
		artist = "The Weeknd"

		js	 = {"song_file": song_file, "title": title, "artist":artist}
		requests.post(admin+"songs", json=js)

		js	 = {"title":title, "artist": artist}
		rsp	= requests.delete(admin+"songs", json=js)

		self.assertEqual(rsp.status_code,204)

	def test_remove_song_happy_2(self):
		"""Attempting to remove 'Dont Look Back In Anger' - from its title and artist"""
		f = open("./wavs/Don't Look Back In Anger.wav","rb")
		wav = f.read()
		f.close()

		song_file = base64.b64encode(wav).decode("ascii")
		title = "Don't Look Back In Anger"
		artist = "Oasis"

		js	 = {"song_file": song_file, "title":title, "artist":artist}
		requests.post(admin+"songs", json=js)

		js	 = {"title":title, "artist": artist}
		rsp	= requests.delete(admin+"songs", json=js)

		self.assertEqual(rsp.status_code,204)

	def test_remove_song_happy_3(self):
		"""Attempting to remove 'Everybody (Backstreets Back) (Radio Edit)' - from its title and artist"""
		f = open("./wavs/Everybody (Backstreet's Back) (Radio Edit).wav","rb")
		wav = f.read()
		f.close()

		song_file = base64.b64encode(wav).decode("ascii")
		title = "Everybody (Backstreet's Back) (Radio Edit)"
		artist = "Backstreet Boys"

		js	 = {"song_file": song_file, "title":title, "artist":artist}
		requests.post(admin+"songs", json=js)

		js	 = {"title":title, "artist": artist}
		rsp	= requests.delete(admin+"songs", json=js)

		self.assertEqual(rsp.status_code,204)

	def test_remove_song_happy_4(self):
		"""Attempting to remove 'good 4 u' - from its title and artist"""
		f = open("./wavs/good 4 u.wav","rb")
		wav = f.read()
		f.close()

		song_file = base64.b64encode(wav).decode("ascii")
		title = "good 4 u (Extended Mix)"
		artist = "Olivia Rodrigo"

		js	 = {"song_file": song_file, "title":title, "artist":artist}
		requests.post(admin+"songs", json=js)

		js	 = {"title":title, "artist": artist}
		rsp	= requests.delete(admin+"songs", json=js)

		self.assertEqual(rsp.status_code,204)

	#####################################
	###### Story 2 - Unhappy Tests ######
	#####################################
	def test_remove_song_unhappy_1(self):
		"""Testing attempt to remove song that is not in the DB"""
		f = open("./wavs/Blinding Lights.wav","rb")
		wav = f.read()
		f.close()

		song_file = base64.b64encode(wav).decode("ascii")
		adding_title = "Blinding Lights"
		adding_artist = "The Weeknd"

		js	 = {"song_file": song_file, "title":adding_title, "artist":adding_artist}
		requests.post(admin+"songs", json=js)

		title = "Lights of Acceptable Brightness"
		artist = "The Weekday"

		js	 = {"title":title, "artist": artist}
		rsp	= requests.delete(admin+"songs", json=js)

		self.assertEqual(rsp.status_code,404)
		self.assertEqual(rsp.json()['error'], "Song not found in database - check title and artist correct")

	def test_remove_song_unhappy_2(self):
		"""Testing attempt to remove song but giving 'None' instead of name"""
		js	 = {"title":None, "artist": None}
		rsp	= requests.delete(admin+"songs", json=js)

		self.assertEqual(rsp.status_code,400)
		self.assertEqual(rsp.json()['error'], "Both 'title' and 'artist' fields must be provided and not None")
	
	###################################
	###### Story 3 - Happy Tests ######
	###################################
	def test_get_all_songs_happy_1(self):
		"""Testing when there is one song in DB"""
		f = open("./wavs/Blinding Lights.wav","rb")
		wav = f.read()
		f.close()

		song_file = base64.b64encode(wav).decode("ascii")
		title = "Blinding Lights"
		artist = "The Weeknd"

		js	 = {"song_file": song_file, "title": title, "artist":artist}
		requests.post(admin+"songs", json=js)

		rsp	= requests.get(admin+"songs")

		self.assertEqual(rsp.status_code,200)
		self.assertEqual(len(rsp.json()['songs']), 1)
		self.assertEqual(rsp.json()['songs'], [["Blinding Lights", "The Weeknd"]])

	def test_get_all_songs_happy_2(self):
		"""Testing when there are no songs to get"""
		rsp	= requests.get(admin+"songs")

		self.assertEqual(rsp.status_code,200)
		self.assertEqual(len(rsp.json()['songs']), 0)
		self.assertEqual(rsp.json()['songs'], [])

	def test_get_all_songs_happy_3(self):
		"""Testing when all songs are in the DB"""
		self.setUpForUserTests()
		rsp	= requests.get(admin+"songs")

		expected = [["Blinding Lights", "The Weeknd"], ["Don't Look Back In Anger","Oasis"], ["Everybody (Backstreet's Back) (Radio Edit)","Backstreet Boys"], ["good 4 u","Olivia Rodrigo"]]
		expected = sorted(expected, key=lambda x: x[1])

		self.assertEqual(rsp.status_code,200)
		self.assertEqual(len(rsp.json()['songs']), 4)
		self.assertEqual(rsp.json()['songs'], expected)


	####################################################
	###### Story 3 - No Appropriate Unhappy Tests ######
	####################################################

	###################################
	###### Story 4 - Happy Tests ######
	###################################
	def test_user_happy_1(self):
		"""Testing the user getting the segment of 'Blinding Lights' """
		self.setUpForUserTests()

		f = open("./wavs/~Blinding Lights.wav","rb")
		wav = f.read()
		f.close()

		song_file = base64.b64encode(wav).decode("ascii")

		js = {"fragment": song_file}
		rsp	= requests.post(user, json=js)

		song = rsp.json()['song']
		wav = base64.b64decode(song)
		
		f = open("./wavs/Blinding Lights.wav","rb")
		expected_wav = f.read()
		f.close()

		self.assertEqual(expected_wav, wav)
		self.assertEqual(rsp.status_code,200)

	def test_user_happy_2(self):
		"""Testing the user getting the segment of 'Dont Look Back In Anger' """
		self.setUpForUserTests()

		f = open("./wavs/~Don't Look Back In Anger.wav","rb")
		wav = f.read()
		f.close()

		song_file = base64.b64encode(wav).decode("ascii")

		js = {"fragment": song_file}
		rsp	= requests.post(user, json=js)

		song = rsp.json()['song']
		wav = base64.b64decode(song)

		f = open("./wavs/Don't Look Back In Anger.wav","rb")
		expected_wav = f.read()
		f.close()

		self.assertEqual(expected_wav, wav)
		self.assertEqual(rsp.status_code,200)
	
	def test_user_happy_3(self):
		"""Testing the user getting the segment of 'Everybody (Backstreets Back) (Radio Edit)' """
		self.setUpForUserTests()

		f = open("./wavs/~Everybody (Backstreet's Back) (Radio Edit).wav","rb")
		wav = f.read()
		f.close()

		song_file = base64.b64encode(wav).decode("ascii")

		js	 = {"fragment": song_file}
		rsp	= requests.post(user, json=js)

		song = rsp.json()['song']
		wav = base64.b64decode(song)

		f = open("./wavs/Everybody (Backstreet's Back) (Radio Edit).wav","rb")
		expected_wav = f.read()
		f.close()

		self.assertEqual(expected_wav, wav)
		self.assertEqual(rsp.status_code,200)

	def test_user_happy_4(self):
		"""Testing the user getting the segment of 'good 4 u' """
		self.setUpForUserTests()

		f = open("./wavs/~good 4 u.wav","rb")
		wav = f.read()
		f.close()

		song_file = base64.b64encode(wav).decode("ascii")

		js	 = {"fragment": song_file}
		rsp	= requests.post(user, json=js)

		song = rsp.json()['song']
		wav = base64.b64decode(song)

		f = open("./wavs/good 4 u.wav","rb")
		expected_wav = f.read()
		f.close()

		self.assertEqual(expected_wav, wav)
		self.assertEqual(rsp.status_code,200)
	
	#####################################
	###### Story 4 - Unhappy Tests ######
	#####################################
	def test_user_unhappy_1(self):
		"""Testing with a fragment that is not in the DB"""
		f = open("./wavs/~Blinding Lights.wav","rb")
		wav = f.read()
		f.close()

		song_file = base64.b64encode(wav).decode("ascii")

		js	 = {"fragment": song_file}
		rsp	= requests.post(user, json=js)

		self.assertEqual(rsp.status_code,404)
		self.assertEqual(rsp.json()['error'], "Song not found in database")
		self.assertEqual(rsp.json()['song_info'], {"title":"Blinding Lights", "artist":"The Weeknd"})

	def test_user_unhappy_2(self):
		"""Testing with a fragment that isnt a song file"""

		js	 = {"fragment": "abcd"}
		rsp	= requests.post(user, json=js)

		self.assertEqual(rsp.status_code,400)
		self.assertEqual(rsp.json()['error'], "Audio file couldnt be decoded")

	def test_user_unhappy_3(self):
		"""Testing with 'Davos' fragment"""
		f = open("./wavs/~Davos.wav","rb")
		wav = f.read()
		f.close()

		song_file = base64.b64encode(wav).decode("ascii")
		 
		js	 = {"fragment": song_file}
		rsp	= requests.post(user, json=js)

		self.assertEqual(rsp.status_code,404)
		self.assertEqual(rsp.json()['error'], "Song not found external in database")