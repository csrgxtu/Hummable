from src.mq_broker import MqBroker
from src.wechat import WechatManager
from src.gmail import GmailManager
from lib.logger import logger
import asyncio
from conf import settings
import multiprocessing


def main():
	# start wechat manager
	# wm = WechatManager()
	# print("wechat manager started")

	# start gmail manager
	gm = GmailManager(settings.Gmail_Address, settings.Gmail_Password)
	asyncio.async(gm.new_mail())
	logger.info('gmail manager started...')
	asyncio.async(gm.mq_sub())
	# gm.mq_sub()
	# p = multiprocessing.Process(target=gm.mq_sub)
	# p.start()
	logger.info('after gm.mq_sub')

	# start slack manager

	asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
	main()
