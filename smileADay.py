import cv2
from kivy.app import App
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.relativelayout import RelativeLayout
from kivymd.app import MDApp
from kivy.uix.video import Video
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

cap = cv2.VideoCapture(0)
trainedFaceData = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
trainedSmileData = cv2.CascadeClassifier("haarcascade_smile.xml")


class MainApp(MDApp):
    title = "DOG"
    def build(self):
        # Create a vertical box layout to hold the buttons
        layout = BoxLayout(orientation='horizontal', spacing=700)
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"

        layout = RelativeLayout()

        # Create an image widget for displaying camera feed
        self.img = Image()
        layout.add_widget(self.img)

        video = Video(source='funny_dog.mp4')
        video.state='play'
        video.options = {'eos': 'loop'}
        video.allow_stretch=True
        video.width = self.img.width
        layout.add_widget(video)

        # Set the position of the camera feed image using pos_hint
        self.img.pos_hint = {'y': 0, 'center_x': 0.5,'height': 0.5}
        self.img.size_hint = (1, 0.5)

        # Set the position and size of the video player using pos_hint and size_hint
        video.pos_hint = {'top': 1, 'center_x': 0.5, 'height': 0.5}
        video.size_hint = (0.5, 0.5)  # Set video player size to match camera feed size
    

        Clock.schedule_interval(self.update, 1.0 / 60.0) # Update at 60 FPS

        return layout

    def update(self, dt):
        # Read a frame from the camera
        ret, frame = cap.read()

        if not ret:
            return

        # Flip the frame vertically
        frame = cv2.flip(frame, 0)

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

                flipped_image = cv2.flip(frame, 0)

                # Save the original unflipped frame as an image
                cv2.imwrite("smile_detected.jpg", flipped_image)

        # Convert the frame to texture for display in Kivy
        image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        image_texture.blit_buffer(frame.tostring(), colorfmt='bgr', bufferfmt='ubyte')
        self.img.texture = image_texture

if __name__ == '__main__':
    MainApp().run()

cap.release()
cv2.destroyAllWindows()
