from lib.slack_helper import SlackHelper
import asyncio
from hbmqtt.client import MQTTClient, ClientException, ConnectException
from hbmqtt.mqtt.constants import QOS_1, QOS_2


class SlackManager(object):
	""" manager that invoke slack_helper and mqtt client """

	slack_helper = None

	def __init__(self, slack_token):
		self.slack_helper = SlackHelper(slack_token)

	def run(self):
		pass

	@asyncio.coroutine
	def subcriber(self):
		""" subscribe mqtt topic /slack_in, listen for incoming msgs """
		C = MQTTClient()
		yield from C.connect('mqtt://127.0.0.1:1883/')
		yield from C.subscribe([
			('/slack_in', QOS_1),
		])
		try:
			while True:
				message = yield from C.deliver_message()
				packet = message.publish_packet
				print("%d:  %s => %s" % (0, packet.variable_header.topic_name, str(packet.payload.data)))
		except ClientException as ce:
			yield from C.unsubscribe(['/slack_in'])
			yield from C.disconnect()
			print("Client exception: %s" % ce)

	@asyncio.coroutine
	def publisher(self, msg):
		""" publish msg to mqtt topic /slack_out """
		try:
			C = MQTTClient()
			yield from C.connect('mqtt://127.0.0.1:1883/')
			yield from C.publish('/slack_out', bytes(msg, 'utf-8'), qos=0x00)
			yield from C.disconnect()
		except ConnectException as ce:
			asyncio.get_event_loop().stop()