import shutil
from shutil import *
import mergevec as mv
import resize as rs
import tester as ts
import sys,os,subprocess,glob
import argparse,re

cwd = os.getcwd()

def move_some(source_dir,dest_dir,n):
    s_dir = os.listdir(source_dir)
    for i,file in enumerate(s_dir):
        if(i>n):
            break
        shutil.move(source_dir+"/"+file,dest_dir)

def create_txt(path,f_name):
    f= open(f_name,"w+")
    files = os.listdir(path)
    for file in files:
        f.write(path + "/" + file+"\n")

def rem_ext(dir, ext):
    for f in os.listdir(dir):
        if re.search(ext, f):
            os.remove(os.path.join(dir, f))

def create(name,pfolder,nfolder,ratio,num_samples,min_size):
    name = name+"_cascade.xml"
    num_samples = str(num_samples)
    if(ratio>1):
        w = int(20)
        h = int(ratio*20)
    else:
        h = int(20)
        w = int(20/ratio)

    folders = ['pos_train_images','pos_test_images','neg_train_images',
    'neg_test_images','positive_images','negative_images','classifier','samples']

    for folder in folders:
        if os.path.exists(folder):
            shutil.rmtree(folder,ignore_errors=False,onerror=None)

    rem_ext(cwd,".txt")
    # if os.path.exists("positives.txt"): 
    #     os.remove("positives.txt")
    # if os.path.exists("negatives.txt"): 
    #     os.remove("negatives.txt")

    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)

    folders = [cwd+"/"+f for f in folders]

    for filename in glob.glob(os.path.join(pfolder, '*.*')):
        shutil.copy(filename, folders[1])
    for filename in glob.glob(os.path.join(nfolder, '*.*')):
        shutil.copy(filename, folders[3])

    move_some(folders[1],folders[0],30)
    move_some(folders[3],folders[2],1000)

    rs.resize_all(folders[0],h*10,w*10,folders[4])
    rs.resize_all(folders[2],400,400,folders[5])

    create_txt(folders[4],"positives.txt")
    create_txt(folders[5],"negatives.txt")


    # p_str="""'opencv_createsamples -bgcolor 0 -bgthresh 0 -maxxangle 1.1\
    # -maxyangle 1.1 maxzangle 0.5 -maxidev 40 -w """
    # # p_str="positives.txt negatives.txt "+folders[7]+" "+num_samples+" "+p_str
    # p_str=p_str+str(w)+" -h "+str(h)+"'"
    # lis=["perl","createsamples.pl","positives.txt","negatives.txt",cwd+"/samples",num_samples,p_str]
    foldr = os.listdir(folders[4])
    # pipe = subprocess.call(lis,shell=True)
    for file in foldr:
        p_str = "-img "+folders[4]+"/"+file+" -bg negatives.txt -info in.txt -maxxangle 1.0 -maxyangle 1.0 -maxzangle 0.5 -maxidev 40 -num "+num_samples
        args = ["opencv_createsamples"] + p_str.split(" ")
        pipe = subprocess.call(args)
        p_str = "-info in.txt -num "+num_samples+" -w "+str(w)+" -h "+str(h)+" -vec "+folders[7]+"/"+file+".vec"
        args = ["opencv_createsamples"] + p_str.split(" ")
        pipe = subprocess.call(args)
        rem_ext(cwd,".jpg")
    mv.merge_vec_files(folders[7],'samples.vec')

    o_str = """-data classifier -vec samples.vec -bg negatives.txt\
    -numStages 20 -minHitRate 0.999 -maxFalseAlarmRate 0.5 -numPos """+str(num_samples)+"""\
    -numNeg """+str(int(num_samples)/2)+" -w "+str(w)+" -h "+str(h) +""" -mode ALL -precalcValBufSize 1024\
    -precalcIdxBufSize 1024"""
    args=["opencv_traincascade"]+o_str.split()
    pipe = subprocess.call(args)

    # classifiers = os.listdir(folders[6])
    shutil.move(folders[6]+"/cascade.xml",cwd+"/")
    os.rename("cascade.xml",name)

    rem_ext(folders[1],".txt")
    rem_ext(folders[3],".txt")
    ts.tester(cwd+"/"+name,folders[1],folders[3],min_size)


if __name__=='__main__' :
    pfolder,nfolder=get_args()
    # pfolder=input("Positive images folder:")
    # nfolder=input("Negative images folder:")
    create("Taj",pfolder,nfolder,1,100,(100,100))
