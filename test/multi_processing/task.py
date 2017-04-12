import time
import paho.mqtt.client as mqtt
import json
import requests


def task():
	while True:
		feed_url = 'http://github.com/csrgxtu'
		res = requests.get(feed_url)
		mq_pub(dict(code=res.status_code))
		time.sleep(3)


def task1():
	print("this is task1")


def mq_pub(msg_dict):
	client = mqtt.Client()
	client.connect('127.0.0.1')
	client.publish('/slack_in', json.dumps(msg_dict))
	print(json.dumps(msg_dict))
	client.disconnect()