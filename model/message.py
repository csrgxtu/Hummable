
class Message(object):
	type = None
	src = None
	src_name = None
	dest = None
	content = None

	def __init__(self, type, src_id, src_name, dest, content):
		self.type = type
		self.src_id = src_id
		self.src_name = src_name
		self.dest = dest
		self.content = content

