import multiprocessing
from task import task

def main():
	p = multiprocessing.Process(target=task)
	p.start()

if __name__ == '__main__':
	main()