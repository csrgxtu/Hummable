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
from wxpy import embed

def main():
    # get configurations
    parser = SafeConfigParser()
    parser.read('../conf/hummable.ini')
    token = parser.get('slack', 'token')

    # client
    slack_manager = SlackManager(token)
    # print(slack_manager.api_test())

    # wechat
    wechat_manager = WechatManager()
    @wechat_manager.bot.register()
    def print_msgs(msg):
        # send to a hard coded group, i.e #passed
        gid = 'G4LQR11LH'
        msg = msg.text
        as_user = 'false'
        user_name = 'wechat'
        icon_url = 'https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_120x44dp.png'
        if slack_manager.send_msg_to_private_group(gid, msg, as_user, user_name, icon_url):
            print('Success')
            print(type(msg))
            print(msg)
            print(msg.sender)
            print(msg.member)
            print(msg.type)
        else:
            print(msg)
            print('Error')

    embed(shell='ipython' banner='Being hummable') #wait infinite, or programme will exit right away


if __name__ == '__main__':
    main()
