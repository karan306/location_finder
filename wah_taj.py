import cv2
import numpy as numpy

taj_cascade = cv2.CascadeClassifier('taj_cascade.xml')

img = cv2.imread('58.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
taj = taj_cascade.detectMultiScale(gray,50,50)

font = cv2.FONT_HERSHEY_SIMPLEX
for (x,y,w,h) in taj:
	cv2.putText(img,'TAJ',(x+10,y+10), font, 0.5, (11,255,255), 2, cv2.LINE_AA)
cv2.waitKey(10000)
cv2.namedWindow("window")
cv2.imshow("window", img)
# cv2.imshow('img',img)
cv2.waitKey(10000)