import logging

LOG_LEVELS = {
    "0": logging.NOTSET,
    "1": logging.DEBUG,
    "2": logging.INFO,
    "3": logging.WARNING,
    "4": logging.ERROR,
    "5": logging.CRITICAL
}


class CustomFormatter(logging.Formatter):

    green = "\x1b[32;1m"
    white = "\x1b[29;1m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;1m"
    bold_red = "\x1b[31;21m"
    reset = "\x1b[0m"
    error_format = "%(asctime)s - %(levelname)s: (%(filename)s:%(lineno)d) %(message)s"
    info_format = "%(levelname)s: %(message)s"

    FORMATS = {
        logging.DEBUG: green + info_format + reset,
        logging.INFO: white + info_format + reset,
        logging.WARNING: yellow + error_format + reset,
        logging.ERROR: red + error_format + reset,
        logging.CRITICAL: bold_red + error_format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, "%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


logger = logging.getLogger()
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

ch.setFormatter(CustomFormatter())

logger.addHandler(ch)
