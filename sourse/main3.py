# import the necessary packages
import numpy as np
from imutils.perspective import four_point_transform
from imutils import contours
import imutils
import cv2 as cv2

# define the dictionary of digit segments, so we can identify
# each digit on the thermostat
DIGITS_LOOKUP = {
    (1, 1, 1, 0, 1, 1, 1): 0,
    (0, 0, 1, 0, 0, 1, 0): 1,
    (1, 0, 1, 1, 1, 1, 0): 2,
    (1, 0, 1, 1, 0, 1, 1): 3,
    (0, 1, 1, 1, 0, 1, 0): 4,
    (1, 1, 0, 1, 0, 1, 1): 5,
    (1, 1, 0, 1, 1, 1, 1): 6,
    (1, 1, 1, 0, 0, 1, 0): 7,
    (1, 1, 1, 1, 1, 1, 1): 8,
    (1, 1, 1, 1, 0, 1, 1): 9
}
# load the example image
image = cv2.imread("photo.jpg")

# pre-process the image by resizing it, converting it to
# graycale, blurring it, and computing an edge map
image = imutils.resize(image, height=500)
cv2.imshow('Input', image)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(blurred, 50, 200, 255)

# cv2.imshow('2', edged)

# find contours in the edge map, then sort them by their
# size in descending order
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
displayCnt = None
# loop over the contours
for c in cnts:
    # approximate the contour
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    # if the contour has four vertices, then we have found
    # the thermostat display
    print(len(approx))
    if len(approx) == 4:
        displayCnt = approx
        break

warped = four_point_transform(gray, displayCnt.reshape(4, 2))
output = four_point_transform(image, displayCnt.reshape(4, 2))

# cv2.imshow('3', output)

# threshold the warped image, then apply a series of morphological
# operations to clean up the thresholded image
thresh = cv2.threshold(warped, 60, 255, cv2.THRESH_BINARY_INV)[1]
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 3))
thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

# cv2.imshow('2', thresh)

# find contours in the thresholded image, then initialize the
# digit contours lists
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
digitCnts = []

# # Самый конченный кусок кода
for c in cnts:
    (x, y, w, h) = cv2.boundingRect(c)
    if x < 50 or y < 10 or w > 70 or h > 50 or cv2.contourArea(c) > 700 or cv2.contourArea(c) < 20:
        cv2.fillPoly(thresh, pts=[c], color=(0, 0, 0))
output1 = cv2.drawContours(output.copy(), cnts, -1, (0, 255, 0), 1)
# cv2.imshow('3', output1)
# #

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 5))
thresh = cv2.morphologyEx(thresh, cv2.MORPH_DILATE, kernel)

digitCnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
digitCnts = imutils.grab_contours(digitCnts)

# output2 = cv2.drawContours(output.copy(), digitCnts, -1, (0, 255, 0), 1)
# cv2.imshow('4.2', output2)

# Сортировка слева направо
# digitCnts = contours.sort_contours(digitCnts, method="left-to-right")[0]
digits = []
cv2.imshow('Contour', thresh)
# loop over each of the digits

# thresh1 = cv2.cvtColor(thresh.copy(), cv2.COLOR_GRAY2BGR)

for c in digitCnts:
    # extract the digit ROI
    (x, y, w, h) = cv2.boundingRect(c)
    roi = thresh[y:y + h, x:x + w]
    # compute the width and height of each of the 7 segments
    # we are going to examine
    (roiH, roiW) = roi.shape
    (dW, dH) = (int(roiW * 0.3), int(roiH * 0.3))
    dHC = int(roiH * 0.1)
    # define the set of 7 segments
    segments = [
        ((0, 0), (w, dH)),  # top
        ((0, 0), (dW, h // 2)),  # top-left
        ((w - dW, 0), (w, h // 2)),  # top-right
        ((0, (h // 2) - dHC), (w, (h // 2) + dHC)),  # center
        ((0, h // 2), (dW, h)),  # bottom-left
        ((w - dW, h // 2), (w, h)),  # bottom-right
        ((0, h - dH), (w, h))  # bottom
    ]
    on = [0] * len(segments)

    # cv2.putText(thresh1, str(m), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)

    # loop over the segments
    for (i, ((xA, yA), (xB, yB))) in enumerate(segments):
        # extract the segment ROI, count the total number of
        # thresholded pixels in the segment, and then compute
        # the area of the segment
        segROI = roi[yA:yB, xA:xB]

        # cv2.rectangle(thresh1, (x + xA, y + yA), (x + xB, y + yB), (0, 255, 0), 1)

        total = cv2.countNonZero(segROI)
        area = (xB - xA) * (yB - yA)
        # if the total number of non-zero pixels is greater than
        # 50% of the area, mark the segment as "on"
        if float(area) != 0 and total != 0 and total / float(area) > 0.5:
            on[i] = 1
    # lookup the digit and draw it on the image
    print(tuple(on), end=' ')
    if cv2.countNonZero(roi) / (w * h) >= 0.65:
        on = [0, 0, 1, 0, 0, 1, 0]

    digit = '-'
    try:
        digit = DIGITS_LOOKUP[tuple(on)]
        print(' = ', digit)
        digits.append(digit)
    except:
        print("not find")
        digit = '1'

    cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 1)
    cv2.putText(output, str(digit), (x + 10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)

cv2.imshow('Result!', output)
cv2.waitKey()
