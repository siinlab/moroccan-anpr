from os.path import join, dirname
from os import environ

__MODELS_PATH = join(dirname(__file__), '..', 'models')


def __get_model_path(model_name: str) -> str:
    """ Get the path to the model.

    Args:
        model_name (str): The name of the model.

    Returns:
        str: The path to the model.
    """
    return join(__MODELS_PATH, model_name, 'best.pt')


CARS_MODEL_PATH = __get_model_path('cars-model')
LP_MODEL_PATH = __get_model_path('lp-model')
LPC_MODEL_PATH = __get_model_path('ocr-model')