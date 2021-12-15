import os
import json

################ Paths  #######################

TEMP_FILES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/temp')
SAVED_MODELS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/data/models')
CLASSES_JSON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/data/classes.json')

################# Parametros para los modelos #####################

MODEL_1_PATH = os.path.join(SAVED_MODELS_PATH, "modelo1.h5")
MODEL_2_PATH = os.path.join(SAVED_MODELS_PATH, "modelo2.h5")
MODEL_3_PATH = os.path.join(SAVED_MODELS_PATH, "vgg16.h5")

MODELS = {
    "1": None,
    "2": None,
    "3": None
}