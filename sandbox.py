import cv2
import numpy as np
import easygui

# User Interface
# Q to quit
# M to Mask only areas from cam
# B to blend
# L to load mask
# S to save mask
#  cvR to reset the mask\nUse left mouse button to start drawing areas to mask, easier if in blend mode", title='Expat Audio Optical Inspection ', ok_button='OK', image=None, root=None)



# User set parameters
camerapixwidth = 1280
camerapixheight = 720 # Resolution to be used. this is very camera specific.
SelectedCam = 0 # Which webcam will be used?
UsingWindows = True # Later in the code, this is used to allow directx to talk to webcams (for more resolution flexibility)

easygui.msgbox(msg="Q to quit\nM to Mask only areas from cam\nB to blend\nL to load mask\nS to save mask\nR to reset the mask\nUse left mouse button to start drawing areas to mask, easier if in blend mode", title='Expat Audio Optical Inspection ', ok_button='OK', image=None, root=None)



#Draws a blank canvas for the Mask
masker = np.zeros((camerapixheight, camerapixwidth, 1), dtype=np.uint8)

# System Globals to track settings.
blend = False
show_mask = False
zoom = False
exitplease = False
drag = False
drag_start = (0,0)
drag_end = (0,0)




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
    global drag_start, drag_end, img, patterns, regions, show_regions, show_mask, masker, blend, camerapixwidth, camerapixheight, SelectedCam
    zoom = False

    if UsingWindows == True:
        cap = cv2.VideoCapture(SelectedCam, cv2.CAP_DSHOW) # this uses directshow apparently.
    else:
        cap = cv2.VideoCapture(SelectedCam) # Standard line used in openCV



    cap.set(3, camerapixwidth) #Frame width
    cap.set(4, camerapixheight) #Frame Height
    cv2.namedWindow('ExpatAudio AOI')
    cv2.setMouseCallback('ExpatAudio AOI', on_mouse, 0)



    while (True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2RGBA)

        char = chr(cv2.waitKey(1) & 255)
        if (char == 'q'): # Quit
            break
        elif (char == 27): # Quit
            break
        elif (char == 's'): # Save Current Display
            outputfilename = easygui.filesavebox(msg="Save whatever is on the screen", title="Save as PNG", default='', filetypes="*.png")
            cv2.imwrite(outputfilename, masker) # Saves whatever the mask is to the file
        elif (char == 'l'): # Load Mask from External File
            masktoopen = easygui.fileopenbox(msg=None, title=None, default='*', filetypes=None, multiple=False)
            masker = cv2.imread(masktoopen, 0)
        elif (char == 'r'): # Reset the mask
            masker = np.zeros((720, 1280, 1), dtype=np.uint8)
        elif (char == 'm'): # Show/Not Show Mask
            show_mask = not show_mask
        elif (char == 'b'): # blend
            blend = not blend
        elif (char == 'z'):
            zoom = not zoom

        # This magic line shuts down the app if a user presses the X button in the GUI
        if cv2.getWindowProperty('ExpatAudio AOI', cv2.WND_PROP_VISIBLE) < 1:
            break


            # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if exitplease == True:
            break

        if show_mask == False:
            OutputImage = gray
        elif show_mask == True:
            maskedgray = cv2.bitwise_and(gray, gray, mask=masker)
            OutputImage = maskedgray

        if blend == True:
            alpha = 0.5
            beta = (1.0 - alpha)
            OutputImage = cv2.addWeighted(gray, alpha, masker, beta, 0.0)

        if zoom == True:
            sub = gray[320:454, 544:680]
            ZoomedImage = cv2.resize(sub, (0, 0), fx=4, fy=4)
            cv2.imshow('ZOOM', ZoomedImage)
        else:
            cv2.destroyWindow("ZOOM")

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

