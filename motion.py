import cv2
import os
import MySQLdb as sql
import motion as mt
import time

# Establish a connection to MySQL
db = sql.connect(
    host="localhost",
    user="root",
    password="Superstar@123",
    database="motiondet"
)


def save_snapshot(image_path):
    # Save the image path in the database
    cursor = db.cursor()
    query = "INSERT INTO snapshots (image_path) VALUES (%s)"
    values = (image_path,)
    cursor.execute(query, values)
    db.commit()

# Create the 'images' directory if it doesn't exist
image_directory = "/home/akms/motion"
if not os.path.exists(image_directory):
	os.makedirs(image_directory)

def motion_track():
	os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
	os.environ["QT_SCREEN_SCALE_FACTORS"] = "1"
	os.environ["QT_SCALE_FACTOR"] = "1"


	# Initialize the video capture
	cap = cv2.VideoCapture(0)

	# Create a background subtractor object
	fgbg = cv2.createBackgroundSubtractorMOG2()

	# Loop through the video frames
	while True:
	    # Read the current frame
	    ret, frame = cap.read()
	    
	    # Apply the background subtraction
	    fgmask = fgbg.apply(frame)
	    
	    # Perform morphological operations to remove noise
	    fgmask = cv2.erode(fgmask, None, iterations=2)
	    fgmask = cv2.dilate(fgmask, None, iterations=2)
	    
	    #cv2.imshow('Motion Tracking', fgmask)
	    # Find contours of the foreground objects
	    contours, hierarchy = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	    
	    # Iterate through the contours and track the motion
	    for contour in contours:
	        motion_detected = False
	        # Filter out small contours
	        if cv2.contourArea(contour) < 4500:
	            continue
		

	        # Compute the bounding box for the contour
	        (x, y, w, h) = cv2.boundingRect(contour)
		
	        # Draw the bounding box on the frame
	        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

	        motion_detected = True
		
	    # If motion is detected, save the snapshot
	    if motion_detected:
	        # Generate a unique filename for the image
	        timestamp = str(int(time.time()))
	        image_filename = f"{timestamp}.jpg"
	        image_path = os.path.join(image_directory, image_filename)

	        # Save the snapshot image
	        cv2.imwrite(image_path, frame)

	        # Save the image path in the database
	        save_snapshot(image_path)

	        # Pause for 2000 milliseconds (2 seconds)
	        time.sleep(2)

	        # Display the resulting frame
	        cv2.imshow('Motion Tracking', frame)
	    
	        # Exit the loop when 'q' is pressed
	        if cv2.waitKey(1) & 0xFF == ord('q'):
	            break

	# Release the video capture and close all windows
	cap.release()
	cv2.destroyAllWindows()

