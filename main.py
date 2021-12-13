import cv2
import random as rng
import numpy as np
import time
from mss import mss
debug= False

def process_image(img):


    # scale_percent = 50

    # #calculate the 50 percent of original dimensions
    # width = int(img.shape[1] * scale_percent / 100)
    # height = int(img.shape[0] * scale_percent / 100)

    # # dsize
    # dsize = (width, height)
    # img = cv2.resize(img, dsize)

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_gray=cv2.GaussianBlur(img_gray,(9,9),1)




    _, thresh_bin = cv2.threshold(img_gray, 30,255, cv2.THRESH_BINARY)

    contours, hierarchy = cv2.findContours(thresh_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    hull = []

    # calculate points for each contour
    for i in range(len(contours)):
        # creating convex hull object for each contour
        hull.append(cv2.convexHull(contours[i], False))
    my_hull = sorted(hull, key=cv2.contourArea)[-3]
    # create an empty black image

    rect = cv2.boundingRect(my_hull)
    x,y,w,h = rect
    cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

    table = img[y:y+h,x:x+w]

    # print(img.shape)
    # cv2.imshow("image", img)
    # cv2.imshow("th bin", thresh_bin)
    if debug: cv2.imshow("table", table)

    img_gray = cv2.cvtColor(table, cv2.COLOR_BGR2GRAY)
    if debug: cv2.imshow("gray table", img_gray)

    ret, thresh = cv2.threshold(img_gray, 245, 255, 0)

    if debug: cv2.imshow('thresh_bin', thresh)

    try:

        lines = cv2.HoughLinesP(thresh, 1, np.pi/180, 20, np.array([]), 19, 20)
        for line in lines:
            for x1, y1, x2, y2 in line:
                m = (y2-y1)/(x2-x1)
                x3=0
                y3 = int(m*(x3-x1)+y1)
                x4=table.shape[1]
                y4 = int(m*(x4-x1)+y1)

                cv2.line(table, (x3, y3), (x4, y4), (20, 220, 20), 2)
    except:pass

    return table


img = cv2.imread('image3.png')
img = process_image(img)
img= cv2.resize(img, (1100,600))
cv2.imshow('image', img)
cv2.waitKey()
cv2.destroyAllWindows()

# sct = mss()
# m = sct.monitors[1]
# w=int(m['width']*(3/4))
# monitor = {
#     "top": 0,  # 100px from the top
#     "left": 0,  # 100px from the left
#     "width": w,
#     "height":m['height'],
#     "monitor":m
# }


# while(True):
#     sct_img = sct.grab(monitor)
#     img_np = np.array(sct_img)
#     # cv2.imshow('t',img_np)
#     # cv2.waitKey()
#     # Capture frame-by-frame
#     frame = process_image(img_np)


#     # Our operations on the frame come here

#     # Display the resulting frame
#     resized= cv2.resize(frame, (200,200))
#     cv2.imshow('table',resized)
#     if cv2.waitKey(5) & 0xFF == ord('q'):
#         break

# cv2.destroyAllWindows()

