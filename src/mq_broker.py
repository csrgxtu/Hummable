import logging
import asyncio
from hbmqtt.broker import Broker
from conf import settings

class MqBroker(object):
	""" message queue broker server """

	config = {
		'listeners': {
			'default': {
				'max-connections': settings.MAX_CONNECTIONS,
				'type': 'tcp'
			},
			'hummable': {
				'bind': settings.BIND
			}
		},
		'timeout-disconnect-delay': settings.TIMEOUT_DISCONNECT_DELAY,
		'auth': {
			'plugins': ['auth.anonymous'],
			'allow-anonymous': True
		}
	}

	def __init__(self):
		formatter = "[%(asctime)s] :: %(levelname)s :: %(name)s :: %(message)s"
		logging.basicConfig(level=logging.INFO, format=formatter)
		asyncio.async(self.broker_coro())

	@asyncio.coroutine
	def broker_coro(self):
		broker = Broker(config=self.config)
		yield from broker.start()
