from lib.slack_helper import SlackHelper


class SlackManager(object):
	""" manager that invoke slack_helper and mqtt client """

	slack_helper = None

	def __init__(self, slack_token):
		self.slack_helper = SlackHelper(slack_token)

	def run(self):
		pass