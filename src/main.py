#!/usr/bin/env python3
# coding=utf-8
#
# Author: Archer
# File: main.py
# Date: 21/March/2017
# Desc: entrance
from configparser import SafeConfigParser
from slack import SlackManager
from wechat import WechatManager
from wxpy import *


def main():
    # get configurations
    parser = SafeConfigParser()
    parser.read('../conf/hummable.ini')
    token = parser.get('slack', 'token')

    # client
    slack_client = SlackManager(token)
    print(slack_client.api_test())

    # wechat
    wecaht_client = WechatManager()
    @bot.register()
    def incoming_msg(msg):
        print(msg)


if __name__ == '__main__':
    main()
