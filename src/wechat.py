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
		pass

	def new_msg(self):
		bot = Bot()
		self.bot = bot
		self._prepare_friends(bot)
		self._prepare_groups(bot)
		self._prepare_mps(bot)

		@bot.register()
		def recv_msg(msg):
			message = Message('wechat', msg.sender.wxid, msg.sender.name, None, msg.text)
			logger.debug(json.dumps(message, default=lambda o: o.__dict__))
			self.mq_pub(json.loads(json.dumps(message, default=lambda o: o.__dict__)))

		bot.join()

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
		message = json.loads(msg.payload.decode("utf-8"))
		logger.debug(message)
		if message.get('type') != 'wechat':
			return

		# find the target object
		for friend in self.friends:
			if friend.wxid == message.get('dest'):
				friend.send(message.get('content'))
				return

		for group in self.groups:
			if group.wxid == message.get('dest'):
				group.send(message.get('content'))
				return

		logger.warn(message.get('dest') + ' not found in wechat')
		return

	def _prepare_friends(self, bot):
		logger.debug('_prepare_friends')
		self.friends = bot.friends()
		logger.debug('what the fuck')
		return

	def _prepare_groups(self, bot):
		self.groups = bot.groups()
		return

	def _prepare_mps(self, bot):
		self.mps = bot.mps()
		return
