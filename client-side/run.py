import os
import cv2
import base64
import requests
import json

from utils.Detector import Detector
from utils.utils import resizeImage, generate_client_id
import CONFIG as cfg


if __name__ == "__main__":

    # generar el id del cliente 
    detector = Detector()

    # inicializar la camara
    cap = cv2.VideoCapture(cfg.SOURCE)

    crop = False
    show_crop = False
    while cap.isOpened():
        ret, frame_orig = cap.read()

        # resize del frame
        frame = None
        if ret:
            frame_orig = resizeImage(frame_orig, width=720)
            # enviar al clasificador
            if crop:
                frame, roi = detector.detect(frame_orig)
                if roi is not None:
                    # resize ROI crop especificado en el CONFIG.py  en este caso 256 x 256 
                    roi = cv2.resize(roi, cfg.ROI_SIZE, interpolation=cv2.INTER_AREA)

                    # generar un nombre para el roi ..
                    roi_id = (max([int(f.split("__")[1].split(".")[0]) for f in os.listdir(cfg.ROI_SAVE_PATH)]) 
                        if len(os.listdir(cfg.ROI_SAVE_PATH)) > 0 else 0)
                    roi_id += 1
                    roi_path = os.path.join(cfg.ROI_SAVE_PATH, f"roi__{roi_id}.jpg")
                    
                    # guardar el crop 
                    cv2.imwrite(roi_path, roi)
                    print(f"roi__{roi_id}.jpg image saved ...")
                else:
                    print("nothing to detect ...")
                crop = False
        
            print(type(frame))
            if frame is not None:
                cv2.imshow("client camera", frame)
            else:
                cv2.imshow("client camera", frame_orig)
            key = cv2.waitKey(1)

            if show_crop and roi is not None:
                cv2.imshow("last cropped image", roi)

            if key == 27 or key == ord('q'):
                break
            elif key == ord('c'):
                crop = True
                show_crop = True
            elif key == ord('e'):
                #convertir todos los crop de roi a base64
                print("sending crops to the server for prediction")
                break
    # destroy and release
    cv2.destroyAllWindows()
    cap.release()   

    # iterar a través de crop para generar códigos base64 
    images = []
    for roi_name in os.listdir(cfg.ROI_SAVE_PATH):

        roi_id = roi_name.split("__")[1].split(".")[0]
        roi_path = os.path.join(cfg.ROI_SAVE_PATH, roi_name)
        roi = cv2.imread(roi_path)

        retval, buffer = cv2.imencode('.jpg', roi)
        roi_base64 = base64.b64encode(buffer)
        images.append({
            "id": roi_id,
            "Content": roi_base64.decode('UTF-8')   # convertir los bytes a string
        })
        print(f"base64 code generated for {roi_name} ...")

    print("waiting for the server response ...")
    # datos para enviar a la api
    data = {
        'id_client': cfg.CLIENT_ID,
        'images': images,
        'models': [key for key in cfg.MODELS_LIST if cfg.MODELS_LIST[key]]
        }

    # headert http para flask
    headers = {
        'Content-type': 'application/json', 
        'Accept': 'text/plain'
        }
    
    # enviar solicitud post y guardar respuesta  
    response = requests.post(
        url = cfg.API_ENDPOINT, 
        data = json.dumps(data),
        headers = headers
        )

    # sacar la rta del json
    response_json = response.json()
    print(json.dumps(response_json, indent=4, sort_keys=True))

