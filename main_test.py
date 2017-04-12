from src.gmail import GmailManager
from conf import settings


g = GmailManager(settings.Gmail_Address, settings.Gmail_Password)
g.check_mail()
