import cv2
import numpy as np

video = cv2.VideoCapture("road car view.mp4")
while True:
    ret, frame = video.read()
    frame = frame[400:,:]

# get edges of the video
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    
    lower_white = 150
    upper_white = 230
    mask = cv2.inRange(gray, lower_white, upper_white)
    
    edges = cv2.Canny(mask, 75, 150)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, maxLineGap=80)
    if lines is not None: 
        for line in lines:
            x1,y1, x2,y2 = line[0]
            cv2.line(frame, (x1,y1), (x2,y2), (0,255,0), 5)

    cv2.imshow("frame", frame)
   
    cv2.imshow("edges", edges)
    #if wanna load again the video:
    #if not ret:
     #   video = cv2.VideoCapture("road car view.mp4")
     #   continue
    
    key = cv2.waitKey(25)
    if key == 27:
        break
video.release()
cv2.destroyAllWindows()