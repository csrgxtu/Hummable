import asyncio
from lib.logger import logger


@asyncio.coroutine
def task1():
	while True:
		logger.info('what the task1')
		yield from asyncio.sleep(3)


@asyncio.coroutine
def task2():
	while True:
		logger.info('what the task2')
		yield from asyncio.sleep(3)


def main():
	tasks = []
	loop = asyncio.get_event_loop()

	tasks.append(asyncio.async(task1()))
	tasks.append(asyncio.async(task2()))

	loop.run_until_complete(asyncio.wait(tasks))

if __name__ == '__main__':
	main()
