import cv2 as cv
import numpy as np
import time
import matplotlib.pyplot as plt
START_TIME=time.time()
# STEP 1: READ INPUT IMAGE
# img = cv.imread('image_0.jpg')
# img = cv.imread('image_1.jpg')

img = cv.imread('image_2x.png')
# STEP 2: EXTRACT THE FEATURES OF IMAGE - NOS ROWS, COLUMNS, CHANNELS
rows, cols , channel = img.shape
if(cols%2==1):
    img = img[0:rows, 0:cols-1]

rows, cols , channel = img.shape
# STEP 3: CONVERT THE IMAGE TO A SQUARE IMAGE BY ZERO PADDING
M = np.float32([[1, 0, 0], [0, 1, (cols - rows) / 2]])  # tx is the conventional x axis corresponding to no of columns
im2 = cv.warpAffine(img, M, (cols, cols))               # since col>rows; else use rows
rows2, cols2, channel2 = im2.shape                      # confirm whether nos rows and cols are equal in number
                                                        # print(rows2,cols2,channel)
cv.imwrite('toBeEncrypted.png',im2)

# STEP 4: ROTATE COLOUR IMAGE TO 3 DIFFERENT DIRECTIONS
M_r= cv.getRotationMatrix2D(((cols2 - 1) / 2.0, (rows2 - 1) / 2.0), -90, 1)
imr=cv.warpAffine(im2, M_r, (rows2, cols2))
M_l= cv.getRotationMatrix2D(((cols2 - 1) / 2.0, (rows2 - 1) / 2.0), +90, 1)
iml=cv.warpAffine(im2, M_l, (rows2, cols2))
M_d= cv.getRotationMatrix2D(((cols2 - 1) / 2.0, (rows2 - 1) / 2.0), 180, 1)
imd=cv.warpAffine(im2, M_d, (rows2, cols2))
                                                        # cv.imshow('img_r', imr)
                                                        # cv.waitKey(0)
                                                        # cv.imshow('img_l', iml)
                                                        # cv.waitKey(0)
                                                        # cv.imshow('img_d', imd)
                                                        # cv.waitKey(0)
                                                        # cv.destroyAllWindows()
                                                        # random cutting and shuffling of images:
                                                        # we are cutting the rows and not indivisual pixals

# STEP 5: RANDOM CUTTING OF IMAGE ALONG ROWS ON ALL THE 4 AUGMENTED IMAGES
np.random.shuffle(im2)
np.random.shuffle(imr)
np.random.shuffle(iml)
np.random.shuffle(imd)
                                                        # cv.imshow('img_2', im2)
# cv.waitKey(0)
# cv.destroyAllWindows()

# STEP 6: GENERATE THE PRIMARY KEY BY PERFORMING XOR OPERATION ON ALL 4 AUGMENTED IMAGES TO OBTAIN A PRIMARY KEY
dst1 = cv.bitwise_xor(im2, imr)
dst2 = cv.bitwise_xor(iml, imd)
primaryKey = cv.bitwise_xor(dst1, dst2)

# STEP 7: SPLIT THE PRIMARY KEY IN TO ITS R, B, G COMPONENTS
b, g, r = cv.split(primaryKey)
                                                        # cv.imshow('dst1', primaryKey)
""" Alternate way to simply flip channel 
# def flipper(channel):
#     channel_ltr=cv.flip(channel,1)
#     channel_utd=cv.flip(channel,0)
#     channel_tra=cv.flip(channel,-1)
#     return channel_ltr^channel_tra^channel_utd
"""
# creating a lambda function that flips input in 3 direction
x = lambda channel: cv.flip(channel, 1) ^ cv.flip(channel, 0) ^ cv.flip(channel, -1)
# creating a lambda function that rotates the channel and then flips in 3 direction
y = lambda b: x(b) ^ x(cv.rotate(b, 0))

# STEP 8: USE THE LAMBDA FUNCTION IN ALL THREE CHANNELS
b1 = y(b)
g1 = y(g)
r1 = y(r)


# STEP 9: OBTAIN SECRET KET BY XOR LOGIC
key = (b1 ^ b) ^ (g1 ^ g) ^ (r1 ^ r)

cv.imshow('dst1', key)
cv.imwrite('secret_key.png', key)

END_TIME=time.time()
print(END_TIME-START_TIME)



