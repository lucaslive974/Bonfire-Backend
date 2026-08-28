from utils.logger import Logger, HttpLogger, logger, http_logger


def test_logger_singleton():
    l1 = Logger()
    l2 = Logger()
    assert l1 is l2
    assert l1 is logger


def test_http_logger_singleton():
    h1 = HttpLogger()
    h2 = HttpLogger()
    assert h1 is h2
    assert h1 is http_logger
