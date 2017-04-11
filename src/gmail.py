import feedparser
import requests
import paho.mqtt.client as mqtt
from lib.logger import logger
from conf import settings
from model.message import Message
import json
import time
import asyncio


class GmailManager(object):
	""" Gmail client, login and query the new mail """
	feed_url = 'https://mail.google.com/gmail/feed/atom'

	def __init__(self, address, password):
		self.address = address
		self.password = password

	@asyncio.coroutine
	def new_mail(self):
		""" get new mail """
		while True:
			res = requests.get(self.feed_url, auth=(self.address, self.password))
			if res.status_code != 200:
				pass
			else:
				rtv = feedparser.parse(res.text)
				mails = rtv.get('entries')
				for mail in mails:
					message = Message('gmail', mail.get('author_detail').get('email'), mail.get('author'), None, mail.get('title'))
					self.mq_pub(json.loads(json.dumps(message, default=lambda o: o.__dict__)))
					logger.info(json.dumps(message, default=lambda o: o.__dict__))

			time.sleep(128)

	def mq_pub(self, msg):
		client = mqtt.Client()
		client.connect(settings.HOST)
		client.publish(settings.Slack_In_Topic, json.dumps(msg))
		client.disconnect()

	def mq_sub(self):
		logger.info('###### in mq_sub')
		try:
			client = mqtt.Client()
			client.on_message = self.send_msg
			client.connect(settings.HOST)
			client.subscribe(settings.Slack_Out_Topic)
			logger.info('mq_usb ok')
			client.loop_forever()
		except ConnectionRefusedError as e:
			logger.warn(e)

	def send_msg(self, client, obj, msg):
		# check if wechat msg

		# find the target

		# send it
		logger.info(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))