from src.wechat import WechatManager
from src.gmail import GmailManager
from lib.logger import logger
import asyncio
from conf import settings


def main():
	tasks = []
	loop = asyncio.get_event_loop()

	# start wechat manager
	# wm = WechatManager()
	# print("wechat manager started")

	# start gmail manager
	gm = GmailManager(settings.Gmail_Address, settings.Gmail_Password)
	tasks.append(asyncio.async(gm.new_mail()))
	# tasks.append(asyncio.async(gm.mq_sub()))

	# start slack manager

	loop.run_until_complete(asyncio.wait(tasks))


if __name__ == '__main__':
	main()
