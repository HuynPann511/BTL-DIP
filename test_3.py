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
        cv2.fillPoly(mask, polygons, 255)
        masked_image = cv2.bitwise_and(frame, mask)
        return masked_image

# XÁC ĐỊNH TRUNG BÌNH HỆ SỐ SLOPE (HS GÓC) VÀ INTERCEPT (HS GIAO)
#-------------- tạo ra các tọa độ của đường thẳng từ các thông số của đường thẳng (hs góc và hs giao) -----------------
"""
def make_coordinates(image, line_parameters):
    slope, intercept = line_parameters
    y1 = image.shape[0]
    y2 = int(y1*(3/5))
    x1 = int((y1 - intercept)/slope)
    x2 = int((y2 - intercept)/slope)
    return np.array([x1, y1, x2, y2])

#-------------- tính toán trung bình của các thông số -----------------
# Kết quả là một cặp đường thẳng trái và phải có các thông số đã được trung bình
def average_slope_intercept(image, lines):
    left_fit = []
    right_fit = []
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        slope = parameters[0]
        intercept = parameters[1]
        if slope < 0:
            left_fit.append((slope, intercept))
        else:
            right_fit.append((slope, intercept))
    left_fit_average = np.average(left_fit, axis=0)
    right_fit_average = np.average(right_fit, axis=0)
    left_line = make_coordinates(image, left_fit_average) 
    right_line = make_coordinates(image, right_fit_average)
    return np.array([left_line, right_line])
"""
#-------------- Hàm vẽ các đường thẳng trắng lên ảnh màu đen  -----------------
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
    lower_white = 130
    upper_white = 260
    mask = cv2.inRange(blur, lower_white, upper_white)
    edges = cv2.Canny(blur, 75, 150)
    cv2.imshow('nhap', edges)

#-------------------- XÁC ĐỊNH ROI --------------------
    plt.imshow(edges)
    #plt.show() 
    after_ROI = region_of_interest(edges)
    cv2.imshow('after_ROI', after_ROI)
   
#-------------------- HOUGH TRANSFORM --------------------
    lines = cv2.HoughLinesP(after_ROI, 1, np.pi/180, 50, maxLineGap=80)
   #average_lines = average_slope_intercept(frame, lines)
    line_video = display_lines(frame, lines)
    combo_video = cv2.addWeighted(frame, 0.8, line_video, 1, 1) #ghép 2 video lại với 2 trọng số khác nhau

#_________________________________________________________________________________
    cv2.imshow('gray', gray)
    #cv2.imshow('blur', blur)
    cv2.imshow("frame", frame)
    #cv2.imshow("edges_blur", edges)
    cv2.imshow('result', combo_video)
    #if wanna load again the video:
    #if not ret:
     #   video = cv2.VideoCapture("road car view.mp4")
     #   continue
    # Chờ 1ms, và kiểm tra xem có phím nào được nhấn không
    key = cv2.waitKey(1) & 0xFF

        # Nếu phím spacebar được nhấn, thì tạm dừng hoặc tiếp tục video
    if key == ord(' '):
        while True:
            key2 = cv2.waitKey(1) or 0xff
            cv2.imshow('Video', frame)
            if key2 == ord(' '):
                break
        
    key = cv2.waitKey(25)
    if key == 27:
        break
video.release()
cv2.destroyAllWindows()