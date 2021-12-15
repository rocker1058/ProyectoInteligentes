import os


CLIENT_ID = "asdf0123cjekc"
PORT_NUMBER = 5000
API_ENDPOINT = f"http://localhost:{PORT_NUMBER}/predict"

MODELS_LIST = {
    "1": True,      #  modelo 1
    "2": True,      #  modelo 2
    "3": True        #  vgg16 
}


# Fuente puede ser el path a un video o imagen 
SOURCE = 0     #  webcam
#SOURCE = "videos/video_test.mp4"

SOURCE_IMAGES = "images"

# path para guardar los crop
ROI_SAVE_PATH = "crops"
os.makedirs(ROI_SAVE_PATH, exist_ok=True)   #  crear el directorio si no existe

ROI_SIZE = (256, 256)