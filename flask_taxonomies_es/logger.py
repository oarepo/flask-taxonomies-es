import logging

logger = logging.getLogger("flask-taxonomies-es")
formatter = logging.Formatter('[%(asctime)s - %(name)s - %(levelname)s]: %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)