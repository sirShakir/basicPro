import numpy as np
import cv2
import os.path

videoString = 'videoCapture#'
videoInt = 0
videoName = videoString + str(videoInt)

while os.path.isfile(videoName + '.avi'):
    videoInt = videoInt + 1
    videoName = videoString + str(videoInt)

videoName = videoName + '.avi'


cap = cv2.VideoCapture(0)
firstFrame = None
isRecording = False
fourcc = cv2.VideoWriter_fourcc(*'XVID')
#out = cv2.VideoWriter(videoName + 'avi',fourcc, 20.0, (640,480))
out = cv2.VideoWriter(videoName,fourcc, 20.0, (640,480))


while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (1, 21), 0)

    # if the first frame is None, initialize it
    if firstFrame is None:
            firstFrame = gray
            continue

    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
    
    if thresh.any() and isRecording == False:
        #print(thresh.any())
        #print(counterA)
        isRecording = True
    elif thresh.any() == False:
        #print("False")
        isRecording = False
            
    if isRecording == True:
        #print("Ca Ca Ka Crazy!!!")
        out.write(frame)

    # Display the resulting frame
    cv2.imshow('frame',gray)
    cv2.imshow('thresh',thresh)
    firstFrame = gray.copy()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()