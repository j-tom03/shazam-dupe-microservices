import sqlite3

class Repository:
	def __init__(self,table):
		self.table = table 
		self.database = self.table + ".db" 
		self.make()

	def make(self):
		with sqlite3.connect(self.database) as connection:
			cursor = connection.cursor()
			cursor.execute(
				f"CREATE TABLE IF NOT EXISTS {self.table} " +
				"(pk TEXT PRIMARY KEY, title TEXT, artist TEXT, song_file TEXT)"
			)
			connection.commit()

	def clear(self):
		with sqlite3.connect(self.database) as connection:
			cursor = connection.cursor()
			cursor.execute(
				f"DELETE FROM {self.table}" 
			)
			connection.commit()

	def insert(self,js):
		with sqlite3.connect(self.database) as connection:
			cursor = connection.cursor()
			cursor.execute(
				f"INSERT INTO {self.table} (pk,title,artist,song_file) VALUES (?,?,?,?)",
				(js["title"]+" -/- "+js["artist"],js["title"],js["artist"],js["song_file"])
			)
			connection.commit()
			return cursor.rowcount

	def remove(self,pk):
		with sqlite3.connect(self.database) as connection:
			cursor = connection.cursor()
			cursor.execute(
				f"DELETE FROM {self.table} WHERE pk=?",
				(pk,)
			)
			connection.commit()
			return True
		
	def update(self,js):
		with sqlite3.connect(self.database) as connection:
			cursor = connection.cursor()
			cursor.execute(
				f"UPDATE {self.table} SET title=?, artist=?, song_file=? WHERE pk=?",
				(js["title"],js["artist"],js["song_file"],js["title"]+" -/- "+js["artist"])
			)
			connection.commit()
			return cursor.rowcount

	def lookup(self,pk):
		with sqlite3.connect(self.database) as connection:
			cursor = connection.cursor()
			cursor.execute(
				f"SELECT pk, title, artist, song_file FROM {self.table} WHERE pk=?",
				(pk,)
			)
			row = cursor.fetchone()
			if row:
				return {"pk":row[0],
						"title":row[1],
						"artist":row[2],
						"song_file":row[3],
						}
			else:
				return None
			
	def read_songs(self):
		with sqlite3.connect(self.database) as connection:
			cursor = connection.cursor()
			cursor.execute(
				f"SELECT * FROM {self.table}"
			)
			row = cursor.fetchone()
			songs = []
			while row is not None:
				songs += [[row[1], row[2]]]
				row = cursor.fetchone()

			songs = sorted(songs, key=lambda x: x[1])
			return {"songs": songs}