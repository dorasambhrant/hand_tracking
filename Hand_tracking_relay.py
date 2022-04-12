import cv2 as cv
import mediapipe as mp
import time
from shapely.geometry import Point
from shapely.geometry import polygon
from shapely.geometry.polygon import Polygon
import urllib.request
import tkinter as tk
from tkinter import simpledialog
ROOT = tk.Tk()
ROOT.withdraw()
ip = simpledialog.askstring(title="ThumbsDown",prompt="Enter The IP of the RELAY")
col=(36, 255, 116)
root_url = "http://"+str(ip)+"/" 
def sendRequest(url):
	n = urllib.request.urlopen(url)

cap = cv.VideoCapture(0)
W_state=True
R_state=True
mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False,
                      max_num_hands=2,
                      min_detection_confidence=0.5,
                      min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils
x=180
y=100
w=300
h=250
a= (x,y)
b= (x,y+h)
c= (x+w,y+h)
d= (x+w,y)
print(a,b,c,d)
points_cord=(a,b,c,d)
points=Polygon(points_cord)
ptime = 0
ctime = 0
while True :
    _, imgo = cap.read()
    k=cv.waitKey(1)
    img = cv.cvtColor(imgo,cv.COLOR_BGR2RGB)     
    results  = hands.process(img)
    ok = int(1)
    W_state=True
    col=(36, 255, 116)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks :
            for id,lm in enumerate(handLms.landmark): 
                h, w, c = img.shape 
                cx,cy = int(lm.x * w), int(lm.y * h)
                if((cx or cy)!=0):
                    cp=Point(cx,cy)
                if (id == 4 or id== 8 or id==12 or id==20 or id==16) :
                    if(points.contains(cp)):
                        W_state=False
                        cv.circle(imgo,(cx,cy),10,(0,255,0),cv.FILLED)
                        col=(0,0,255)
                        
    
    else:
        col=(36, 255, 116)
        W_state=True
    if k==32:
        if (W_state):
            R_state=not R_state
            if(R_state):
                sendRequest(root_url+"/OPEN_LED")
            else:
                sendRequest(root_url+"/CLOSE_LED")
        else:
            sendRequest(root_url+"/CLOSE_LED")

    cv.putText(imgo,str("WINDOW-OPEN") if int(R_state) else str("WINDOW-CLOSED"), (75,25), cv.FONT_HERSHEY_DUPLEX, 1.0, (25,255,231), 2)
    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime  
    cv.rectangle(imgo,b,d,col,3)
    cv.putText(imgo,str(int(fps)),(25,25),cv.FONT_HERSHEY_DUPLEX,1.0,(235,132,7),thickness = 2)
    if k & 0xFF== 27  :
        break
    cv.namedWindow("ThumbsDown", cv.WND_PROP_FULLSCREEN)
    cv.setWindowProperty("ThumbsDown", cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
    cv.imshow("ThumbsDown",imgo)

cap.release()