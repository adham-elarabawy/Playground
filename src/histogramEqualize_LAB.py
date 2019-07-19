import numpy as np
import cv2

# --CONFIG--
DEBUG = False
VERSION_NUMBER = 3
video_name = 'nutri_bar.mkv'
video_path = '/Users/adhamelarabawy/Documents/Kelzal/test_videos/' + video_name

# create writer object
fileName = str(VERSION_NUMBER) + 'aheq_' + video_name[:-4] + '.avi'
imgSize = (1280, 800)
frame_per_second = 25.0
writer = cv2.VideoWriter(fileName, cv2.VideoWriter_fourcc(
    *"MJPG"), frame_per_second, imgSize)

# start video capture
cap = cv2.VideoCapture(video_path)
i = 0
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        print(i)
        i += 1
        # -----Converting image to LAB Color model-----------------------------------
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        cv2.imshow("lab", lab)

        # -----Splitting the LAB image to different channels-------------------------
        l, a, b = cv2.split(lab)
        if DEBUG:
            cv2.imshow('l_channel', l)
            cv2.imshow('a_channel', a)
            cv2.imshow('b_channel', b)

        # -----Applying CLAHE to L-channel-------------------------------------------
        clahe = cv2.createCLAHE(clipLimit=1.0, tileGridSize=(8, 8))
        cl = clahe.apply(l)
        cv2.imshow('CLAHE output', cl)

        # -----Merge the CLAHE enhanced L-channel with the a and b channel-----------
        limg = cv2.merge((cl, a, b))
        if DEBUG:
            cv2.imshow('limg', limg)

        # -----Converting image from LAB Color model to RGB model--------------------
        final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

        # grayed = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # heq_frame = clahe.apply(grayed)
        # cv2.imshow('cvwin', heq_frame)
        # final = cv2.cvtColor(heq_frame, cv2.COLOR_GRAY2RGB)
        writer.write(final)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # press q to quit
            print("quit succcessfully")
            break
    else:
        print("finished successfully... quit")
        break

# When everything done, release the capture
cap.release()
writer.release()
cv2.destroyAllWindows()
