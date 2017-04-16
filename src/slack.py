from lib.slack_helper import SlackHelper
from conf import settings
from lib.logger import logger
from model.message import Message
import paho.mqtt.client as mqtt
from lib.session_storage import SessionStorage
import json
import time


class SlackManager(object):
	""" manager that invoke slack_helper and mqtt client """
	slack_helper = None

	def __init__(self, slack_token):
		self.slack_helper = SlackHelper(slack_token)

	def new_slack_msg(self):
		rtm_client = self.slack_helper.create_rtm_client()
		if rtm_client.rtm_connect():
			while True:
				try:
					rtv = rtm_client.rtm_read()
					if len(rtv) != 0:
						logger.debug(rtv[0])
						if not rtv[0].get('subtype') and rtv[0].get('type') == 'message':
							# compose a message
							gid = rtv[0].get('channel')
							content = rtv[0].get('text')
							dest, type = self.get_src_id_and_type_from_sessions(gid)
							if dest is False:
								logger.warn('dest is false ' + str(gid))
							message = Message(type, gid, None, dest, content)
							self.mq_pub(json.loads(json.dumps(message, default=lambda o: o.__dict__)))
					time.sleep(1)
				except Exception as e:
					logger.warn(e)
					rtm_client.rtm_connect()
		else:
			logger.error('rtm_client cant connect')

	def mq_pub(self, msg):
		client = mqtt.Client()
		client.connect(settings.HOST)
		client.publish(settings.Slack_Out_Topic, json.dumps(msg))
		client.disconnect()

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
		message = json.loads(msg.payload.decode("utf-8"))
		logger.info(message)

		rtv = self.slack_helper.search_and_open_group(message.get('src_name'))
		if not rtv:
			logger.warn('search_and_open_group failed ' + str(rtv))
			rtv = self.slack_helper.create_private_group(message.get('src_name'))
			if not rtv:
				logger.error('cant create group ' + str(message.get('src_name')))
				# return False
				gid = None
			else:
				gid = rtv
		else:
			gid = rtv

		logger.debug(gid)
		self.set_sessions(dict(gid=gid, src_id=message.get('src_id'), type=message.get('type')))
		rtv = self.slack_helper.send_msg_to_private_group(gid, message.get('content'), None, message.get('src_id'), '')
		if not rtv:
			logger.warn(rtv)
			# return False
		# return True

	def set_sessions(self, session):
		""" session = {gid: '', src_id: '', type: ''} """
		session_storage = SessionStorage(settings.Session_Storage_File)
		sessions = session_storage.read()

		if type(session) is not dict:
			return False

		if not session.get('gid') or not session.get('src_id') or not session.get('type'):
			return False

		for e in sessions:
			if e == session:
				return True

		sessions.append(session)
		session_storage.write(sessions)
		logger.debug('set session: ' + json.dumps(session))
		return True

	def get_src_id_and_type_from_sessions(self, gid):
		""" get source id and type from sessions according to the group id """
		session_storage = SessionStorage(settings.Session_Storage_File)
		sessions = session_storage.read()

		logger.debug('sessions: ' + str(len(sessions)))
		for session in sessions:
			logger.debug(json.dumps(session))
			if session.get('gid') == gid:
				return session.get('src_id'), session.get('type')

		return False, False
