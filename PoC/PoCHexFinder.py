import cv2
import numpy as np

def HexFinder(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)

    contours, _= cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    max_area = 0
    c = 0
    for i in contours:
            area = cv2.contourArea(i)
            if area > 1000:
                    if area > max_area:
                        max_area = area
                        best_cnt = i
                        image = cv2.drawContours(image, contours, c, (0, 255, 0), 3)
            c+=1
    mask = np.zeros((gray.shape),np.uint8)
    cv2.drawContours(mask,[best_cnt],0,255,-1)
    cv2.drawContours(mask,[best_cnt],0,0,2)

    out = np.zeros_like(gray)
    out[mask == 255] = gray[mask == 255]

    blur = cv2.GaussianBlur(out, (5,5), 0)

    thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)
    cv2.imshow("thresh1", thresh)

    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    averageArea = 0
    counter = 0
    for i in contours:
        area = cv2.contourArea(i)
        if area > 1000/2 and area < 2000:
            counter += 1
            averageArea += area

    averageArea = averageArea/counter

    c = 0
    HexFound = np.zeros_like(image)
    for i in contours:
        area = cv2.contourArea(i)
        if area > 700:
            cv2.drawContours(HexFound, contours, c, (0, 255, 0), 3)
        c+=1

    return HexFound

