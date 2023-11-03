import logging
import re
import inspect

# for `/a/b/c.py` captures `c` as the first group
DROP_PY_RE = re.compile('^.*\/(.*)?\.pyc?')
def make_logger():
    """
    Makes a logger from a given python filename passed by __filename__
    TODO(@abhillman): structured logging
    :param filename:
    :return:
    """
    # Get the stack so we can fetch the caller
    filename = inspect.stack()[1].filename

    # Create a name from the filename of caller
    sanitized_name = DROP_PY_RE.sub(r'\1', filename)

    # The following is largely from https://docs.python.org/3/howto/logging.html#configuring-logging.
    # create logger
    logger = logging.getLogger(sanitized_name)
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)

    return logger
