import cv2
import sys

activity = sys.argv[1]

# Create a VideoCapture object and read from input file
cap = cv2.VideoCapture(f'./activities/{activity}/demo.mp4')

# Check if camera opened successfully
if (cap.isOpened()== False): 
    print("Error opening video file")

#vid_playing = True

# Read until video is completed
while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret == True:

        # Display the resulting frame
        winName = "Demo"
        img = cv2.resize(frame, (750,500))
        cv2.namedWindow(winName)
        cv2.moveWindow(winName, 1200, 0)
        cv2.imshow(winName, img)
    
        # Press Q on keyboard to exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    
    # Break the loop
    else: 
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

# When everything done, release 
# the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()
