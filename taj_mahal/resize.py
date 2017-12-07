from PIL import Image
import os, sys
import cv2

path = "/home/karan/location_finder/taj_mahal/non-taj/"
dirs = os.listdir( path )

# def resize():
#     for item in dirs:
#         if os.path.isfile(path+item):
#             im = Image.open(path+item)
#             f, e = os.path.splitext(path+item)
#             imResize = im.resize((200,200), Image.ANTIALIAS)
#             imResize.save(f + ' resized.jpg', 'JPEG', quality=90)

# resize()
count=1

if not os.path.exists('neg'):
	os.makedirs('neg')
for file in dirs:
	try:
		img=cv2.imread(path+file)
		resized_image = cv2.resize(img, (100, 100),90)
		cv2.imwrite("neg/"+str(count)+".jpg",resized_image)
		count=count+1
	except Exception as e:
		print(str(e))
