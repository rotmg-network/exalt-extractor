import datetime
import os.path
import sys
import logging
from colorama import Fore, Back, Style, init


def test_colors() -> None:
    """ Prints all the ANSI 256 colors and their code to the console """
    for i in range(0, 16):
        for j in range(0, 16):
            code = str(i * 16 + j)
            sys.stdout.write(u"\u001b[38;5;" + code + "m " + code.ljust(4))
        print(u"\u001b[0m")


def add_custom_log_level(lvl_name: str, lvl_num: int, method_name=None):
    """ Add a custom log level to the logging module """
    if method_name is None:
        method_name = lvl_name.lower()

    if hasattr(logging, lvl_name):
        raise AttributeError(f"'{lvl_name}' already defined in logging module")
    if hasattr(logging, method_name):
        raise AttributeError(f"'{method_name}' already defined in logging module")
    if hasattr(logging.getLoggerClass(), method_name):
        raise AttributeError(f"'{method_name}' already defined in logger class")

    def log_for_level(self, message, *args, **kwargs):
        if self.isEnabledFor(lvl_num):
            self._log(lvl_num, message, args, **kwargs)

    def log_to_root(message, *args, **kwargs):
        logging.log(lvl_num, message, *args, **kwargs)

    logging.addLevelName(lvl_num, lvl_name)
    setattr(logging, lvl_name, lvl_num)
    setattr(logging.getLoggerClass(), method_name, log_for_level)
    setattr(logging, method_name, log_to_root)


def get_log_time(now) -> str:
    """ Return a formatted time string (e.g 01/02/22 10:21:05) from a given datetime """
    return now.strftime("%d-%m-%y %H:%M:%S")


def get_input(message: str) -> str:
    """ A custom wrapper over input() that uses our logging format """
    time_now = get_log_time(datetime.datetime.now())
    print(f"{Style.BRIGHT}{Back.BLACK}{time_now} [INPUT] {message}:{Style.RESET_ALL} ", end="", sep="")
    return input()


class CustomLogLevel:
    SUCCESS = 15


class ColorFormatter(logging.Formatter):
    """ A custom formatter for the logging library that uses ANSI color codes """

    def __init__(self, fmt):
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.DEBUG: Fore.LIGHTMAGENTA_EX + self.fmt + Style.RESET_ALL,
            logging.INFO: Fore.CYAN + self.fmt + Style.RESET_ALL,
            logging.WARNING: Fore.YELLOW + self.fmt + Style.RESET_ALL,
            logging.ERROR: Fore.RED + self.fmt + Style.RESET_ALL,
            logging.CRITICAL: Back.BLACK + Style.BRIGHT + Fore.RED + self.fmt + Style.RESET_ALL,
            CustomLogLevel.SUCCESS: Style.BRIGHT + Fore.GREEN + self.fmt + Style.RESET_ALL,
        }

    def format(self, record):
        log_format = self.FORMATS.get(record.levelno)
        time = get_log_time(datetime.datetime.now())
        formatter = logging.Formatter(time + " " + log_format)
        return formatter.format(record)


class Logger:
    # _instance is the singleton Logger class
    _instance = None

    def __new__(cls, *args, **kwargs):
        """ Ensure the class is only initialized as a singleton by persisting itself """
        if cls._instance is None:
            init()  # initialize colorama
            cls._instance = super().__new__(cls)
            add_custom_log_level("SUCCESS", CustomLogLevel.SUCCESS)
            cls._instance = logging.getLogger("crumbs")
            cls._instance.setLevel(logging.DEBUG)

            now = datetime.datetime.now()
            formatter = ColorFormatter('[%(filename)s | %(levelname)s] %(message)s')

            dirname = "./logs"
            if not os.path.isdir(dirname):
                os.mkdir(dirname)
            file_handler = logging.FileHandler(dirname + "/log_" + now.strftime("%Y-%m-%d") + ".log")
            stream_handler = logging.StreamHandler()
            file_handler.setFormatter(formatter)
            stream_handler.setFormatter(formatter)

            cls._instance.addHandler(file_handler)
            cls._instance.addHandler(stream_handler)
        return cls._instance
