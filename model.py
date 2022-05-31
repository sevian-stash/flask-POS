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
			print(f"DB Can't Be Closed: {e}")
		else:
			print('DB Closed')

	def read(self, table, column='*', condition={'1':'1'}, search_limit=None):
		condition_column = ''
		db_ret = None

		for idx, condition_id in enumerate(condition):
			condition_column += f'{condition_id} = %s'

			if idx < len(condition) - 1:
				condition_column += ' AND '

		condition_value = tuple(condition.values())

		self.cursor.execute(f"SELECT {','.join(column)} FROM {table} WHERE {condition_column}", condition_value)

		if search_limit is None:
			db_ret = self.cursor.fetchall()
		else:
			db_ret = self.cursor.fetchmany(search_limit)

		return db_ret

	def update(self, table, update, condition={'True':'True'}):
		db_ret = None
		condition_column = ''
		update_column = ''

		# Spread Values from Array into Tuple
		(*temp_unpacked,) = update.values()
		query_value = temp_unpacked

		(*temp_unpacked,) = condition.values()
		query_value += temp_unpacked

		query_value = tuple(query_value)

		# Concat with Proper Spacing
		for idx, update_id in enumerate(update):
			update_column += f'{update_id} = %s'

			if idx < len(update) - 1:
				update_column += ', '


		for idx, condition_id in enumerate(condition):
			condition_column += f'{condition_id} = %s'

			if idx < len(condition) - 1:
				condition_column += ' AND '

		self.cursor.execute(f"UPDATE {table} SET {update_column} WHERE {condition_column}", query_value)

		return True