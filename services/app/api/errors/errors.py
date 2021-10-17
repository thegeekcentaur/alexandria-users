import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def invalid_request(err):
    logger.error(f"Exception raised {err} while inserting data to Mongodb. Please check the request body.")
