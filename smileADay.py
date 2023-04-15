import cv2
from kivy.app import App
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivy.clock import Clock

cap = cv2.VideoCapture(0)
trainedFaceData = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
trainedSmileData = cv2.CascadeClassifier("haarcascade_smile.xml")


class SmileDetectorApp(App):
    def build(self):
        self.img = Image()
        Clock.schedule_interval(self.update, 1.0 / 30.0) # Update at 30 FPS
        return self.img

    def update(self, dt):
        # Read a frame from the camera
        ret, frame = cap.read()

        if not ret:
            return

        # Turn image to grayscale
        grayScaleImg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect face, detected objects are returned as a list of rectangles
        faces = trainedFaceData.detectMultiScale(grayScaleImg)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (100, 200, 50), 4)

            theFace = frame[y:y + h, x:x + w]

            faceGreyscale = cv2.cvtColor(theFace, cv2.COLOR_BGR2GRAY)

            smiles = trainedSmileData.detectMultiScale(faceGreyscale, scaleFactor=1.7, minNeighbors=20)

            if len(smiles) > 0:
                x_, y_, w_, h_ = smiles[0]
                cv2.rectangle(theFace, (x_, y_), (x_ + w_, y_ + h_), (50, 50, 200), 4)
                cv2.putText(frame, "smiling", (x, y + h + 40), fontScale=3,
                            fontFace=cv2.FONT_HERSHEY_PLAIN, color=(255, 255, 255))

        # Convert the frame to texture for display in Kivy
        image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        image_texture.blit_buffer(frame.tostring(), colorfmt='bgr', bufferfmt='ubyte')
        self.img.texture = image_texture


if __name__ == '__main__':
    SmileDetectorApp().run()

cap.release()
cv2.destroyAllWindows()
