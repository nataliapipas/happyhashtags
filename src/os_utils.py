import os

cwd = os.getcwd()


def read_query(query_name: str, logger):
    """
    Loads a query from the queries folder and returns it
    :param query_name: The query to be loaded
    :return:
    """
    logger.info("Reading query: {}".format(query_name))
    try:
        f = open('queries/{}'.format(query_name))
        return f.read()
    except Exception as e:
        raise (e)
