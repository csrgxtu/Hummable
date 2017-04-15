import pickle
from lib.logger import logger


class SessionStorage(object):
	""" use pickle file as session storage """

	def __init__(self, filename):
		self.filename = filename

	def append(self, data):
		""" append to the pickle file """
		with open(self.filename, 'w+') as file_handler:
			pickle.dump(data, file_handler)

	def write(self, data):
		""" write to the pickle file """
		with open(self.filename, 'wb') as file_handler:
			pickle.dump(data, file_handler)

	def read(self):
		""" load the pickle file """
		try:
			with open(self.filename, 'rb') as file_handler:
				data = pickle.load(file_handler)
				return data
		except Exception as e:
			logger.warn(e)
			return []
