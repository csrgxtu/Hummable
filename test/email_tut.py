import imaplib, struct, time
import email as Email


class Mail():
	def __init__(self):
		self.user = 'archer.li@shopeemobile.com'
		self.password = 'whatthefuck'
		# self.ser = serial.Serial('/dev/tty.usbmodem621', 9600)
		self.M = imaplib.IMAP4_SSL('imap.gmail.com', '993')
		self.M.login(self.user, self.password)

	def get_emails(self, email_ids):
		data = []
		for e_id in email_ids:
			_, response = self.M.fetch(e_id, '(UID BODY[TEXT])')
			data.append(response[0][1])
		return data

	def get_subjects(self, email_ids):
		subjects = []
		for e_id in email_ids:
			_, response = self.M.fetch(e_id, '(body[header.fields (from)])')
			print(response)
			_, response = self.M.fetch(e_id, '(body[header.fields (subject)])')
			subjects.append(response[0][1][9:])
		return subjects

	def emails_from(self, name):
		'''Search for all mail from name'''
		status, response = self.M.search(None, '(FROM "%s")' % name)
		email_ids = [e_id for e_id in response[0].split()]
		print('Number of emails from %s: %i. IDs: %s' % (name, len(email_ids), email_ids))
		return email_ids

	def checkMail(self):
		self.M.select('INBOX')
		status, response = self.M.status('INBOX', "(UNSEEN)")
		status, email_ids = self.M.search(None, '(UNSEEN)')
		emails = self.get_subjects(email_ids)
		for email in emails:
			print(email)

		# self.unRead = self.M.search(None, '(UNSEEN)')
		# print(self.unRead[0].split())
		# print(self.unRead[1][0].split())
		# # return len(self.unRead[1][0].split())
		# return self.unRead[1][0].split()[-1]

	def sendData(self):
		self.numMessages = self.checkMail()
		# turn the string into packed binary data to send int
		self.ser.write(struct.pack('B', self.numMessages))


email = Mail()

# check for new mail every minute
while 1:
	mid = email.checkMail()
	# result, data = email.M.uid('fetch', mid, '(RFC822)')
	# print(result)
	# # b = Email.message_from_string(data[0][1])
	# b = Email.message_from_bytes(data[0][1])
	# print(b['From'])
	# print(b['Subject'])
	# payloads = b.get_payload()
	# for payload in payloads:
	# 	# print(payload)
	# 	print(payload.get_payload())
	time.sleep(60)