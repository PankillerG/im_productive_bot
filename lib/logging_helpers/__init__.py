import logging


def configure_logging(filename=None):
    logging.basicConfig(
        filename=filename,
        format='[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
        level=logging.INFO,
    )


def get_function_logger(logger):
    def function_logger(function):
        def wrapper(*args, **kwargs):
            logger.info(f'Function {function.__name__} is starting')
            try:
                function_res = function(*args, **kwargs)
                logger.info(f'Function {function.__name__} executed successfully')
                return function_res
            except:
                logger.info(f'Function {function.__name__} failed')
        return wrapper
    return function_logger
