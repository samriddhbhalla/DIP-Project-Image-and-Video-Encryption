import cv2
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
    #cv2.imshow('frame_gray', gray)
    cv2.imshow('frame_colour',frame)




    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()

