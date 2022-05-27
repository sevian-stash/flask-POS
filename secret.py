import bcrypt as crypt

class Secret(object):
	"""docstring for Secret"""
	def __init__(self):
		super(Secret, self).__init__()

	def hash_password(password):
		salt = crypt.gensalt(14)
		hashed_pw = crypt.hashpw(password.encode('utf-8'), salt)

		return hashed_pw.decode();

	def check_password(password, hashed_pw):
		return crypt.checkpw(password.encode('utf-8'), hashed_pw.encode('utf-8'))
