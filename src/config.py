from os.path import join, dirname
from pydantic import BaseModel

class BoxOutput(BaseModel):
    """ A class to hold the output of the barcode model. """

    x1: float
    y1: float
    x2: float
    y2: float
    score: float
    label: str
    
class Status(BaseModel):
    """ A class to hold the status of the server. """

    status: str
    
    
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