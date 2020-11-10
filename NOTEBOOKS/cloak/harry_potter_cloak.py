import cv2
import numpy as np

cap=cv2.VideoCapture(0)
back = cv2.imread("./back.jpg")##returns BGR
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))
while cap.isOpened():
    ret,frame=cap.read()
    if ret:
        hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        blue=np.uint8([[[255,0,0]]])##bgr value of blue
        hsv_blue=cv2.cvtColor(blue,cv2.COLOR_BGR2HSV)
        #print(hsv_blue)##[[[120 255 255]]]
        lower_blue=np.array([0,100,100])
        upper_blue=np.array([130,255,255])
        mask=cv2.inRange(hsv,lower_blue,upper_blue)
        part1=cv2.bitwise_and(back,back,mask=mask)
        ##(src1, src2[, dst[, mask]])
        mask=cv2.bitwise_not(mask)
        part2=cv2.bitwise_and(frame,frame,mask=mask)
        out.write(part1+part2)
        cv2.imshow("cloak",part1+part2)
    if cv2.waitKey(1)==ord("r"):
        break
cap.release()
cv2.destroyAllWindows()
