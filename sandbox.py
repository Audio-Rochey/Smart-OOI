import cv2
import numpy as np

# from os import listdir
# from time import time
# from os.path import isfile, join

# black blank image
#blank_image = np.zeros(shape=[720, 1280, 3], dtype=np.uint8)
#masker = blank_image
masker = np.zeros((720, 1280, 1), dtype=np.uint8)

# Adds a white rectangle into the mask. (image, start cord, end cord, color, line width where -1 means fill



show_mask = False
exitplease = False
drag = False
drag_start = (0,0)
drag_end = (0,0)

#masker = cv2.imread("mask.png",0)
# cv2.namedWindow('ExpatAudio AOI')


def on_mouse(event, x, y, flags, params):
    global drag, drag_start, drag_end, img, patterns, regions, exitplease, masker

    if event == cv2.EVENT_RBUTTONDOWN:
        exitplease = 1


    if event == cv2.EVENT_LBUTTONDOWN:
        drag_start = (x, y)
        drag_end = (x, y)
        print(drag_start)
        print(drag_end)
        drag = True

    elif event == cv2.EVENT_LBUTTONUP:
        drag = False
        drag_end = (x, y)
        print(drag_start)
        print(drag_end)
        cv2.rectangle(masker, drag_start, drag_end, (255, 255, 255), -1)

    elif event == cv2.EVENT_MOUSEMOVE and drag == True:
        drag_end = (x, y)
        print(drag_start)
        print(drag_end)


def show_webcam():
    global drag_start, drag_end, img, patterns, regions, show_regions, show_mask, masker
    zoom = False
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280) #Frame width
    cap.set(4, 720) #Frame Height
    cv2.namedWindow('ExpatAudio AOI')
    cv2.setMouseCallback('ExpatAudio AOI', on_mouse, 0)



    while (True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2RGBA)

        char = chr(cv2.waitKey(1) & 255)
        if (char == 'q'): # Quit
            break
        elif (char == 27): #Quit
            break
        elif (char == 's'): #Save Current Display
            cv2.imwrite("output.jpg", OutputImage)
        elif (char == 'l'): #Load Mask from External File
            masker = cv2.imread("mask2.png", 0)
        elif (char == 'r'): # Reset the mask
            masker = np.zeros((720, 1280, 1), dtype=np.uint8)
        elif (char == 'm'): #Show/Not Show Mask
            show_mask = not show_mask
        #elif (char == 'z'):
        #    zoom = not zoom



        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if exitplease == True:
            break

        if show_mask == False:
            OutputImage = gray
        elif show_mask == True:
            maskedgray = cv2.bitwise_and(gray, gray, mask=masker)
            OutputImage = maskedgray

        # Display the resulting frame
        cv2.imshow('ExpatAudio AOI', OutputImage)


    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


def main():
    print("Hello World!")
    show_webcam()


if __name__ == "__main__":
    main()

