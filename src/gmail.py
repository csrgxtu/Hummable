import feedparser
import requests
import paho.mqtt.client as mqtt
from lib.logger import logger
from conf import settings
from model.message import Message
import json
import sys
import time

feed_url = 'https://mail.google.com/gmail/feed/atom'


def mq_pub(msg):
	client = mqtt.Client()
	client.connect(settings.HOST)
	client.publish(settings.Slack_In_Topic, json.dumps(msg))
	client.disconnect()


def new_mail():
	""" get new mail """
	while True:
		logger.info('new mail')
		res = requests.get(feed_url, auth=(settings.Gmail_Address, settings.Gmail_Password))
		if res.status_code != 200:
			logger.warn('new_mail' + str(res.status_code))
		else:
			# logger.info(res.text)
			rtv = feedparser.parse(res.text)
			mails = rtv.get('entries')
			for mail in mails:
				message = Message('gmail', mail.get('author_detail').get('email'), mail.get('author'), None, mail.get('title'))
				logger.info(json.dumps(message, default=lambda o: o.__dict__))
				# mq_pub(json.loads(json.dumps(message, default=lambda o: o.__dict__)))
				logger.info('##### fuck')

		time.sleep(3)

class GmailManager(object):
	""" Gmail client, login and query the new mail """
	feed_url = 'https://mail.google.com/gmail/feed/atom'

	def __init__(self, address, password):
		self.address = address
		self.password = password

	def mq_pub(self, msg):
		client = mqtt.Client()
		client.connect(settings.HOST)
		client.publish(settings.Slack_In_Topic, json.dumps(msg))
		client.disconnect()

	def new_mail(self):
		""" get new mail """
		while True:
			logger.info('new mail')
			res = requests.get(self.feed_url, auth=(self.address, self.password))
			if res.status_code != 200:
				logger.warn('new_mail' + str(res.status_code))
			else:
				# logger.info(res.text)
				rtv = feedparser.parse(res.text)
				mails = rtv.get('entries')
				for mail in mails:
					message = Message('gmail', mail.get('author_detail').get('email'), mail.get('author'), None, mail.get('title'))
					logger.info(json.dumps(message, default=lambda o: o.__dict__))
					self.mq_pub(json.loads(json.dumps(message, default=lambda o: o.__dict__)))
					logger.info('##### fuck')

			time.sleep(3)


	def mq_sub(self):
		try:
			client = mqtt.Client()
			client.on_message = self.send_msg
			client.connect(settings.HOST)
			client.loop_start()
			client.subscribe(settings.Slack_Out_Topic)
		except ConnectionRefusedError as e:
			logger.warn(e)

	def send_msg(self, client, obj, msg):
		# check if wechat msg

		# find the target

		# send it
		sys.stdout.writelines(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
		logger.info(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
