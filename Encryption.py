import cv2 as cv
import matplotlib.pyplot as plt
import pywt
import numpy as np
import time

START_TIME=time.time()

# STEP 1: INPUT IMAGE TO BE ENCRYPTED

img=cv.imread('toBeEncrypted.png')

# STEP 2: GET R,G,B COMPONENTS FROM THE COLOUR IMAGE

b, g, r = cv.split(img)

# STEP 3: GENERATE THE SECRET KEY

secretKey3col=cv.imread('secret_key.png')

# STEP 3a: CONVERT THE GENERATED SECRET KEY TO GRAY SCALE IMAGE

secretKey=cv.cvtColor(secretKey3col, cv.COLOR_BGR2GRAY)
                                                                # print(secretKey.shape)
# STEP 4: HAAR WAVELET TRANSFORM ON EACH CHANNEL OF INPUT IMAGE, THEN SCRAMBLING BY MULTIPLICATION OF HORZ, VERT, DIAG DETAILS WITH -1 AND RETURNING THE APPROPRIATE COEFFICIENTS

def scrambling(channel):
    cof2 = pywt.dwt2(channel, 'haar')
    LL, (LH, HL, HH) = cof2
    cof = LL, (-LH, -HL, -HH)
    return cof

cof_r=scrambling(r)
cof_g=scrambling(g)
cof_b=scrambling(b)

dt = np.dtype('B')

# STEP 5: SECOND SCRAMBLING PROCEDURE USING CHAOTIC MAPS TO BE IMPLEMENTED LATER
#
#

# STEP 6: INVERSE DWT OF THE COEFFICIENTS

img_r=np.round( pywt.idwt2(cof_r, 'haar') ).astype(int)
img_g=np.round( pywt.idwt2(cof_g, 'haar') ).astype(int)
img_b=np.round( pywt.idwt2(cof_b, 'haar') ).astype(int)

img_r = np.clip(img_r, 0, 255).astype(dt)
img_g = np.clip(img_g, 0, 255).astype(dt)
img_b = np.clip(img_b, 0, 255).astype(dt)

# STEP 7: ENCRYPT EACH CHANNEL WITH THE SECRET KEY

img_r_secret=img_r^secretKey
img_g_secret=img_g^secretKey
img_b_secret=img_b^secretKey

# STEP 8: MERGE THE ENCRYPTED CHANNELS
encryptedImage=cv.merge([img_r_secret,img_g_secret,img_b_secret])
cv.imwrite("EncryptedImage.png",encryptedImage)
cv.imshow('encrypted', encryptedImage)

END_TIME=time.time()
print(END_TIME-START_TIME)
