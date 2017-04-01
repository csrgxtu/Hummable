import logging
import asyncio
import os
from hbmqtt.broker import Broker


class MqBroker(object):
	""" message queue broker server """
	def __init__(self):
		formatter = "[%(asctime)s] :: %(levelname)s :: %(name)s :: %(message)s"
		logging.basicConfig(level=logging.INFO, format=formatter)
		asyncio.get_event_loop().run_until_complete(self.broker_coro())
		asyncio.get_event_loop().run_forever()

	@asyncio.coroutine
	def broker_coro(self):
		broker = Broker()
		yield from broker.start()