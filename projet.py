import cv2

img = cv2.imread('TurtleD.tif')


cv2.namedWindow('img',cv2.WINDOW_NORMAL) # Can be resized

cv2.imshow('img',img)


cv2.waitKey(0)
