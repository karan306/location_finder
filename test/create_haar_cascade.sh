#!/bin/bash

cwd=$(pwd)
read -p "Name of the object": name
read -p "Positive Images Directory(Atleast 50)": pos_images
read -p "Negative Images Directory(Atleast 1200)": neg_images
read -p "height-width ratio of the object to detect": ratio

name="$name.xml"
touch $name

if [ $ratio -gt 1 ]
	then
	w=20
	h=$((ratio * 20))
else
	h=20
	w=$((ratio * 20))
fi

h2=$((h * 10))
w2=$((w * 10))

mkdir pos_train_images
mkdir pos_test_images
mkdir neg_train_images
mkdir neg_test_images

# mkdir neg_images
# alias mtd "cd"
cp -v "$pos_images/"*.jpe $cwd/pos_test_images
cp -v "$neg_images/"*.jpe $cwd/neg_test_images
find "$cwd/pos_test_images/"*.jpe -maxdepth 1 | head -30 | xargs mv -t ./pos_train_images
find "$cwd/neg_test_images/"*.jpe -maxdepth 1 | head -1000 | xargs mv -t ./neg_train_images
# ln $neg_images ./neg_images

echo "$cwd/pos_train_images/ $h2 $w2 positive_images" | python3 resize.py
echo "$cwd/neg_train_images/ 400 400 negative_images" | python3 resize.py

find ./positive_images -iname "*.jpg" > positives.txt
find ./negative_images -iname "*.jpg" > negatives.txt

str="opencv_createsamples -bgcolor 0 -bgthresh 0 -maxxangle 1.1\
   -maxyangle 1.1 maxzangle 0.5 -maxidev 40 -w "

str="$str$w -h $h"
echo $str

mkdir classifier
mkdir samples

perl bin/createsamples.pl positives.txt negatives.txt $cwd/samples 2500\
   "$str"

python ./tools/mergevec.py -v samples/ -o samples.vec

opencv_traincascade -data classifier -vec samples.vec -bg negatives.txt\
   -numStages 20 -minHitRate 0.999 -maxFalseAlarmRate 0.5 -numPos 2000\
   -numNeg 1000 -w $w -h $h -mode ALL -precalcValBufSize 1024\
   -precalcIdxBufSize 1024

# cp ./classifier/cascade.xml .
cat $cwd/classifier/cascade.xml > $name

echo "$name $cwd/pos_test_images/ $cwd/neg_test_images/" |python3 tester.py

rm -r pos_test_images
rm -r pos_train_images
rm -r neg_train_images
rm -r neg_test_images
rm -r classifier
rm -r samples
rm *.txt
rm *.xml


