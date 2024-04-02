import cv2
import numpy as np

video = cv2.VideoCapture("road car view.mp4")
while True:
    ret, frame = video.read()
   # frame = frame[400:,:] 
    def canny(frame):
        # get edges of the video
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (9, 9), 0)
        lower_white = 150
        upper_white = 230
        canny = cv2.inRange(blur, lower_white, upper_white)
        return canny
   # mask_gray = cv2.inRange(gray, lower_white, upper_white)
  #edges_1 = cv2.Canny(mask_gray, 75, 150)
    canny = cv2.Canny(frame, 75, 150)
    
    """
    # vẽ line của gray
    lines_1 = cv2.HoughLinesP(edges_1, 1, np.pi/180, 50, maxLineGap=80)
    if lines_1 is not None: 
        for line in lines_1:
            x1,y1, x2,y2 = line[0]
            cv2.line(frame, (x1,y1), (x2,y2), (0,255,0), 5)
    
    
    #vẽ line của blur
    lines_2 = cv2.HoughLinesP(edges, 1, np.pi/180, 50, maxLineGap=80)
    if lines_2 is not None: 
        for line in lines_2:
            x1,y1, x2,y2 = line[0]
            cv2.line(frame, (x1,y1), (x2,y2), (0,255,0), 5)
    """

   # cv2.imshow('gray', gray)
    #cv2.imshow('blur', blur)
    #cv2.imshow("frame", frame)
   
    cv2.imshow('result', canny)
 
    #if wanna load again the video:
    #if not ret:
     #   video = cv2.VideoCapture("road car view.mp4")
     #   continue
    
    key = cv2.waitKey(25)
    if key == 27:
        break
video.release()
cv2.destroyAllWindows()