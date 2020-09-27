import inspect
import logging

class BaseClass:
    @staticmethod
    def get_logger():
        logger_name = inspect.stack()[1][3]
        logger = logging.getLogger(logger_name)
        fmt = logging.Formatter("%(asctime)s: %(levelname)s %(name)s: %(message)s")
        file_handler = logging.FileHandler('../results/api_automation.log', 'a')
        file_handler.setFormatter(fmt)
        logger.addHandler(file_handler)
        logger.setLevel(logging.INFO)
        return logger

    @staticmethod
    def dict_compare(dict1, dict2):
        if len(dict1.keys()) != len(dict2.keys()):
            return False
        for key in dict1.keys():
            if not type(dict1[key]) is dict:
                try:
                    assert dict1[key] == dict2[key], "Data Mismatch {} - {}".format(dict1[key], dict2[key])
                except AssertionError as e:
                    raise e
            else:
                if type(dict2[key]) is dict:
                    try:
                        BaseClass.dict_compare(dict1[key], dict2[key])
                    except AssertionError as e:
                        raise e
                else:
                    return False
        return True

