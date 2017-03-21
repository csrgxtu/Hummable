# coding=utf-8
#
# Author: Archer
# File: slack.py
# Desc: slack logic
# Date: 21/March/2017
# from slackclient import SlackClient
import requests
import json


class SlackManager(object):
    api_prefix = 'https://slack.com/api/'
    token = None
    slack_client = None

    def __init__(self, token):
        self.token = token
        # self.slack_client = SlackClient(token)

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

    # list private group
    # group ids or boolean
    def list_private_group(self):
        url = self.api_prefix + 'groups.list?token=' + self.token
        body = requests.get(url)
        if body.status_code == 200:
            rtv = json.loads(body.text)
            if rtv.get('ok') is True:
                gids = [group.get('id') for group in rtv.get('groups')]
                return gids
            else:
                return False
        else:
            return False

    # archive private group, this will delete the group
    # boolean
    def archive_private_group(self, gid):
        url = self.api_prefix + 'groups.archive?channel=' + gid + '&token=' + self.token
        body = requests.get(url)
        if body.status_code == 200:
            rtv = json.loads(body.text)
            if rtv.get('ok') is True:
                return True
            else:
                return False
        else:
            return False

    # send msg to a private group
    # return boolean
    def send_msg_to_private_group(self, gid, msg, as_user, user_name):
        url = self.api_prefix + 'chat.postMessage?channel=' + gid + '&text=' + msg + '&as_user=false&user_name=' + user_name + '&token=' + self.token
        print(url)
        body = requests.get(url)
        print(body.text)
        if body.status_code == 200:
            rtv = json.loads(body.text)
            if rtv.get('ok') is True:
                return True
            else:
                return False
        else:
            return False
