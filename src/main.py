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
    WechatSessions = list()

    # client
    def send_msg_handler(msg):
        # split wxid msg
        wxid, text = msg.split(' ', 1)
        # query WechatSessions
        for session in WechatSessions:
            if wxid == session.get('sid'):
                sender = session.get('sender')
                sender.send(text)
    slack_manager = SlackManager(token)

    # wechat
    def receive_msg_handler(msg):
        if msg.sender.wxid not in WechatSessions:
            session = dict(sid=msg.sender.wxid, sender=msg.sender)
            WechatSessions.append(session)

        sender = msg.sender # sender object
        text = msg.text
        msg_type = msg.type
        gid = 'G4LQR11LH'
        as_user = 'false'
        user_name = msg.sender.name + ' -- '+ msg.sender.wxid
        icon_url = 'https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_120x44dp.png'

        if msg_type is not 'Text':
            text = '[' + msg_type + '] msg type to be implemented'

        if slack_manager.send_msg_to_private_group(gid, text, as_user, user_name, icon_url):
            print('send msg from wechat ' + user_name + ' to slack ' + gid)
        else:
            print('error send msg from wechat ' + user_name + ' to slack ' + gid)

    wechat_manager = WechatManager(receive_msg_handler)

    # create slack rtm client
    slack_manager.create_rtm_client(send_msg_handler)

    embed(shell='ipython', banner='Being hummable') #wait infinite, or programme will exit right away


if __name__ == '__main__':
    main()
