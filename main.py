from src.mq_broker import MqBroker
from src.wechat import WechatManager
from src.gmail import GmailManager
from lib.logger import logger
import asyncio
import multiprocessing


def main():
	# start wechat manager
	# wm = WechatManager()
	# print("wechat manager started")

	# start gmail manager
	gm = GmailManager('archer.li@shopeemobile.com', 'whatthefuck')
	asyncio.async(gm.new_mail())
	logger.info('gmail manager started...')

	# start slack manager

	asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
	main()
