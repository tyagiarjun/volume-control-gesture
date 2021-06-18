import cv2
import time
import numpy as np
import handtrackingmodule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam,hCam=640,480

cap= cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
pTime=0

detector=htm.handDetector(detectioncon=0.8)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange=(volume.GetVolumeRange())
minVol=volRange[0]
maxVol=volRange[1]
vol=0
volbar=400


while True:
    success,img=cap.read()

    img= detector.findHands(img)
    lmlist=detector.findposition(img,draw=False)
    if len(lmlist)!=0:
        #print(lmlist[4],lmlist[8])

        x1,y1=lmlist[4][1],lmlist[4][2]
        x2,y2=lmlist[8][1],lmlist[8][2]

        cx,cy=(x1+x2)//2, (y1+y2)//2

        cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
        cv2.circle(img,(x2,y2),15,(255,0,255),cv2.FILLED)
        cv2.circle(img,(cx,cy),15,(255,0,255),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)

        length=math.hypot(x2-x1,y2-y1)
        #print(length)


        vol=np.interp(length,[20,170],[minVol,maxVol])
        volbar=np.interp(length,[20,170],[400,150])

        print(int(length),vol)

        volume.SetMasterVolumeLevel(vol, None)

        if length<20:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

    cv2.rectangle(img,(50,150),(85,400),(0,255,0),3)
    cv2.rectangle(img,(50,int(volbar)),(85,400),(0,255,0),cv2.FILLED)

    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime

    cv2.putText(img,str(int(fps)),(40,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),1)
    cv2.imshow('IMAGE',img)
    cv2.waitKey(1)