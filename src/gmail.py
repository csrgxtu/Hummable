import paho.mqtt.client as mqtt
from lib.logger import logger
from conf import settings
import imaplib
from model.message import Message
import json


class GmailManager(object):
	""" Gmail client, login and query the new mail """

	def __init__(self, address, password):
		self.address = address
		self.password = password
		self.M = imaplib.IMAP4_SSL('imap.gmail.com', '993')
		self.M.login(self.address, self.password)

	def get_mail(self, email_ids):
		rtv = []
		for e_id in email_ids:
			try:
				_, response = self.M.fetch(e_id, '(body[header.fields (from)])')
				From = str(response[0][1]).split(' <')[1][0:-10]
				_, response = self.M.fetch(e_id, '(body[header.fields (subject)])')
				Subject = str(response[0][1][9:])[2:-9]
				rtv.append(dict(From=From, Subject=Subject))
			except:
				continue

		return rtv

	def check_mail(self):
		self.M.select('INBOX')
		self.M.status('INBOX', "(UNSEEN)")
		status, email_ids = self.M.search(None, '(UNSEEN)')
		email_ids = str(email_ids[0])[1:].replace("'", "").split(' ')
		rtv = self.get_mail(email_ids)
		for email in rtv:
			print(email.get('From'), email.get('Subject'))
			message = Message('gmail', email.get('From'), email.get('From'), None, email.get('Subject'))
			logger.info('before self.mq_pub')
			self.mq_pub(json.loads(json.dumps(message, default=lambda o: o.__dict__)))
			logger.info('after self.mq_pub')

	def mq_pub(self, msg):
		client = mqtt.Client()
		client.connect(settings.HOST)
		client.publish(settings.Slack_In_Topic, json.dumps(msg))
		client.disconnect()

	def mq_sub(self):
		try:
			client = mqtt.Client()
			client.on_message = self.send_msg
			client.connect(settings.HOST)
			client.subscribe(settings.Slack_Out_Topic)
			client.loop_forever()
		except ConnectionRefusedError as e:
			logger.warn(e)

	def send_msg(self, client, obj, msg):
		# check if wechat msg

		# find the target

		# send it
		logger.info(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
