from flask import request,session, render_template, redirect, url_for, jsonify, Response
import os
from app import app
import base64
from PIL import Image
import re

import app.CONFIG as CONFIG
from app.utils import utils


@app.route('/')
def index():
    return render_template('index.html', status=session)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if request.method == 'POST':
            data = request.get_json(force=True)

            id_client = data["id_client"]
            models_ids = data["models"]

            # guardar todas las imágenes en una carpeta temporal 
            for image_data in data["images"]:
                image_name = image_data["id"]
                base64_code = image_data["Content"]

                # resolver el problema del padding  
                base64_code = f"{base64_code}{'=' * ((4 - len(base64_code) % 4) % 4)}"

                image_path = os.path.join(CONFIG.TEMP_FILES_PATH, image_name + '.jpg')
                with open(image_path, "wb") as f:
                    f.write(base64.b64decode(base64_code))
                print("temp image saved...")

            
            # hacer la prediccion de la imagen con el modelo que se eligi´p
            print("making predictions now...")
            results = utils.predict(models_ids)

            # borrar los crop temporales
            [os.remove(os.path.join(CONFIG.TEMP_FILES_PATH, crop)) for crop in os.listdir(CONFIG.TEMP_FILES_PATH)]
            
            return jsonify({
                "state": "success",
                "message": "Predictions made satisfactorily",
                "results": results
            })

        else:
            return jsonify({
                    "state": "error",
                    "message": "Error making predictions"
                }) 

    except Exception as e:
        return jsonify({
            "state": "error",
            "message": "Error making predictions"
        })