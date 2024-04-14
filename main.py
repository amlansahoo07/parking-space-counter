# Import necessary libraries
import cv2
import pickle
import numpy as np
import argparse
from markparkingspace import markParkingSpace

# Function definition borrowed from cvzone library by Computer Vision Zone
# Website: https://www.computervision.zone/
def putTextRect(img, text, pos, scale=3, thickness=3, colorT=(255, 255, 255),
                colorR=(255, 0, 255), font=cv2.FONT_HERSHEY_PLAIN,
                offset=10, border=None, colorB=(0, 255, 0)):
    """
    Creates Text with Rectangle Background
    :param img: Image to put text rect on
    :param text: Text inside the rect
    :param pos: Starting position of the rect x1,y1
    :param scale: Scale of the text
    :param thickness: Thickness of the text
    :param colorT: Color of the Text
    :param colorR: Color of the Rectangle
    :param font: Font used. Must be cv2.FONT....
    :param offset: Clearance around the text
    :param border: Outline around the rect
    :param colorB: Color of the outline
    :return: image, rect (x1,y1,x2,y2)
    """

    # Extract position coordinates
    ox, oy = pos
    # Calculate text size and position
    (w, h), _ = cv2.getTextSize(text, font, scale, thickness)
    x1, y1, x2, y2 = ox - offset, oy + offset, ox + w + offset, oy - h - offset

    # Draw rectangle with text
    cv2.rectangle(img, (x1, y1), (x2, y2), colorR, cv2.FILLED)
    if border is not None:
        cv2.rectangle(img, (x1, y1), (x2, y2), colorB, border)
    cv2.putText(img, text, (ox, oy), font, scale, colorT, thickness)

    return img, [x1, y2, x2, y1]

def CheckParkingSpace(imgProcessed, img, posList, width, height):
    """
    Check the status of parking spaces based on image processing.
    :param imgProcessed: Processed image containing thresholded parking spots.
    :param img: Original image.
    :param posList: List of parking spot positions.
    :param width: Width of parking spots.
    :param height: Height of parking spots.
    """
    
    spaceCounter = 0
    
    # Iterate through each parking spot
    for pos in posList:
        x,y = pos
        # Crop the parking spot from the processed image
        imgCrop = imgProcessed[y:y+height, x:x+width]
        # cv2.imshow(str(x*y),imgCrop) # Display cropped spots

        # Count non-zero pixels in the cropped image
        count = cv2.countNonZero(imgCrop)

        # Determine color and thickness based on occupancy
        if count < 850:
            color = (0,255,0) # Green for empty space
            thickness = 4
            spaceCounter += 1
        else:
            color = (0,0,255) # Red for occupied space
            thickness = 2

        # Display count and rectangle on the original image
        putTextRect(img, str(count), (x,y+height-3), scale=1, thickness=2, offset=0, colorR=color)
        cv2.rectangle(img, pt1=pos, pt2=(pos[0]+width,pos[1]+height), color=color, thickness=thickness)
    
    # Display total free spaces
    putTextRect(img, f"Free: {spaceCounter}/{len(posList)}", (100,50), scale=3, thickness=4, offset=20, colorR=(0,200,0))

# Main function
def main(args):
    # Video feed
    cap = cv2.VideoCapture('carPark.mp4')

    # Mark parking spaces based on cmdline argument
    if args.mode == "generate":
        markParkingSpace()
    
    # Loading the pre-trained weights
    with open('CarParkPos','rb') as f:
        posList = pickle.load(f)

    # Approx. width and height estimated by hit n trial
    width, height = 106, 46 
        
    while True:
        # Reset video feed to the beginning when it reaches the end
        if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            cap.set(cv2.CAP_PROP_POS_FRAMES,0) # Reset the final frame to zero for a loop

        # Applying image processing techniques
        success, img = cap.read()
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray, (3,3), 1)
        imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
        imgMedian = cv2.medianBlur(imgThreshold, 5)
        imgDilate = cv2.dilate(imgMedian, kernel=np.ones((3,3), np.uint8), iterations=1)

        # Checking availibility of parking space
        CheckParkingSpace(imgDilate, img, posList, width, height)
        
        # Display the processed image
        cv2.imshow("Image", img)
        # cv2.imshow("ImageBlur", imgBlur)
        # cv2.imshow("ImageThresh", imgThreshold)
        # cv2.imshow("ImageMedian", imgMedian)
        # cv2.imshow("ImgDilate", imgDilate)

        key = cv2.waitKey(10)
        if key == ord('q'):  # Press 'q' key to exit
            break

        # Check if the window is still open
        if cv2.getWindowProperty("Image", cv2.WND_PROP_VISIBLE) < 1:
            break

    # Release video capture and destroy windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Specify mode of operation to load weights')
    parser.add_argument('--mode', default='load', choices=['load', 'generate'],
                        help="Specify 'load' to load pre-trained weights or 'generate' to generate weights.")
    args = parser.parse_args()
    try:
        main(args)
    except KeyboardInterrupt:
        print("Program terminated by Keyboard interrupt")