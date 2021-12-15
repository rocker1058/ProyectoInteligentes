import os 
import cv2
import numpy as np
import random


def resizeImage(image, width=None, height=None, inter=cv2.INTER_AREA):
   # inicializar las dimensiones de la imagen que se cambiará de tamaño

    dim = None
    (h, w) = image.shape[:2]

    # si tanto el ancho como el alto no son detectados, entonces devuelve la img original
    if width is None and height is None:
        return image

    # compruebe si no hay ancho 
    if width is None:
        if height > h:
            return image
        # calcular el ratio de la altura y construir las dimensiones

        r = height / float(h)
        dim = (int(w * r), height)
    # de lo contrario, la altura es null
    else:
        if width > w:
            return image
        # calcular la relación del ancho y construir la dimensiones

        r = width / float(w)
        dim = (width, int(h * r))

    # resize para la imagen 
    resized = cv2.resize(image, dim, interpolation=inter)
    # return de la imagen
    return resized


def generate_client_id():
    return "client_id"