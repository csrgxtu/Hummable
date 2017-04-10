from src.mq_broker import MqBroker
from src.wechat import WechatManager
import asyncio
import multiprocessing


def main():
	# start message broker
	p = multiprocessing.Process(target=MqBroker)
	p.start()
	# mq = MqBroker()
	print("Message Broker started...")

	# start wechat manager
	# asyncio.async(WechatManager())
	wm = WechatManager()
	print("wechat manager started")

	# start slack manager

	asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
	main()
