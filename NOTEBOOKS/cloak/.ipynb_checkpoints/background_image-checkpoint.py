import cv2
cap = cv2.VideoCapture(0) #to record from the web cam .my web cam is present on 0 therefore i used 0

while cap.isOpened():
    ret,back=cap.read() ##HERE WE ARE READING FROM THE CAM 
    ##Basically, ret is a boolean regarding whether or not there was a return at all, 
    # at the back is each frame that is returned. 
    # If there is no back, no error is generated simply None is returned
    if ret:
        cv2.imshow("image",back)
        if cv2.waitKey(1)==ord("r"):
            cv2.imwrite('back.jpg',back)##so in back.jpg your background image is saved(the last image when r was pressed)
            break
cap.release()##it releases all the resources of your machine(here camera only)
cv2.destroyAllWindows()
##after running you can see a back.jpg being created
            
