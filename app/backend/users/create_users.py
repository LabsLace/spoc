from shared_functions.spoc_logger import logger


def create(user):
    logger.info(user)
    return {"message": "create_user"}
