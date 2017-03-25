#!/usr/bin/env python3
# coding=utf-8
#
# Author: Archer
# File: main.py
# Date: 21/March/2017
# Desc: entrance
from configparser import SafeConfigParser
from wxpy import embed
from src.wechat import WechatManager
from src.slack import SlackManager
from lib.slack_handler import *
from lib.wechat_handler import *
from src.session import wx_slack_sessions
import json

def main():
    # get configurations
    parser = SafeConfigParser()
    parser.read('./conf/hummable.ini')
    token = parser.get('slack', 'token')
    # WechatSessions = list()
    # wx_slack_sessions = list()

    slack_manager = SlackManager(token)
    wx_slack_sessions = slack_manager.set_private_sessions()

    wechat_manager = WechatManager(slack_manager, receive_msg_handler, wx_slack_sessions)

    # create slack rtm client
    slack_manager.create_rtm_client(send_msg_handler, wx_slack_sessions)

    embed(shell='ipython', banner='Being hummable') #wait infinite, or programme will exit right away


if __name__ == '__main__':
    main()
