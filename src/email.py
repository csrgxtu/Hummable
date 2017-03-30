import imaplib


class Email(object):
	"""listening email event"""
	def __init__(self, address, password):
		mail = imaplib.IMAP4_SSL('imap.gmail.com')
		pass
