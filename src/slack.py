from lib.slack_helper import SlackHelper
import asyncio
from conf import settings
from lib.logger import logger
import paho.mqtt.client as mqtt
import json


class SlackManager(object):
	""" manager that invoke slack_helper and mqtt client """

	slack_helper = None

	def __init__(self, slack_token):
		self.slack_helper = SlackHelper(slack_token)

	def mq_sub(self):
		try:
			client = mqtt.Client()
			client.on_message = self.send_msg
			client.connect(settings.HOST)
			client.subscribe(settings.Slack_In_Topic)
			client.loop_forever()
		except ConnectionRefusedError as e:
			logger.warn(e)

	def send_msg(self, client, obj, msg):
		logger.info(msg.payload.decode("utf-8"))
		message = json.loads(msg.payload.decode("utf-8"))
		logger.info(message)
		rtv = self.slack_helper.open_private_group(message.get('src_name'))
		logger.info(rtv)
		rtv = self.slack_helper.send_msg_to_private_group(rtv, message.get('content'), None, message.get('src_id'), '')
		logger.info(rtv)
		logger.info(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

