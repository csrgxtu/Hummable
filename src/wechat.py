#!/usr/bin/env python3
# coding=utf-8
#
# Author: Archer
# File: wechat.py
# Date: 21/March/2017
# Desc: wechat logic
from wxpy import *
import paho.mqtt.client as mqtt
import asyncio
from conf import settings
from lib.logger import logger
import json
from model.message import Message
import time


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

		# get wechat msg and send to slack in topic
		@bot.register()
		def receive_msg(msg):
			logger.info("[WechatManager.init.receive_msg]" + msg.text)
			message = Message('wechat', msg.sender.wxid, msg.sender.name, None, msg.text)
			self.mq_pub(json.loads(json.dumps(message, default=lambda o: o.__dict__)))

		logger.info('####init')
		# time.sleep(10)
		# asyncio.async(self.mq_sub())
		self.mq_sub()

	def mq_pub(self, msg):
		client = mqtt.Client()
		client.connect(settings.HOST)
		client.publish(settings.Slack_In_Topic, json.dumps(msg))
		client.disconnect()

	# @asyncio.coroutine
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

	# @asyncio.coroutine
	# def mq_sub(self):
	# 	conn = MQTTClient()
	# 	yield from conn.connect(settings.MQTT_URL)
	# 	yield from conn.subscribe([
	# 		(settings.Slack_Out_Topic, QOS_1)
	# 	])
	# 	try:
	# 		while True:
	# 			message = yield from conn.deliver_message()
	# 			packet = message.publish_packet
	# 			# print(packet.payload.data.decode())
	# 			self.send_msg(packet.payload.data.decode())
	# 			logger.info('[WechatManager.mq_sub]' + packet.payload.data.decode())
	# 		# yield from conn.unsubscribe([settings.Slack_Out_Topic])
	# 		# yield from conn.disconnect()
	# 	except ClientException as ce:
	# 		print(ce)

	# @asyncio.coroutine
	def send_msg(self, client, obj, msg):
		# check if wechat msg

		# find the target

		# send it
		logger.info(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

	def _prepare_friends(self, bot):
		self.friends = bot.friends()
		return

	def _prepare_groups(self, bot):
		self.groups = bot.groups()
		return

	def _prepare_mps(self, bot):
		self.mps = bot.mps()
		return
