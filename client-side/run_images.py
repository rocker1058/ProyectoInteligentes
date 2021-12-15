import os
import cv2
import base64
import requests
import json
import sys

from utils.Detector import Detector
from utils.utils import resizeImage, generate_client_id
import CONFIG as cfg


if __name__ == "__main__":

    # generar  el id del cliente 
    detector = Detector()

    
    # inicializar la camara para hacer con video o webcam
    #cap = cv2.VideoCapture(cfg.SOURCE)

    # imagenes o directorio
    for image_name in os.listdir(cfg.SOURCE_IMAGES):

        image_path = os.path.join(cfg.SOURCE_IMAGES, image_name)
        img = cv2.imread(image_path)

        roi = None
        if img is not None:
            # resize para las imagenes con 720
            img = resizeImage(img, width=720)

            # correr el clasificador para el directorio
            img, roi = detector.detect(img)
            if roi is not None:
                #cambiar el tamaño del recorte de ROI especificado en el archivo CONFIG.py 
                roi = cv2.resize(roi, cfg.ROI_SIZE, interpolation=cv2.INTER_AREA)

                # generar el nombre para el crop de ROI 
                roi_id = (max([int(f.split("__")[1].split(".")[0]) for f in os.listdir(cfg.ROI_SAVE_PATH)]) 
                    if len(os.listdir(cfg.ROI_SAVE_PATH)) > 0 else 0)
                roi_id += 1
                roi_path = os.path.join(cfg.ROI_SAVE_PATH, f"roi__{roi_id}.jpg")
                
                # guardar el roi
                cv2.imwrite(roi_path, roi)
                print(f"roi__{roi_id}.jpg image saved ...")
            else:
                print("nothing to detect ...")
            
            cv2.imshow("client camera", img)

            if roi is not None:            
                # agregar bordes al roi 
                roi = cv2.copyMakeBorder(
                    roi,
                    top=10,
                    bottom=10,
                    left=10,
                    right=10,
                    borderType=cv2.BORDER_CONSTANT,
                    value=[0, 0, 255]
                )
                cv2.imshow("last cropped image", roi)
            key = cv2.waitKey(0)

            if key == 27 or key == ord('q'):
                sys.exit()
                
            elif key == ord('e'):
                # convertir todos los crop de roi a base64 
                print("sending crops to the server for prediction")
                break
            
    #destruye las ventanas opencv
    cv2.destroyAllWindows()
    #cap.release()   

    # iterando a través de crop para generar códigos base64 
    images = []
    for roi_name in os.listdir(cfg.ROI_SAVE_PATH):

        roi_id = roi_name.split("__")[1].split(".")[0]
        roi_path = os.path.join(cfg.ROI_SAVE_PATH, roi_name)
        roi = cv2.imread(roi_path)

        retval, buffer = cv2.imencode('.jpg', roi)
        roi_base64 = base64.b64encode(buffer)
        images.append({
            "id": roi_id,
            "Content": roi_base64.decode('UTF-8')   # convertir la matriz de bytes a formato de string 
        })
        print(f"base64 code generated for {roi_name} ...")

    print("waiting for the server response ...")
    # datos que se enviarán a api 
    data = {
        'id_client': cfg.CLIENT_ID,
        'images': images,
        'models': [key for key in cfg.MODELS_LIST if cfg.MODELS_LIST[key]]
        }

    headers = {
        'Content-type': 'application/json', 
        'Accept': 'text/plain'
        }
    
    # enviar solicitud de publicación y guardar respuesta como objeto de respuesta 
    response = requests.post(
        url = cfg.API_ENDPOINT, 
        data = json.dumps(data),
        headers = headers
        )

    # extraer el formato json de respuesta 
    response_json = response.json()
    print(json.dumps(response_json, indent=4, sort_keys=True))

