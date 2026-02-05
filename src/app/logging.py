import logging


def setup_logging(level=logging.DEBUG):
    logging.basicConfig(
        level=level,
        datefmt='%Y-%m-%d %H:%M:%S',
        format='[%(asctime)s.%(msecs)03d] %(levelname)s - %(message)s',
    )
