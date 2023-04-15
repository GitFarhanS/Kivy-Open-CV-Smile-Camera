from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.uix.button import Button
import cv2


class CameraApp(App):
    def build(self):
        # Create a vertical box layout for the app
        layout = BoxLayout(orientation='vertical')

        # Create a camera widget and add it to the layout
        self.camera = Camera(resolution=(640, 480), play=True)
        layout.add_widget(self.camera)

        # Create a button widget for capturing and saving the image
        capture_button = Button(text='Capture', size_hint=(1, 0.1))
        capture_button.bind(on_press=self.capture_image)
        layout.add_widget(capture_button)

        return layout

    def capture_image(self, instance):
        # Capture the current camera frame as an image
        filename = 'captured_image.png'
        self.camera.export_to_png(filename)
        print(f'Image captured and saved as {filename}')


if __name__ == '__main__':
    CameraApp().run()
