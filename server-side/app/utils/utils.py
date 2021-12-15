import cv2
import numpy as np
import app.CONFIG as CONFIG
import os
from tensorflow.keras.models import load_model
from keras import backend as K


def load_models():

    # metrica de los modelos
    dependencies = {
        'precision_m': precision_m,
        "recall_m": recall_m,
        "f1_m": f1_m
    }

    CONFIG.MODELS["1"] = load_model(CONFIG.MODEL_1_PATH, custom_objects=dependencies)
    CONFIG.MODELS["2"] = load_model(CONFIG.MODEL_2_PATH, custom_objects=dependencies)
    CONFIG.MODELS["3"] = load_model(CONFIG.MODEL_3_PATH, custom_objects=dependencies)

def predict(models_ids):
    resutls = []
    for model_id in models_ids:
        
        # inicializar el diccionario de resultados del modelo 
        model_results = {
            "model_id": model_id,
            "results": []
        }

        # obtener el modelo del diccionario de modelos basado en la identificación del modelo 
        model = CONFIG.MODELS[model_id]

        # iterar a través de todas las imágenes guardadas en la carpeta temporal 
        for image_name in os.listdir(CONFIG.TEMP_FILES_PATH):
            
            # leer la imagen usando la ruta de la imagen 
            image_path = os.path.join(CONFIG.TEMP_FILES_PATH, image_name)
            img = cv2.imread(image_path)

            # si el modelo no es VGG, se debe convertir a una escala de gris solo par 1 y 2 
            if model_id in ["1", "2"]:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                img = np.expand_dims(img, axis=2)


            # preprocesar la imagen 
            img = img / 255.
            img_batch = np.expand_dims(img, axis=0)  

            # hacer las predicciones en el directorio y seleccionar el primero 
            predictions = model.predict(img_batch)[0] 

            # tomar el índice de la clase con mayor probabilidad
            cls_id = np.argmax(predictions)

            # agregar la identificación de la imagen y la clase de predicción 
            model_results["results"].append({
                "class": str(cls_id),
                "id-image": image_name.split(".")[0]
            })

        # agregar los resultados del modelo a la lista de resultados  para mostrar al cliente
        resutls.append(model_results)
    
    print(resutls)
    return resutls


def recall_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall

def precision_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision

def f1_m(y_true, y_pred):
    precision = precision_m(y_true, y_pred)
    recall = recall_m(y_true, y_pred)
    return 2 * ((precision * recall) / (precision + recall + K.epsilon()))

