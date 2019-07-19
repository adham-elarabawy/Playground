import numpy as np
import cv2

# --CONFIG--
DEBUG = False
VERSION_NUMBER = 4
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
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
i = 0
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        print(i)
        i += 1
        grayed = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        heq_frame = clahe.apply(grayed)
        #final = cv2.cvtColor(heq_frame, cv2.COLOR_GRAY2RGB)
        (thresh, im_bw) = cv2.threshold(heq_frame, 0,
                                        255, cv2.THRESH_OTSU)
        final = cv2.cvtColor(im_bw, cv2.COLOR_GRAY2BGR)
        cv2.imshow('cvwin', final)
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
