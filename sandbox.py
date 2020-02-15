import cv2
import numpy as np

# from os import listdir
# from time import time
# from os.path import isfile, join

# black blank image
blank_image = np.zeros(shape=[960, 1280, 3], dtype=np.uint8)

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 960)

show_mask = 0

# mask = cv2.imread("mask.png",0)
# cv2.namedWindow('ExpatAudio AOI')

while (True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    char = chr(cv2.waitKey(1) & 255)
    if (char == 'q'):
        break
    elif (char == 27):
        break
    #elif (char == 't'):
    #    cv2.imwrite("output.jpg", img)
    #elif (char == 'd'):
    #    show_regions = not show_regions
    elif (char == 's'):
        show_mask = not show_mask
    #elif (char == 'z'):
    #    zoom = not zoom



    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # diff = cv2.bitwise_and(gray,gray,mask=mask)
    #diff = gray
    #diff = blank_image

    if show_mask == 0:
        OutputImage = gray
    elif show_mask == 1:
        OutputImage = blank_image

    # Display the resulting frame
    cv2.imshow('ExpatAudio AOI', OutputImage)


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
