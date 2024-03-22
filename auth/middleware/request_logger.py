# middleware/request_logger.py
from loguru import logger
import time

class RequestLoggerMiddleware:
    def __init__(self, app, log_level="INFO", log_format="{time} | {level: <8} | {message}", log_file=None):
        self.app = app
        self.log_level = log_level
        self.log_format = log_format
        self.log_file = log_file

        if self.log_file:
            logger.add(self.log_file, level=self.log_level, format=self.log_format)
        else:
            logger.add(lambda msg: print(msg, end=""), level=self.log_level, format=self.log_format)

    def __call__(self, environ, start_response):
        start_time = time.time()

        response = self.app(environ, start_response)

        end_time = time.time()

        logger.info(
            f"Request received: {environ['REQUEST_METHOD']} {environ['PATH_INFO']} "
            f"| Execution time: {end_time - start_time:.5f}s"
        )

        return response
