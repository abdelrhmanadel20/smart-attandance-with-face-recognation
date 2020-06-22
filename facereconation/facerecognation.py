# -*- coding: utf-8 -*-
"""Copy of facerecognation.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DvRi8pd2h2txhpDxUwKgMD2HCVN9Rnn4

imports
"""

import numpy as np
import os.path

"""aline faces"""

import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from align import AlignDlib

# %matplotlib inline

def load_image(path):
    img = cv2.imread(path, 1)
    # OpenCV loads images with color channels
    # in BGR order. So we need to reverse them
    return img[...,::-1]
def align_image(img):
    return alignment.align(96, img, alignment.getLargestFaceBoundingBox(img), 
                           landmarkIndices=AlignDlib.OUTER_EYES_AND_NOSE)

"""load model"""

def load_model():
  import pickle
 
  model_pkl = open("svc_model.pkl", "rb")

  # Reading the model
  model = pickle.load(model_pkl)
  return model

"""load data"""

metadata=np.load("meta.npz",allow_pickle=True)['meta']
pepole=np.load("meta.npz",allow_pickle=True)['pepole']
embedded=np.load("meta.npz",allow_pickle=True)['embedded']

from sklearn.preprocessing import LabelEncoder
encoder = LabelEncoder()

encoder.fit(pepole)

"""preprocessing images"""

def distance(emb1, emb2):
    return np.sum(np.square(emb1 - emb2))

def similarity(v1, v2):
    n1 = np.linalg.norm(v1)
    n2 = np.linalg.norm(v2)
    x1 = np.squeeze(np.asarray(v1))

    x2 = np.squeeze(np.asarray(v2))
    return np.dot(x1,x2, out=None) / n1 / n2

from PIL import Image
import face_recognition
def face_detector(img_path):
  faces=[]
  image = face_recognition.load_image_file(img_path)
  


# Find all the faces in the image using a pre-trained convolutional neural network.
# This method is more accurate than the default HOG model, but it's slower
# unless you have an nvidia GPU and dlib compiled with CUDA extensions. But if you do,
# this will use GPU acceleration and perform well.
# See also: find_faces_in_picture.py
  face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=0, model="cnn")

  if(len(face_locations)):
       for face_location in face_locations:
          
       # Print the location of each face in this image
          top, right, bottom, left = face_location
      
    # You can access the actual face itself like this:
          face_image = image[top:bottom, left:right]
      
          faces.append(face_image)
      
      return faces,image

def image_recognizer(img,model,nn4_small2_pretrained):
  
  pepole=np.load("meta.npz",allow_pickle=True)['pepole']
  from sklearn.preprocessing import LabelEncoder
  encoder = LabelEncoder()

  encoder.fit(pepole)
 

  image = align_image(img)
  if(image is not None):
    image = (image / 255.).astype(np.float32)
    emb = nn4_small2_pretrained.predict(np.expand_dims(image, axis=0))
 
    image_pred = model.predict(emb)
  
    
    image_identity = encoder.inverse_transform(image_pred)[0]
  
       
 
    
  else:
    image_identity='none'
  return image_identity,image