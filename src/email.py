import imaplib


class Email(object):
	"""listening email event"""

	mail = None

	def __init__(self, address, password):
		self.mail = imaplib.IMAP4_SSL('imap.gmail.com')
		self.mail.login(address, password)

	def new_mail_event(self):
		""" check new mail in a loop """
		pass
