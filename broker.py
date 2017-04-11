from src.mq_broker import MqBroker
import asyncio


def main():
	# start message broker
	broker = MqBroker()
	print("Message Broker started...")

	asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
	main()
