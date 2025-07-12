import cv2 as cv
import mediapipe as mp
import time
import numpy as np
import handdetectormodule as hdm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

cap=cv.VideoCapture(0)
wCam ,hCam=640,480
cv.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime=0
detector = hdm.HandDetector( detection_confidence=0.7)
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# Get the current volume range
minVol=volume.GetVolumeRange()[0]
maxVol=volume.GetVolumeRange()[1]
vol=0
volRect=400
volPer=0



# print(f"Audio output: {device.FriendlyName}")
# print(f"- Muted: {bool(volume.GetMute())}")
# print(f"- Volume level: {volume.GetMasterVolumeLevel()} dB")
print(f"- Volume range: {volume.GetVolumeRange()[0]} dB - {volume.GetVolumeRange()[1]} dB")
print(volume.GetVolumeRange())
volume.SetMasterVolumeLevel(-20.0, None)

    

while True:
    success,img=cap.read()
    # imgRGB=cv.cvtColor(img,cv.COLOR_BGR2RGB) 
    detector.find_hands(img)
    lmList = detector.find_position(img,draw=False)
   
    if len(lmList) != 0:
        # print(lmList[4],lmList[8])  # Print the position of the thumb tip
        x1,y1=lmList[4][1],lmList[4][2]
        x2,y2=lmList[8][1],lmList[8][2]
        cx,cy=(x1+x2)//2,(y1+y2)//2
        cv.circle(img, (cx, cy), 10, (255, 0, 255), cv.FILLED)
        # Draw a circle at the midpoint between the thumb and index finger tips
        # we r accesing the first and the second landmark of the hand
        cv.circle(img, (x1, y1), 10, (255, 0, 255), cv.FILLED)
        cv.circle(img, (x2, y2), 10, (255, 0, 255), cv.FILLED)
        cv.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        length = math.hypot(x2 - x1, y2 - y1)
        # Calculate the distance between the thumb and index finger tips
        #here we will be converting hand range to volume range
        vol=np.interp(length, [50, 235], [minVol, maxVol])
        volRect=np.interp(length, [50, 235], [400, 150])
        volPer=np.interp(length, [50, 235], [0, 100])
        print(f"Volume: {vol}")
        volume.SetMasterVolumeLevel(vol, None)
        # Set the volume level based on the distance between the thumb and index finger tips    
       
        if length < 50:
            cv.circle(img, (cx, cy), 10, (0, 255, 0), cv.FILLED)
            # Draw a filled circle at the midpoint if the distance is less than 50 pixels
            # cv.putText(img, "Volume Up", (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)


    cv.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
    cv.rectangle(img,(50,int(volRect)),(85,400),(0,255,0),cv.FILLED)
    cv.putText(img,f'{int(volPer)}%', (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    # Draw a rectangle around the image
    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv.putText(img, f'FPS: {int(fps)}', (40, 450), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
    cv.imshow("Image", img)
    cv.waitKey(1)
    #this will show the image in the window
    # and wait for 1 millisecond before showing the next image