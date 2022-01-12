import pyqrcode
import cv2
from pyzbar.pyzbar import decode
from PIL import Image
import numpy as np
from datetime import datetime
import time

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)


def markattendance(data):
    with open('qrcode.csv','r+') as f:
        mydata = f.readlines()
        namelist = []
        for line in mydata:
            entry = line.split(',')
            namelist.append(entry[0])
        if data not in namelist:
            now  = datetime.now()
            dtstring = now.strftime('%H:%M:%S')
            f.writelines(f'\n{data},{dtstring}')

while True:
    sucess , img = cap.read()
    for barcode in decode(img):
        data = barcode.data.decode('utf-8')
        pts = np.array([barcode.polygon],np.int32)
        pts = pts.reshape((-1,1,2))
        cv2.polylines(img,[pts],True,(255,0,255),3)
        pts1 = barcode.rect
        cv2.putText(img,data,(pts1[0],pts1[1]),cv2.FONT_HERSHEY_COMPLEX,0.9,(255,0,255))
      #  print(data)
        markattendance(data)
        

    cv2.imshow("QRCode",img)
    cv2.waitKey(1)