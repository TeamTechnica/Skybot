import sqlite3

class DBHelper:
	def __init__(self, dbname="todo.sqlite"):
		self.dbname = dbname
		self.conn = sqlite3.connect(dbname)

	def setup(self):
		user_table = """CREATE TABLE IF NOT EXISTS 
						users(user_id integer, name text, link text, max_passenger real)"""
		flight_table = """CREATE TABLE IF NOT EXISTS
						flights(passenger_id integer, time text, flight_date text last_day text)"""
		match_table = """CREATE TABLE IF NOT EXISTS
						matches(passenger_id integer, name text, match_id integer)"""
		self.conn.execute(user_table)
		self.conn.execute(flight_table)
		self.conn.execute(match_table)
		self.conn.commit()

	def add_user(self, user_text):
		stmt = "INSERT INTO users (user_id, name, link, max_passenger) VALUES (?)"
		args = (user_text)
		self.conn.execute(stmt, args)
		self.conn.commit()


	def delete_match(self, match_text):
		stmt = "DELETE FROM matches WHERE match_id = (?) "
		args = (match_text)
		self.conn.execute(stmt, args)
		self.conn.commit()
		

	def get_users(self):
		stm = "SELECT * FROM users"
		return [x for x in self.conn.execute(stmt)] 
