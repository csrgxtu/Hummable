from src.wechat import WechatManager
from src.gmail import GmailManager
from lib.logger import logger
from conf import settings
import multiprocessing


def main():
	jobs = []
	# start wechat manager
	# wm = WechatManager()
	# print("wechat manager started")

	# start gmail manager
	gm = GmailManager(settings.Gmail_Address, settings.Gmail_Password)
	jobs.append(multiprocessing.Process(target=gm.new_mail))
	jobs.append(multiprocessing.Process(target=gm.mq_sub))

	# start slack manager

	for job in jobs:
		job.start()

if __name__ == '__main__':
	main()
