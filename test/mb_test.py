import logging
import asyncio
from hbmqtt.broker import Broker

config = {
    'listeners': {
        'default': {
            'max-connections': 128,
            'type': 'tcp'
        },
        'my-tcp-1': {
            'bind': '127.0.0.1:1883'
        }
    },
    'timeout-disconnect-delay': 2,
    'auth': {
        'plugins': ['auth.anonymous'],
        'allow-anonymous': True
    }
}
@asyncio.coroutine
def broker_coro():
    broker = Broker(config=config)
    yield from broker.start()


if __name__ == '__main__':
    formatter = "[%(asctime)s] :: %(levelname)s :: %(name)s :: %(message)s"
    logging.basicConfig(level=logging.INFO, format=formatter)
    asyncio.get_event_loop().run_until_complete(broker_coro())
    asyncio.get_event_loop().run_forever()
