import mysql.connector as MySQL

class Model(object):
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
		except MySQL.Error as e:
			raise e
			print(f'DB Not Found: {e}')
		else:
			self.cursor = self.sql.cursor(buffered=True)
			print('DB Connected')

	# def init(self):
		# return [self.sql,self.cursor]

	def __del__(self):
		try:
			self.sql.close()
			print('DB Closed')
		except MySQL.Error as e:
			raise e
			print(f"DB Can't Be Closed: {e}")

	def read(self, table, column='*', condition={'1':'1'}, search_limit=None):
		cursor = self.sql.cursor(buffered=True)
		condition_column = ''
		db_ret = []

		for idx, condition_id in enumerate(condition):
			condition_column += f'{condition_id} = %s'

			if idx < len(condition) - 1:
				condition_column += ' AND '

		condition_value = tuple(condition.values())

		try:
			cursor.execute(f"SELECT {','.join(column)} FROM {table} WHERE {condition_column}", condition_value)
		except MySQL.Error as e:
			print(e)
			return 1

		try:
			if search_limit is None:
				db_ret = cursor.fetchall()
			else:
				db_ret = cursor.fetchmany(search_limit)

			cursor.close()
		except MySQL.Error as e:
			print(e)
			return 1

		return db_ret

	def insert(self, table, new_value):
		cursor = self.sql.cursor(buffered=True)

		parameterized_holder = []
		insert_column = []
		insert_value = tuple(new_value.values())

		for idx, key in enumerate(new_value):
			insert_column.append(key)
			parameterized_holder.append(f'%s')

		try:
			cursor.execute(f"INSERT INTO {table} ({','.join(insert_column)}) VALUES ({','.join(parameterized_holder)})",insert_value)
		except MySQL.Error as e:
			print(e)
			return e
			
		try:
			self.sql.commit()
			cursor.close()
		except MySQL.Error as e:
			print(e)
			return e
			
		return 0

	def update(self, table, update, condition):
		cursor = self.sql.cursor(buffered=True)
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

		try:
			cursor.execute(f"UPDATE {table} SET {update_column} WHERE {condition_column}", query_value)
		except MySQL.Error as e:
			print(e)
			return e
			
		try:
			self.sql.commit()
			print(cursor.statement)
			cursor.close()
		except MySQL.Error as e:
			print(e)
			return e
		
		return 0

	def delete(self, table, condition={'1':'1'}):
		cursor = self.sql.cursor(buffered=True)
		condition_column = ''
		db_ret = []

		for idx, condition_id in enumerate(condition):
			condition_column += f'{condition_id} = %s'

			if idx < len(condition) - 1:
				condition_column += ' AND '

		condition_value = tuple(condition.values())

		try:
			cursor.execute(f"DELETE FROM {table} WHERE {condition_column}", condition_value)
		except MySQL.Error as e:
			print(e)
			return 1

		try:
			self.sql.commit()
			print(cursor.statement)
			cursor.close()
		except MySQL.Error as e:
			print(e)
			return 1

		return 0
