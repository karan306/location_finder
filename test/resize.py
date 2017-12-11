from PIL import Image
import os, sys
import cv2

inp = input()
params = inp.split()
print(params)
path = params[0]
# path = "/home/karan/location_finder/taj/"
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


w=int(params[1])
h=int(params[2])
copy_path=params[3]
copy_path=copy_path+"/"
if not os.path.exists(copy_path):
	os.makedirs(copy_path)
for file in dirs:
	print(file)
	try:
		img=cv2.imread(path+file)
		resized_image = cv2.resize(img,(h,w),90)
		cv2.imwrite(copy_path+str(count)+".jpg",resized_image)
		count=count+1
	except Exception as e:
		print(str(e))
