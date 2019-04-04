import cv2
import numpy as np
import pywt

cam=cv2.VideoCapture(0)
img_counter =0
while(True):
    # capture frame by frame
    ret, frame=cam.read()

    if not ret:
        break

    k=cv2.waitKey(1)

    if k%256==27: #esc pressed
        print("escape it man")
        break
    elif k%256==32:
        img_name="image_{}.png".format(img_counter)
        cv2.imwrite(img_name,frame)

        print("{} written!!!".format(img_name))
        img_counter+=1
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rows, cols, channel = frame.shape


    M = np.float32([[1, 0, 0], [0, 1, (cols - rows) / 2]])
    im2 = cv2.warpAffine(frame, M, (cols, cols))
    #cv2.imshow('frame_gray', gray)
    #cv2.imshow('frame',frame)


    b, g, r = cv2.split(im2)
    secretKey3col = cv2.imread('secret_key.png')
    secretKey = cv2.cvtColor(secretKey3col, cv2.COLOR_BGR2GRAY)

    def scrambling(channel):
        cof2 = pywt.dwt2(channel, 'haar')
        LL, (LH, HL, HH) = cof2
        cof = LL, (-LH, -HL, -HH)
        return cof


    cof_r = scrambling(r)
    cof_g = scrambling(g)
    cof_b = scrambling(b)

    dt = np.dtype('B')

    # img_r = np.round(pywt.idwt2(cof_r, 'haar')).astype(dt)
    # img_g = np.round(pywt.idwt2(cof_g, 'haar')).astype(dt)
    # img_b = np.round(pywt.idwt2(cof_b, 'haar')).astype(dt)

    img_r = np.round(pywt.idwt2(cof_r, 'haar')).astype(int)
    img_g = np.round(pywt.idwt2(cof_g, 'haar')).astype(int)
    img_b = np.round(pywt.idwt2(cof_b, 'haar')).astype(int)

    img_r = np.clip(img_r, 0, 255).astype(dt)
    img_g = np.clip(img_g, 0, 255).astype(dt)
    img_b = np.clip(img_b, 0, 255).astype(dt)

    img_r_secret = img_r ^ secretKey
    img_g_secret = img_g ^ secretKey
    img_b_secret = img_b ^ secretKey

    encryptedImage = cv2.merge([img_b_secret, img_g_secret, img_r_secret])


    ###############################################################################################################

    #Transmission part

    #############################################################################################################3#
    r, g, b = cv2.split(encryptedImage)

    secretKey3col = cv2.imread('secret_key.png')
    secretKey = cv2.cvtColor(secretKey3col, cv2.COLOR_BGR2GRAY)

    img_r_secret = r ^ secretKey
    img_g_secret = g ^ secretKey
    img_b_secret = b ^ secretKey

    def scrambling(channel):
        cof2 = pywt.dwt2(channel, 'haar')
        LL, (LH, HL, HH) = cof2
        cof = LL, (-LH, -HL, -HH)
        return cof

    cof_r = scrambling(img_r_secret)
    cof_g = scrambling(img_g_secret)
    cof_b = scrambling(img_b_secret)

    img_r = (np.round(pywt.idwt2(cof_r, 'haar')).astype(int))
    img_g = (np.round(pywt.idwt2(cof_g, 'haar')).astype(int))
    img_b = (np.round(pywt.idwt2(cof_b, 'haar')).astype(int))

    img_r = np.clip(img_r, 0, 255).astype(dt)
    img_g = np.clip(img_g, 0, 255).astype(dt)
    img_b = np.clip(img_b, 0, 255).astype(dt)
    decryptedImage = cv2.merge([img_r, img_g, img_b])

    cv2.imshow('Something', im2)
    cv2.imshow('is', encryptedImage)
    cv2.imshow('happening', decryptedImage)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()

