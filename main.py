from src.mq_broker import MqBroker
import asyncio


def main():
	# start message broker
	mq = MqBroker()
	print("Message Broker started...")

	# start wechat manager

	# start slack manager

	asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
	main()
