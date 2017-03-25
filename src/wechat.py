#!/usr/bin/env python3
# coding=utf-8
#
# Author: Archer
# File: wechat.py
# Date: 21/March/2017
# Desc: wechat logic
from wxpy import *


class WechatManager(object):
    slack_manager = None
    bot = None
    msg = None
    sessions = list()   # hold session between hummable and wechat {sid, sender}
    friends = list()
    groups = list()
    mps = list()
    chats = list()


    def __init__(self, slack_manager, receive_msg_handler, session_storage):
        bot = Bot()
        self.bot = bot
        self._prepare_friends(bot)
        self._prepare_groups(bot)
        self._prepare_mps(bot)
        self._parepare_chats(bot)
        self.slack_manager = slack_manager

        @bot.register()
        def receive_msg(msg):
            self.msg = msg
            receive_msg_handler(self.slack_manager, msg, session_storage)

    def _prepare_friends(self, bot):
        self.friends = bot.friends()
        return

    def _prepare_groups(self, bot):
        self.groups = bot.groups()
        return

    def _prepare_mps(self, bot):
        self.mps = bot.mps()
        return

    def _parepare_chats(self, bot):
        self.chats = bot.chats()
        return

    def qr_callback(self, uuid, status, qrcode):
        print(uuid)
        return

    def login_callback(self):
        return

    def logout_callback(self):
        return
