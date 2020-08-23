import os


def read_query(query_name: str, logger):
    """
    Loads a query from the queries folder and returns it
    :param logger: The logger object
    :param query_name: The query to be loaded
    :return:
    """
    logger.info("Reading query: {}".format(query_name))
    try:
        f = open('queries/{}'.format(query_name))
        return f.read()
    except FileNotFoundError as e:
        raise e


def read_variable(name: str, default=None):
    """
    Reads an environment variable from the system
    :param default: The default value to be used in case the variable is not set
    :param name: The name of the variable
    :return:
    """
    return os.getenv(name, default)
