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
from lib.session_storage import SessionStorage
import time


class WechatManager(object):
	slack_manager = None
	bot = None
	friends = None
	groups = list()
	mps = list()

	def __init__(self):
		pass

	def new_msg(self):
		bot = Bot()
		self.bot = bot
		self.prepare_wechat_sessions(bot)

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
		if message.get('type') == 'wechat':
			session_storage = SessionStorage(settings.Wechat_Sessions_File)
			wechat_sessions = session_storage.read()

			# find the target object
			logger.debug(wechat_sessions.get('friends'))
			for friend in wechat_sessions.get('friends'):
				if friend.wxid == message.get('dest'):
					friend.send(message.get('content'))
					# return

			logger.debug(wechat_sessions.get('groups'))
			for group in wechat_sessions.get('groups'):
				logger.debug(group.wxid)
				if group.wxid == message.get('dest'):
					group.send(message.get('content'))
					logger.debug('send msg')
					# return

		logger.warn(message.get('dest') + ' not found in wechat')
		# return

	def prepare_wechat_sessions(self, bot):
		friends = self._prepare_friends(bot)
		groups = self._prepare_groups(bot)
		mps = self._prepare_mps(bot)
		wechat_sessions = dict(friends=friends, groups=groups, mps=mps)
		try:
			session_storage = SessionStorage(settings.Wechat_Sessions_File)
			session_storage.write(wechat_sessions)
			return True
		except Exception as e:
			logger.error(e)
			return False

	def _prepare_friends(self, bot):
		return bot.friends()

	def _prepare_groups(self, bot):
		return bot.groups()

	def _prepare_mps(self, bot):
		return bot.mps()
