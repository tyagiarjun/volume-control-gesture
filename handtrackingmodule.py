import cv2
import mediapipe as mp
import time


class handDetector():
    def __init__(self,mode=False,maxHands=2,detectioncon=0.5,trackcon=0.5):
        self.mode=mode
        self.maxHands=maxHands
        self.detectioncon=detectioncon
        self.trackcon=trackcon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.maxHands,self.detectioncon,self.trackcon)
        self.mpDraw = mp.solutions.drawing_utils


    def findHands(self,img,draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.result = self.hands.process(imgRGB)
        # print(result.multi_hand_landmarks)

        if self.result.multi_hand_landmarks:
            for handLms in self.result.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

        return img

    def findposition(self,img,handNo=0,draw=True):

        lmlist=[]
        if self.result.multi_hand_landmarks:
            myhand=self.result.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myhand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmlist.append([id,cx,cy])
                if draw:
                    cv2.circle(img, (cx, cy), 7, (255, 0, 0), cv2.FILLED)

        return lmlist


def main():
    ptime = 0
    ctime = 0
    cap = cv2.VideoCapture(0)
    detector=handDetector()

    while True:
        success, img = cap.read()
        img= detector.findHands(img)
        lmlist=detector.findposition(img)
        if len(lmlist)!=0:

            print(lmlist[4])

        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = ctime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__=='__main__':
    main()