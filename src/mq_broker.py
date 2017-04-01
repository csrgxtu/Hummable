import logging
import asyncio
from hbmqtt.broker import Broker


class MqBroker(object):
	""" message queue broker server """

	config = {
		'listeners': {
			'default': {
				'max-connections': 128,
				'type': 'tcp'
			},
			'my-tcp-1': {
				'bind': '127.0.0.1:1883'
			}
		},
		'timeout-disconnect-delay': 2,
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