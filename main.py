from src.wechat import WechatManager
from src.gmail import new_mail
from lib.logger import logger
from conf import settings
import multiprocessing


def main():
	jobs = []
	# start wechat manager
	# wm = WechatManager()
	# print("wechat manager started")

	# start gmail manager
	jobs.append(multiprocessing.Process(target=new_mail))

	# start slack manager

	for job in jobs:
		job.start()

if __name__ == '__main__':
	main()
