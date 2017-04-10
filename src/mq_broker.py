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
			'my-tcp-1': {
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
		asyncio.get_event_loop().run_until_complete(self.broker_coro())
		asyncio.get_event_loop().run_forever()

	@asyncio.coroutine
	def broker_coro(self):
		broker = Broker(config=self.config)
		yield from broker.start()
