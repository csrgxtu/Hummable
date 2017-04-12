# coding=utf-8
#
# Author: Archer
# File: slack.py
# Desc: slack logic
# Date: 21/March/2017
from slackclient import SlackClient
import requests
import time
import json


class SlackHelper(object):
    api_prefix = 'https://slack.com/api/'
    token = None
    slack_client = None
    rtm = None

    def __init__(self, token):
        self.token = token

    def create_rtm_client(self, send_msg_handler, sessions, slack_manager):
        self.rtm_client = SlackClient(self.token)
        if self.rtm_client.rtm_connect():
            # to do
            while True:
                try:
                    rtv = self.rtm_client.rtm_read()
                    if len(rtv) != 0:
                        if not rtv[0].get('subtype') and rtv[0].get(
                        'type') == 'message':
                            print(rtv[0])
                            send_msg_handler(rtv[0].get('text'),
                            rtv[0].get('channel'), sessions,
                            slack_manager)

                    time.sleep(1)
                except:
                    time.sleep(5)
                    rtv = self.rtm_client.rtm_connect()

        else:
            # warning here
            return False

    # test the slack client connection
    # return dict about your token
    def api_test(self):
        rtv = self.slack_client.api_call('api.test')
        return rtv

    # test auth of this token info
    # return dict
    def auth_test(self):
        rtv = self.slack_client.api_call('auth.test')
        return rtv

    # open or create a slack group, return group id
    def open_private_group(self, name):
        """ open or create a private group """
        rtv = self.create_private_group(name)
        if rtv:
            return rtv
        # rtv = self._unarchive_private_group()
        # first, check if identity_id and name already exists in
        # for session in sessions:
        #     if session.get('wxid') == wxid or (
        #             session.get('slack_group') and
        #             session.get('slack_group').get('name') == name.lower()):
        #         # open it
        #         if session.get('slack_group') and session.get(
        #                 'slack_group').get('is_archived') == True:
        #             # open id
        #             if self._unarchive_private_group(
        #                     session.get('slack_group').get('id')):
        #                 return session.get('slack_group').get('id')
        #             else:
        #                 return False
        #         else:
        #             if not session.get('slack_group'):
        #                 break
        #             return session.get('slack_group').get('id')
        # return self.create_private_group(name, sessions)

    def _unarchive_private_group(self, channel_id):
        """ unarchive an private group """
        url = self.api_prefix + 'groups.unarchive'
        data = dict(token=self.token, channel=channel_id)
        body = requests.get(url, params=data)
        print(body.text)
        if body.status_code == 200:
            rtv = json.loads(body.text)
            if rtv.get('ok') is True:
                return True
            elif rtv.get('error') == 'not_archived':
                return True

        return False

    def _open_private_group(self, channel_id):
        """ open an already exist group which is archived or closed, ie is_archived set to True """
        url = self.api_prefix + 'groups.open?token=' + self.token
        data = dict(channel=channel_id)
        body = requests.get(url, params=data)
        if body.status_code == 200:
            rtv = json.loads(body.text)
            if rtv.get('ok') is True:
                return True
            else:
                return False
        else:
            return False

    # create a private group
    # boolean or the group id
    def create_private_group(self, name):
        url = self.api_prefix + 'groups.create?name=' + name + '&token=' + self.token
        body = requests.get(url)
        if body.status_code == 200:
            rtv = json.loads(body.text)
            if rtv.get('ok') is True:
                return rtv.get('group').get('id')
            else:
                return False
        else:
            return False

    # close a private group
    # boolean
    def close_private_group(self, gid):
        url = self.api_prefix + 'groups.close?channel=' + gid + '&token=' + self.token
        body = requests.get(url)
        if body.status_code == 200:
            rtv = json.loads(body.text)
            if rtv.get('ok') is True:
                return True
            else:
                return False
        else:
            return False

    def set_private_sessions(self):
        url = self.api_prefix + 'groups.list?token=' + self.token
        body = requests.get(url)
        if body.status_code == 200:
            rtv = json.loads(body.text)
            if rtv.get('ok') is True:
                sessions = [
                    dict(sid=group.get('id'), slack_group=group)
                    for group in rtv.get('groups')
                ]
                return sessions
            else:
                return False
        else:
            return False

    # archive private group, this will delete the group
    # boolean
    def archive_private_group(self, gid):
        url = self.api_prefix + 'groups.archive?channel=' + gid + '&token=' + self.token
        body = requests.get(url)
        print(body.text)
        if body.status_code == 200:
            try:
                rtv = json.loads(body.text)
                if rtv.get('ok') is True:
                    return True
                else:
                    return False
            except:
                return False
        else:
            return False

    # send msg to a private group
    # return boolean
    def send_msg_to_private_group(self, gid, msg, as_user, username, icon_url):
        data = dict(
            channel=gid,
            text=msg,
            as_user='false',
            username=username,
            icon_url=icon_url,
            token=self.token)
        url = self.api_prefix + 'chat.postMessage'
        body = requests.get(url, params=data)
        if body.status_code == 200:
            rtv = json.loads(body.text)
            if rtv.get('ok') is True:
                return True
            else:
                return False
        else:
            return False
