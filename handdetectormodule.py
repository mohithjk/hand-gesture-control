import cv2 as cv
import mediapipe as mp
import time

class HandDetector:
    def __init__(self,mode=False,maxhands=2,detection_confidence=0.5,tracking_confidence=0.5):
        self.mode = mode
        self.maxhands = maxhands
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxhands,
            min_detection_confidence=self.detection_confidence,
            min_tracking_confidence=self.tracking_confidence
        )
        self.mpDraw = mp.solutions.drawing_utils

 
        
    def find_hands(self, img, draw=True):
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img
    def find_position(self, img, hand_no=0, draw=True):
        lm_list = []
        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[hand_no]
            for id, lm in enumerate(my_hand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([id, cx, cy])
                if draw:
                    cv.circle(img, (cx, cy), 10, (255, 0, 255), cv.FILLED)
        return lm_list

# mpHands=mp.solutions.hands
# hands=mpHands.Hands()
# mpDraw=mp.solutions.drawing_utils

    # imgRGB=cv.cvtColor(img,cv.COLOR_BGR2RGB)
    # results=hands.process(imgRGB)
  
    # print(results.multi_hand_landmarks)
    
   
    # if results.multi_hand_landmarks:
      
    #     for handLms in results.multi_hand_landmarks:
    #         for id, lm in enumerate(handLms.landmark):
    #             print(id, lm)
    #             h, w, c = img.shape
    #             cx, cy = int(lm.x * w), int(lm.y * h)
    #             cv.circle(img, (cx, cy), 5, (255, 0, 255), cv.FILLED)
    #         mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
   
    # cv.imshow("Image", img)
    # cv.waitKey(1)


def main():
    cap=cv.VideoCapture(0)
    detector = HandDetector()

    pTime=0
    cTime=0
    while True:
        success,img = cap.read()
        img = detector.find_hands(img)
        lmlist = detector.find_position(img)
        if len(lmlist) != 0:
            print(lmlist[4])
            # Example: Print the position of the thumb tip
            
         # Print the position of the thumb tip
        cTime=time.time()
        fps=1/(cTime-pTime)
        pTime=cTime
        cv.putText(img, f'FPS: {int(fps)}', (10, 70), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)



        cv.imshow("Image", img)
        cv.waitKey(1)   

if __name__=="__main__":
    main()
    # This is the main function that will be called when the script is run

