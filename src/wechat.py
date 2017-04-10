#!/usr/bin/env python3
# coding=utf-8
#
# Author: Archer
# File: wechat.py
# Date: 21/March/2017
# Desc: wechat logic
from wxpy import *
from hbmqtt.client import MQTTClient, ClientException
from hbmqtt.mqtt.constants import QOS_1
import asyncio
from conf import settings
from lib.logger import logger

class WechatManager(object):
	slack_manager = None
	bot = None
	friends = list()
	groups = list()
	mps = list()

	def __init__(self):
		bot = Bot()
		self.bot = bot
		self._prepare_friends(bot)
		self._prepare_groups(bot)
		self._prepare_mps(bot)

		# listen slack out topic, get msg and send 2 wechat
		asyncio.async(self.mq_sub())

		# get wechat msg and send to slack in topic
		@bot.register()
		def receive_msg(msg):
			print("msg: " + msg.text)

	@asyncio.coroutine
	def mq_pub(self, msg):
		conn = MQTTClient()
		yield from conn.connect(settings.MQTT_URL)
		tasks = [
			asyncio.async(conn.publish(settings.Slack_In_Topic, msg.encode()))
		]
		yield from asyncio.wait(tasks)
		yield from conn.disconnect()

	@asyncio.coroutine
	def mq_sub(self):
		conn = MQTTClient()
		yield from conn.connect(settings.MQTT_URL)
		yield from conn.subscribe([
			(settings.Slack_Out_Topic, QOS_1)
		])
		try:
			while True:
				message = yield from conn.deliver_message()
				packet = message.publish_packet
				# print(packet.payload.data.decode())
				self.send_msg(packet.payload.data.decode())
			# yield from conn.unsubscribe([settings.Slack_Out_Topic])
			# yield from conn.disconnect()
		except ClientException as ce:
			print(ce)

	@asyncio.coroutine
	def send_msg(self, msg):
		# check if wechat msg

		# find the target

		# send it
		logger.debug(msg)

	def _prepare_friends(self, bot):
		self.friends = bot.friends()
		return

	def _prepare_groups(self, bot):
		self.groups = bot.groups()
		return

	def _prepare_mps(self, bot):
		self.mps = bot.mps()
		return
