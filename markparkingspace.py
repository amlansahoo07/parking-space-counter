import cv2
import pickle

def markParkingSpace():
    """
    Function to mark parking spaces on an image.
    """

    # Approx. width and height of a parking spot estimated by hit n trial
    width, height = 106, 46

    try:
        with open('CarParkPos','rb') as f:
            posList = pickle.load(f)
    except:
        posList = []

    # Handling mouse click event
    def mouseClick(events, x, y, flags, params):
        if events == cv2.EVENT_LBUTTONDOWN:
            print((x,y))
            posList.append((x,y))
        if events == cv2.EVENT_RBUTTONDOWN:
            for i, pos in enumerate(posList):
                x1, y1 = pos
                if x1<x<x1+width and y1<y<y1+height:
                    posList.pop(i)
        
        with open('CarParkPos','wb') as f:
            pickle.dump(posList,f)
        
    while True:
        img = cv2.imread('carParkImg.png')
        for pos in posList:
            cv2.rectangle(img, pt1=pos, pt2=(pos[0]+width,pos[1]+height), color=(255,0,255), thickness=2)
        
        cv2.imshow("Image", img)
        cv2.setMouseCallback("Image", mouseClick)
        key = cv2.waitKey(1)
        if key == ord('q'):  # Press 'q' key to exit
            break

        # Check if the window is still open
        if cv2.getWindowProperty("Image", cv2.WND_PROP_VISIBLE) < 1:
            break
    
    cv2.destroyAllWindows()


if __name__ == "__main__":
    markParkingSpace()