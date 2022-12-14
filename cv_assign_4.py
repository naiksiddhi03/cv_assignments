# -*- coding: utf-8 -*-
"""CV_ASSIGN_4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xg06cVQn8DAep8Po58eS9g7wEF2K33zm
"""

import cv2
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from random import randrange

#from google.colab.patches import cv2_imshow

img_ = cv2.imread('C:/Users/lenovo/Desktop/cv2/ass4/left.jpeg')
img1 = st.cvtColor(img_,cv2.COLOR_BGR2GRAY)
img = cv2.imread('C:/Users/lenovo/Desktop/cv2/ass4/right.jpeg')
img2 = st.cvtColor(img,cv2.COLOR_BGR2GRAY)

st.text('input image: left')
st.image([img_])
st.text('input image : right')
st.image([img])

sift = cv2.xfeatures2d.SIFT_create()
# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)

bf = cv2.BFMatcher()
matches = bf.knnMatch(des1,des2, k=2)

# Apply ratio test
good = []
for m in matches:
  if m[0].distance < 0.5*m[1].distance:
    good.append(m)
matches = np.asarray(good)

if len(matches[:,0]) >= 4:
  src = np.float32([ kp1[m.queryIdx].pt for m in matches[:,0] ]).reshape(-1,1,2)
  dst = np.float32([ kp2[m.trainIdx].pt for m in matches[:,0] ]).reshape(-1,1,2)
  H, masked = cv2.findHomography(src, dst, cv2.RANSAC, 5.0)

else:
  raise AssertionError('Can’t find enough keypoints.')

""" image panorama output  """
dst = cv2.warpPerspective(img_,H,(img.shape[1] + img_.shape[1], img.shape[0]))
plt.subplot(122)
st.title("Warped Image")
st.image([dst])
#plt.show()
plt.figure()
dst[0:img.shape[0], 0:img.shape[1]] = img
st.title('output image')
st.image([dst])
#plt.show()
