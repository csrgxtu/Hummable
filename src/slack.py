# coding=utf-8
#
# Author: Archer
# File: slack.py
# Desc: slack logic
# Date: 21/March/2017
from slackclient import SlackClient

class SlackManager(object):
    token = None
    slack_client = None

    def __init__(self, token):
        self.token = token
        self.slack_client = SlackClient(token)

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
