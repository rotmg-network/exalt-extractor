import datetime
import os.path
import logging
from sys import stdout
from colorama import Fore, Back, Style, init


def test_colors() -> None:
    """ Prints all the ANSI 256 colors with their code to the console. """
    print('\n-------- Testing ANSI colors --------\n')
    for i in range(0, 16):
        for j in range(0, 16):
            code = str(i * 16 + j)
            stdout.write(u"\u001b[38;5;" + code + "m " + code.ljust(4))
        print(u"\u001b[0m")
    print('\n')


def add_custom_log_level(lvl_name: str, lvl_num: int, method_name=None) -> None:
    """
    Add a custom log level to the logging module.
    :param lvl_name: The log level name.
    :param lvl_num: Log level number in the hierarchy. Higher number = more important e.g DEBUG = 5 and INFO = 10.
    :param method_name: The name of the method that calls the log function (defaults to `lvl_name`).
    """
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


def get_log_time(now: datetime.datetime) -> str:
    """ Return a formatted time string (e.g 01/02/22 10:21:05) from a given datetime. """
    return now.strftime("%d-%m-%y %H:%M:%S")


def get_input(message: str = "") -> str:
    """
    A wrapper function over `input()` that uses our custom logger format.
    :param message: The message to print when asking the user for input (optional).
    """
    time_now = get_log_time(datetime.datetime.now())
    print(f"{Style.BRIGHT}{Back.BLACK}{time_now} [INPUT] {'Enter input' if message == '' else message}:{Style.RESET_ALL} ", end="", sep="")
    return input()


class CustomLogLevel:
    """ Class for adding custom LogLevels mapped to integers for the built-in `logging` package. """
    SUCCESS = 15


class ColorFormatter(logging.Formatter):
    """ A custom color formatter for the built-in `logging` package that uses ANSI color codes. """

    def __init__(self, fmt: str):
        """
        Initialize the color formatter with a custom formatting string.
        :param fmt: Format of the log output. See the `logging` package docs for more info.
        """
        super().__init__()
        self.fmt = fmt
        # Initialize all LogLevel types - default and custom
        self.FORMATS = {
            logging.DEBUG: Fore.LIGHTMAGENTA_EX + self.fmt + Style.RESET_ALL,
            logging.INFO: Fore.CYAN + self.fmt + Style.RESET_ALL,
            logging.WARNING: Fore.YELLOW + self.fmt + Style.RESET_ALL,
            logging.ERROR: Fore.RED + self.fmt + Style.RESET_ALL,
            logging.CRITICAL: Back.BLACK + Style.BRIGHT + Fore.RED + self.fmt + Style.RESET_ALL,
            CustomLogLevel.SUCCESS: Style.BRIGHT + Fore.GREEN + self.fmt + Style.RESET_ALL,
        }

    def format(self, record: logging.LogRecord) -> str:
        """
        Custom format function that adds a current readable date/time and log level to a log record and returns it as text.
        :param record: The log record to format.
        :returns: The formatted string that is ready to be passed to the logger.
        """
        log_format = self.FORMATS.get(record.levelno)
        time = get_log_time(datetime.datetime.now())
        formatter = logging.Formatter(time + " " + log_format)
        return formatter.format(record)


class Logger:
    """ The actual logger class that wraps the logging library and is exported/used. """

    _instance = None

    def __new__(cls, *args, **kwargs):
        """ Hook new initializations to ensure the class is a singleton. self._instance contains the global class instance. """
        if cls._instance is None:
            init()  # initialize colorama
            cls._instance = super().__new__(cls)
            add_custom_log_level("SUCCESS", CustomLogLevel.SUCCESS)
            cls._instance = logging.getLogger("crumbs")
            cls._instance.setLevel(logging.DEBUG)
            #
            now = datetime.datetime.now()
            formatter = ColorFormatter('[%(filename)s | %(levelname)s] %(message)s')
            # Ensure that the "logs" directory exists
            dirname = "./logs"
            if not os.path.isdir(dirname):
                os.mkdir(dirname)
            # Create a console and file logging handler
            file_handler = logging.FileHandler(dirname + "/log_" + now.strftime("%Y-%m-%d") + ".log")
            stream_handler = logging.StreamHandler()
            file_handler.setFormatter(formatter)
            stream_handler.setFormatter(formatter)
            cls._instance.addHandler(file_handler)
            cls._instance.addHandler(stream_handler)
        return cls._instance

    @staticmethod
    def newline() -> None:
        """ Simple readability function to log a newline to the console. """
        print("\n")


def get_logger(name: str = None):
    """
    Return a Logger instance for the optional passed file name. This function should be imported in other files.
    :param name: The name of the file the Logger class is called from (default: already set).
    """
    if name is not None:
        return Logger(name)
    return Logger()
