from conf import settings
import coloredlogs, logging
import os


logger = logging.getLogger(os.path.basename(__file__))
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
coloredlogs.install(level=settings.DEBUG_LEVEL, logger=logger, fmt=FORMAT)