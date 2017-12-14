import cv2
import numpy as numpy
import os, sys

def tester(cascade_file,pos_path,neg_path,min_size=(100,100),sf=1.2,mn=6):
	print(cascade_file)
	obj_cascade = cv2.CascadeClassifier(cascade_file)
	pcount,ptotal= test_on(pos_path,obj_cascade,min_size,sf,mn)
	print(pcount,"of",ptotal,"detections in positive images")
	ncount,ntotal= test_on(neg_path,obj_cascade,min_size,sf,mn)
	print(ncount,"of",ntotal,"detections in negative images")


def test_on(path,obj_cascade,min_size,sf,mn):
	if(path[len(path)-1]!='/'):
		path = path+'/'
	dirs = os.listdir(path)
	count= 0
	total= 0
	for file in dirs:
		img = cv2.imread(path+file)
		gray= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		lis = obj_cascade.detectMultiScale(gray,sf,mn,0,min_size)
		total+=1
		if (len(lis)!=0):
			count+=1
	return [count,total]