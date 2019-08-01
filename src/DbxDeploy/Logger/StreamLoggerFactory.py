import logging

class StreamLoggerFactory:

    def create(self, loggerName: str):
        logger = logging.getLogger(loggerName)
        logger.setLevel(logging.INFO)

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s', '%Y-%m-%d %H:%M:%S')
        ch.setFormatter(formatter)

        logger.addHandler(ch)

        return logger
