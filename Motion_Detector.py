import cv2 

def motionDetection():
    # define a video capture object
    vid = cv2.VideoCapture(0)
    
    
    # Capture the two video frame
    # by frame
    ret, frame1 = vid.read()
    ret, frame2 = vid.read()
    
    # Infinite loop starts here :-
    while vid.isOpened():
        # Comparing the two frames using absdiff
        diff = cv2.absdiff(frame1, frame2)
        
        # Convert the diff colour space to gray
        diffGray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        
        # blur or smoothen diffGray
        blur = cv2.GaussianBlur(diffGray, (5, 5), 0)
        
        # Threshold function applied to blur
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        
        # Dilate the output of the Threshold function
        dilated = cv2.dilate(thresh, None, iterations=3)
        
        # Extracting the contours from the image
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        # loop to form rectangles aroun the parts where motion is detected
        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)
            if cv2.contourArea(contour) < 900:
                continue
            cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame1, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,1, (255, 0, 0), 3)
            
        # Display the Frame1  
        cv2.imshow("Motion Detector", frame1)
        
        # Moving to the next frame for Motion dectection
        frame1 = frame2
        ret, frame2 = vid.read()
        
        # the 'q' button is set as the
        # quitting button you may use any
        # desired button of your choice
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    vid.destroyAllWindows()


if __name__ == "__main__":
    motionDetection()
    
