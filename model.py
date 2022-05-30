import mysql.connector as MySQL

class Model(object):
	"""docstring for Model"""
	def __init__(self):
		super(Model, self).__init__()
		try:
			self.sql = MySQL.connect(
			    host="localhost",
			    port=3306,
			    user="local",
			    passwd="localhost",
			    database="happy_pancing"
			    )
		except Exception as e:
			raise e
			print(f'DB Not Found: {e}')
		else:
			self.cursor = self.sql.cursor(buffered=True)
			print('DB Connected')

	def init(self):
		return [self.sql,self.cursor]

	def __del__(self):
		try:
			self.sql.close()
		except Exception as e:
			raise e
			print(e)
			print(f"DB Can't Be Closed: {e}")
		else:
			print('DB Closed')

	def read(*conditions):
		return
