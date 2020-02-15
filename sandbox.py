import cv2
import numpy as np

# from os import listdir
# from time import time
# from os.path import isfile, join

# black blank image
#blank_image = np.zeros(shape=[720, 1280, 3], dtype=np.uint8)
#masker = blank_image
masker = np.zeros((720, 1280, 1), dtype=np.uint8)
cv2.rectangle(masker,(100,200),(400,600),(255,255,255),-1)
# Adds a white rectangle into the mask. (image, start cord, end cord, color, line width where -1 means fill

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

show_mask = 0

#masker = cv2.imread("mask.png",0)
# cv2.namedWindow('ExpatAudio AOI')

while (True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2RGBA)

    char = chr(cv2.waitKey(1) & 255)
    if (char == 'q'):
        break
    elif (char == 27):
        break
    elif (char == 's'):
        cv2.imwrite("output.jpg", OutputImage)
    elif (char == 'l'):
        masker = cv2.imread("mask.png", 0)
    elif (char == 'm'):
        show_mask = not show_mask
    #elif (char == 'z'):
    #    zoom = not zoom



    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    if show_mask == 0:
        OutputImage = gray
    elif show_mask == 1:
        maskedgray = cv2.bitwise_and(gray, gray, mask=masker)
        OutputImage = maskedgray

    # Display the resulting frame
    cv2.imshow('ExpatAudio AOI', OutputImage)


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
