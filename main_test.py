from src.gmail import GmailManager
from conf import settings


g = GmailManager(settings.Gmail_Address, settings.Gmail_Password)
g.new_mail()
