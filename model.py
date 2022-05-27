import mysql.connector as MySQL

class Model(object):
	"""docstring for Model"""
	def __init__(self):
		super(Model, self).__init__()
		self.sql = MySQL.connect(
		    host="localhost",
		    port=3306,
		    user="local",
		    passwd="localhost",
		    database="happy_pancing"
		    )
		self.cursor = self.sql.cursor(buffered=True)
		print('DB Connected')

	def init(self):
		return [self.sql,self.cursor]

	def __del__(self):
		self.sql.close()
		print('DB Closed')

	def read(*conditions):
		return
