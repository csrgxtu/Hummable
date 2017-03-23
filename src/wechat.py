#!/usr/bin/env python3
# coding=utf-8
#
# Author: Archer
# File: wechat.py
# Date: 21/March/2017
# Desc: wechat logic
from wxpy import *


class WechatManager(object):
    bot = None
    msg = None


    def __init__(self, receive_msg_handler):
        bot = Bot()
        self.bot = bot
        @bot.register()
        def receive_msg(msg):
            self.msg = msg
            receive_msg_handler(msg)

    def qr_callback(self, uuid, status, qrcode):
        print(uuid)
        return

    def login_callback(self):
        print('login_callback')
        return

    def logout_callback(self):
        print('logout_callback')
        return
