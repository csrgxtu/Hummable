from conf import settings
import coloredlogs, logging

logger = logging.getLogger('Hummable')
coloredlogs.install(level=settings.DEBUG_LEVEL)