import cv2
import numpy as np
import CONFIG as cfg


class Detector:

    def __init__(self):
        pass


    def detect(self, _image, vis=False):

        # convertir la imagen a escala de grises y desenfocarla usando el desenfoque gaussiano 
        _image_grey = cv2.cvtColor(_image, cv2.COLOR_BGR2GRAY)
        _image_grey = cv2.GaussianBlur(_image_grey, (5, 5), 3)

        # realizar una detección de bordes  
        _edges = cv2.Canny(_image_grey, 50, 200, None, 3)

        # detectar contornos usando una función incorporada contornos
        contours, hierarchy = cv2.findContours(_edges, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

        # pasar los contonrnos para procesar
        if len(contours) > 0:
            _image, roi = self._contours_clusturing(_image, contours)
        else: 
            _image, roi = None, None

        if vis:
            cv2.imshow("Canny Edge Detection", _edges)
        return _image, roi


    def _find_if_close(self, cnt1, cnt2):
        row1, row2 = cnt1.shape[0], cnt2.shape[0]
        for i in range(row1):
            for j in range(row2):
                dist = np.linalg.norm(cnt1[i] - cnt2[j])
                if abs(dist) < 30:
                    return True
        return False


    def _contours_clusturing(self, _image, contours):
        status = np.zeros((len(contours), 1))
        for i, cnt1 in enumerate(contours):
            x = i
            if i != len(contours) - 1:
                for j, cnt2 in enumerate(contours[i + 1:]):
                    x = x + 1
                    dist = self._find_if_close(cnt1, cnt2)
                    if dist:
                        val = min(status[i], status[x])
                        status[x] = status[i] = val
                    else:
                        if status[x] == status[i]:
                            status[x] = i + 1

        contour_clusters = []
        maximum = int(status.max()) + 1
        for i in range(maximum):
            pos = np.where(status == i)[0]
            if pos.size != 0:
                cont = np.vstack(contours[i] for i in pos)
                hull = cv2.convexHull(cont)
                contour_clusters.append(hull)
            
        # extraer la region con mayor área 
        max_area_cnt = max(contour_clusters, key=cv2.contourArea)

        # finding rectangle coordinates arount he contour
        (x, y, w, h) = cv2.boundingRect(max_area_cnt)
        xc, yc = x + w//2, y + h//2

        # escalar las coordenadas del rectángulo 
        s = w if w >= h else h
        x1 = xc - s//2
        y1 = yc - s//2
        x2 = xc + s//2
        y2 = yc + s//2

        # dibuja un rectángulo alrededor del ROI
        cv2.rectangle(_image, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # cropear el  roi
        roi = _image[y1:y2, x1:x2]
        # roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        return (_image, roi)

