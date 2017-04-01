from src.mq_broker import MqBroker


def main():
    # start msg queue broker in main process
    mb = MqBroker()

if __name__ == '__main__':
    main()
