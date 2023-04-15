import cv2

cap = cv2.VideoCapture(0)
trainedFaceData = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
trainedEyeData = cv2.CascadeClassifier("haarcascade_eye.xml")
trainedSmileData = cv2.CascadeClassifier("haarcascade_smile.xml")


while True:
    # Read a frame from the camera
    (ret, frame) = cap.read()

    if not ret:
        break        

    #turns image to grayscale
    grayScaleImg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #detect face, detected objects are returned as a list of rectangles   
    faces = trainedFaceData.detectMultiScale(grayScaleImg)
    

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (100, 200, 50), 4)

        theFace = frame[y:y+h , x:x+w]

        faceGreyscale = cv2.cvtColor(theFace, cv2.COLOR_BGR2GRAY)

        smiles = trainedSmileData.detectMultiScale(faceGreyscale, scaleFactor = 1.7, minNeighbors = 20)
        eyes = trainedEyeData.detectMultiScale(faceGreyscale)

        if len(smiles)>0:
            x_, y_, w_, h_ = smiles[0]
            cv2.rectangle(theFace, ( x_ , y_ ), (x_ + w_ , y_+ h_), (50, 50, 200), 4)
            cv2.putText(frame, "smiling", (x, y+h+40), fontScale = 3, 
            fontFace=cv2.FONT_HERSHEY_PLAIN, color = (255,255,255))

    cv2.imshow("why so serious", frame)

    cv2.waitKey(1)

cap.release
cv2.destroyAllWindows()