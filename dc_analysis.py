import numpy as np
import cv2

# Read the video in the current directory
cap = cv2.VideoCapture('2009-06-24-002.mp4')

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if ret == True: # When frame is captured

        # Image operation
        # 1. BGR to gray 2. Smoothness 3. Edging 4. Hough transformation
        # Some parameters are experimental based

        # Create frame in gray
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Blur the frame with Gaussian filter
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)
        # Detect edge using Canny operator
        edged = cv2.Canny(gray, 150, 350, apertureSize=3)
        # Contour lines with Hough transformation
        lined = cv2.HoughLines(edged, 1, np.pi / 180, 120)  # Step length and threshold lined for the last two
        # parameters.

        # Discard the extreme and draw the line
        result = frame.copy()
        for line in lined[0]:
            rho = line[0]  # Fist parameter for radius in polar coordinate
            theta = line[1]  # Second parameter for angle in polar coordinate
            print rho
            print theta
	    if ((theta < 1.05) or (theta > 1.9)): # Decide by Supposing the line detected is the border of lane
                cv2.imshow('Detection Winsows',edged) # Edging the frame if out of lane
            elif (theta < (np.pi / 4.)) or (theta > (3. * np.pi / 4.)):  # Vertical line
                pt1 = (int(rho / np.cos(theta)), 0)  # The cross point of the line and first row
                pt2 = (int((rho - result.shape[0] * np.sin(theta)) / np.cos(theta)), result.shape[0])  # The cross point
                #  of the line and last row
                cv2.line(result, pt1, pt2, (255))  # Draw a white line
                # Display the edging frame
                cv2.imshow('Detection Winsows', frame)
            else:  # Horizontal line
                pt1 = (0, int(rho / np.sin(theta)))
                pt2 = (result.shape[1], int((rho - result.shape[1] * np.cos(theta)) / np.sin(theta)))
                cv2.line(result, pt1, pt2, (255), 1)
        	# Display the edging frame
                cv2.imshow('Detection Winsows', frame)
        if cv2.waitKey(10) == 27:
            break
        # Display the resulting frame
        cv2.imshow('Result', result)
    else:
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
