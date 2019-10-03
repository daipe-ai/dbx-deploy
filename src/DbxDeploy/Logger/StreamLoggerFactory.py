import logging
import colorlog

class StreamLoggerFactory:

    def create(self, loggerName: str):
        logger = logging.getLogger(loggerName)
        logger.setLevel(logging.DEBUG)

        formatStr = '%(asctime)s %(levelname)s - %(message)s'
        dateFormat = '%H:%M:%S'
        cformat = '%(log_color)s' + formatStr
        formatter = colorlog.ColoredFormatter(cformat, dateFormat)

        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(formatter)

        logger.addHandler(streamHandler)

        return logger
