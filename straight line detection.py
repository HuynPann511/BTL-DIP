import cv2
import numpy as np
import matplotlib.pyplot as plt

video = cv2.VideoCapture("road car view.mp4")

#-------------------------- XÁC ĐỊNH ROI ---------------------------
def region_of_interest(frame):
        height = frame.shape[0]
        polygons = np.array([
        [(82, height), (1180, height),(913, 410), (583, 410) ]
        ])
        mask = np.zeros_like(frame)
        mask_roi = cv2.fillPoly(mask, polygons, 255)
        cv2.imshow('mask_ROI', mask_roi)
        masked_image = cv2.bitwise_and(frame, mask_roi)
        return masked_image

#-------------- Hàm vẽ các đường thẳng (trắng) lên ảnh (đen)  -----------------
# ảnh đen (line_image) có cùng kích thước và kiểu dữ liệu như gốc (image)
def display_lines(image, lines):
    line_image = np.zeros_like(image) 
    if lines is not None:
        for line in lines:
            x1,y1, x2,y2 = line[0]
            cv2.line(line_image, (x1, y1), (x2, y2), (0,255,0), 5)
    return line_image

#_____________________________________________________________________________________________
while True:
    ret, frame = video.read()
    #frame = frame[400:,:] 

#-------------------- CANNY --------------------
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 75, 150)
   

#-------------------- XÁC ĐỊNH ROI --------------------
    plt.imshow(edges)
    #plt.show() 
    after_ROI = region_of_interest(edges)
    #cv2.imshow('after_ROI', after_ROI)
   
#-------------------- HOUGH TRANSFORM --------------------
    lines = cv2.HoughLinesP(after_ROI, 1, np.pi/180, 50, maxLineGap=80)
    line_video = display_lines(frame, lines)
    combo_video = cv2.addWeighted(frame, 0.8, line_video, 1, 1) #ghép 2 video lại với 2 trọng số khác nhau

#_________________________________________________________________________________
    cv2.imshow('gray', gray)
    #cv2.imshow('blur', blur)
    cv2.imshow("frame", frame)
    cv2.imshow("edges", edges)
    cv2.imshow('result', combo_video)
   
    # Chờ 1ms, và kiểm tra xem có phím nào được nhấn không
    key = cv2.waitKey(1) & 0xFF
    # Nếu phím spacebar được nhấn, thì tạm dừng hoặc tiếp tục video
    if key == ord(' '):
        while True:
            key2 = cv2.waitKey(1) or 0xff
            if key2 == ord(' '):
                break
        
    key_off = cv2.waitKey(25)
    if key_off == 27:
        break
video.release()
cv2.destroyAllWindows()