import feedparser
# import requests
import paho.mqtt.client as mqtt
from lib.logger import logger
from conf import settings
from model.message import Message
import json
import asyncio
import aiohttp
import sys


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
			logger.info('new mail')
			# auth = aiohttp.BasicAuth(self.address, self.password)
			response = yield from aiohttp.request('GET', 'https://yahoo.com')
			if response.status == 200:
				logger.info('aiohttp successful')
				body = yield from 																																																																																																																																												response.text()
				logger.info(body)
				logger.info('fuck')
				# rtv = feedparser.parse(response.content)
				# mails = rtv.get('entries')
				# for mail in mails:
				# 	message = Message('gmail', mail.get('author_detail').get('email'), mail.get('author'), None, mail.get('title'))
					# self.mq_pub(json.loads(json.dumps(message, default=lambda o: o.__dict__)))
					# logger.info(json.dumps(message, default=lambda o: o.__dict__))
			else:
				logger.warn('aiohttp failed')
			# # res = requests.get(self.feed_url, auth=(self.address, self.password))
			# logger.info(res.status_code)
			# if res.status_code != 200:
			# 	logger.warn('new_mail' + str(res.status_code))
			# else:
			# 	rtv = feedparser.parse(res.text)
			# 	mails = rtv.get('entries')
			# 	for mail in mails:
			# 		message = Message('gmail', mail.get('author_detail').get('email'), mail.get('author'), None, mail.get('title'))
			# 		self.mq_pub(json.loads(json.dumps(message, default=lambda o: o.__dict__)))
			# 		logger.info(json.dumps(message, default=lambda o: o.__dict__))

			# yield from asyncio.sleep(1)

	def mq_pub(self, msg):
		client = mqtt.Client()
		client.connect(settings.HOST)
		client.publish(settings.Slack_In_Topic, json.dumps(msg))
		client.disconnect()

	@asyncio.coroutine
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
		yield from asyncio.sleep(0)
