import cv2

a=[item for item in dir(cv2) if "EVENT_" in item]
print(a)
# Open webcam
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Display the resulting frame
    cv2.imshow("Dancing Man (Press q to quit)", frame)

    k = cv2.waitKeyEx(50)
    if k!=-1:
        print(k)


# Release resources
cap.release()
cv2.destroyAllWindows()
