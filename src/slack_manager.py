from lib.slack_helper import SlackHelper
import asyncio
from hbmqtt.client import MQTTClient, ClientException, ConnectException
from hbmqtt.mqtt.constants import QOS_1
from conf import settings


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
		yield from C.connect(settings.Slack_Url)
		yield from C.subscribe([
			(settings.Slack_In_Topic, QOS_1),
		])
		try:
			while True:
				message = yield from C.deliver_message()
				packet = message.publish_packet
				print("%d:  %s => %s" % (0, packet.variable_header.topic_name, str(packet.payload.data)))
		except ClientException as ce:
			yield from C.unsubscribe([settings.Slack_In_Topic])
			yield from C.disconnect()
			print("Client exception: %s" % ce)

	@asyncio.coroutine
	def publisher(self, msg):
		""" publish msg to mqtt topic /slack_out """
		try:
			C = MQTTClient()
			yield from C.connect(settings.Slack_Url)
			yield from C.publish(settings.Slack_Out_Topic, bytes(msg, 'utf-8'), qos=0x00)
			yield from C.disconnect()
		except ConnectException as ce:
			asyncio.get_event_loop().stop()