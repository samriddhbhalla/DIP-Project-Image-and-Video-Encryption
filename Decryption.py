import cv2 as cv
import pywt
import numpy as np
import time
START_TIME = time.time()
# STEP 1: INPUT IMAGE TO BE DECRYPTED
img = cv.imread('EncryptedImage.png')

# STEP 2: GET R,G,B COMPONENTS FROM THE COLOUR IMAGE
r, g, b = cv.split(img)

# STEP 3: GENERATE THE SECRET KEY
secretKey3col = cv.imread('secret_key.png')
secretKey = cv.cvtColor(secretKey3col, cv.COLOR_BGR2GRAY)

# STEP 7: DECRYPT EACH CHANNEL WITH THE SECRET KEY
img_r_secret = r ^ secretKey
img_g_secret = g ^ secretKey
img_b_secret = b ^ secretKey

# STEP 4: HAAR WAVELET TRANSFORM ON EACH CHANNEL OF INPUT IMAGE, THEN SCRAMBLING BY MULTIPLICATION OF HORZ, VERT, DIAG DETAILS WITH -1 AND RETURNING THE APPROPRIATE COEFFICIENTS


def scrambling(channel):
    cof2 = pywt.dwt2(channel, 'haar')
    LL, (LH, HL, HH) = cof2
    cof = LL, (-LH, -HL, -HH)
    return cof


cof_r = scrambling(img_r_secret)
cof_g = scrambling(img_g_secret)
cof_b = scrambling(img_b_secret)

# STEP 5: SECOND DE-SCRAMBLING PROCEDURE USING CHAOTIC MAPS TO BE IMPLEMENTED LATER
#
#

# STEP 6: INVERSE DWT OF THE COEFFICIENTS
img_r = (np.round(pywt.idwt2(cof_r, 'haar')).astype(int))
img_g = (np.round(pywt.idwt2(cof_g, 'haar')).astype(int))
img_b = (np.round(pywt.idwt2(cof_b, 'haar')).astype(int))
dt = np.dtype('B')
img_r = np.clip(img_r, 0, 255).astype(dt)
img_g = np.clip(img_g, 0, 255).astype(dt)
img_b = np.clip(img_b, 0, 255).astype(dt)

# STEP 8: MERGE THE ENCRYPTED CHANNELS
decryptedImage = cv.merge([img_b, img_g, img_r])
cv.imwrite("DecryptedImage.png", decryptedImage)
cv.imshow('Decrypted', decryptedImage)
END_TIME = time.time()

# diff=cv.absdiff(decryptedImage,cv.imread('image_0.jpg'))
# cv.imshow('x',diff*100)
print(END_TIME-START_TIME)
cv.waitKey(0)
