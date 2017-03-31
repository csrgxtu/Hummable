import imaplib


class Gmail(object):
	""" Gmail client, login and query the new mail """

	mail_client = None

	def __init__(self, address, password):
		self.mail = imaplib.IMAP4_SSL('imap.gmail.com')
		self.mail.login(address, password)

	@staticmethod
	def new_mail(self):
		""" get new mail """
		pass