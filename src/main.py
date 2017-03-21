#!/usr/bin/env python3
# coding=utf-8
#
# Author: Archer
# File: main.py
# Date: 21/March/2017
# Desc: entrance
from slackclient import SlackClient
from configparser import SafeConfigParser


def main():
    # get configurations
    parser = SafeConfigParser()
    parser.read('../conf/hummable.ini')
    token = parser.get('slack', 'token')

    


if __name__ == '__main__':
    main()
