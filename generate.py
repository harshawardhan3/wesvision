import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Model
import os
import numpy as np
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt

#yao
from globalVar import * 
from filterImages import *
from read_select_files import *

tf.__version__

def generate(blur_threshold, glare_threshold):
    trained_model = load_model('model/blur/blur_detect.h5') 
    glareCNN = tf.keras.models.load_model('model/glare/glare_detect.h5')
    source_dir = "data2/"

    buffr_blur = []
    score_blur = []
    pred_blur = [] #blur status of images 


    buffr_glare=[]
    pred_glare=[] #glare status 
    score_glare=[]

    name=[]

    image_array=[]
    for i in os.listdir(source_dir):
        if not i.startswith("destination"):
            continue

        #blur check 
        img = tf.keras.preprocessing.image.load_img(source_dir+i,target_size = (128,128))
        x = tf.keras.preprocessing.image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        
        classes = trained_model.predict(x/255)
        buffr_blur.append(img)
        score_blur.append(classes)
        name.append(i)
        if classes[0][0]<int(blur_threshold.get())/100: #change blur threshhold here
            pred_blur.append("blur")
        else:
            pred_blur.append("not blur")


        #glare check    
        test_image1 = tf.keras.preprocessing.image.load_img(source_dir+i, target_size = (64,64))
        test_image2 = tf.keras.preprocessing.image.img_to_array(test_image1) #convert PIL image to array
        test_image2 = np.expand_dims(test_image2, axis = 0) #expand image dimensions to make it compatible with CNN input
        glare = glareCNN.predict(test_image2/255) #Values in the array scaled from [0,255] -> [0,1]

        score_glare.append(glare) 
        if glare[0][0] <int(glare_threshold.get())/100: #CNN model refers to 0 as "glare" and 1 as "not glare", applying a threshold for both cases.Change threshhold here
            pred_glare.append("glare")
        else:
            pred_glare.append("not glare") 


    for k in range(len(name)):
        image_array.append([name[k],pred_blur[k],pred_glare[k]])


    ##generate videos
    g_rows = transform_to_rows(name, pred_blur, pred_glare)
    filter_files(g_rows, f"{g_file_dir}/time.txt")
    print("filter_finish")

    select_and_make_video(g_file_dir, g_start_time, g_end_time)
    print("video_generated")