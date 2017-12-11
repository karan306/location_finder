import cv2
import numpy as numpy
import os, sys

inp = input()
params = inp.split()
cascade_file=params[0]

pos_path=params[1]
print(pos_path)
pos_dirs=os.listdir( pos_path )

obj_cascade = cv2.CascadeClassifier(cascade_file)

pos_count=0
pos_total=0

for file in pos_dirs:
	img = cv2.imread(pos_path+file)
	gray= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	lis = obj_cascade.detectMultiScale(gray,1.2,6,0,(100,100))
	pos_total=pos_total+1
	if (len(lis)!=0):
		pos_count=pos_count+1

print(pos_count,"out of",pos_total,"correct detections in positive images")

neg_path=params[2]
print(neg_path)
neg_dirs=os.listdir( neg_path )

neg_count=0
neg_total=0

for file in neg_dirs:
	img = cv2.imread(neg_path+file)
	gray= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	lis = obj_cascade.detectMultiScale(gray,1.2,6,0,(100,100))
	neg_total=neg_total+1
	if (len(lis)!=0):
		neg_count=neg_count+1

print(neg_count,"out of",neg_total,"correct detections in negative images")