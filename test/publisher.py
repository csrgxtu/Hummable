import logging
import asyncio

from hbmqtt.client import MQTTClient
from hbmqtt.mqtt.constants import QOS_1, QOS_2, QOS_0


@asyncio.coroutine
def test_coro():
    C = MQTTClient()
    yield from C.connect('mqtt://127.0.0.1:1883/')
    tasks = [
        asyncio.ensure_future(C.publish('/slack_in', b'TEST MESSAGE WITH QOS_0')),
        asyncio.ensure_future(C.publish('/slack_in', b'TEST MESSAGE WITH QOS_1', qos=QOS_1)),
        asyncio.ensure_future(C.publish('/slack_in', b'TEST MESSAGE WITH QOS_2', qos=QOS_2)),
    ]
    yield from asyncio.wait(tasks)
    print("messages published")
    yield from C.disconnect()


@asyncio.coroutine
def test_coro2():
    try:
        C = MQTTClient()
        ret = yield from C.connect('mqtt://127.0.0.1:1883/')
        message = yield from C.publish('/slack_in', b'TEST MESSAGE WITH QOS_0', qos=QOS_0)
        message = yield from C.publish('/slack_in', b'TEST MESSAGE WITH QOS_1', qos=QOS_1)
        message = yield from C.publish('/slack_in', b'TEST MESSAGE WITH QOS_2', qos=QOS_2)
        #print(message)
        print("messages published")
        yield from C.disconnect()
    except Exception as e:
        # logger.error("Connection failed: %s")
        print(e)
        asyncio.get_event_loop().stop()


def publisher():
	C = MQTTClient()
	ret = C.connect('mqtt://127.0.0.1:1883/')
	message = C.publish('/slack_in', b'TEST MESSAGE WITH QOS_0', qos=QOS_0)
	message = C.publish('/slack_in', b'TEST MESSAGE WITH QOS_1', qos=QOS_1)
	message = C.publish('/slack_in', b'TEST MESSAGE WITH QOS_2', qos=QOS_2)
	print(message)
	print("messages published")
	C.disconnect()

if __name__ == '__main__':
	# formatter = "[%(asctime)s] %(name)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
	# logging.basicConfig(level=logging.DEBUG, format=formatter)
	asyncio.get_event_loop().run_until_complete(test_coro())
	# asyncio.get_event_loop().run_until_complete(test_coro2())
	# publisher()
