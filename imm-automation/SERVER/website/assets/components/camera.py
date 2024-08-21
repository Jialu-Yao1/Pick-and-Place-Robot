import cv2 as cv
import time


class USBCamera:
    def __init__(self, cam_port):
        self.cam_port = cam_port
        self.cam = None
        self.connect()

    def __del__(self):
        self.disconnect()

    def connect(self):
        """
        Connects to the camera at a given port.
        """
        self.cam = cv.VideoCapture(self.cam_port)

    def disconnect(self):
        """
        Disconnects the camera.
        """
        self.cam.release()

    def image(self, filename):
        """
        Takes an image using the camera.

        :param filename: File name to store the image under.
        """
        result, image = self.cam.read()
        if result:
            cv.imwrite(f"{filename}.png", image)
        else:
            print("No image detected.")


if __name__ == "__main__":
    # 0 for built in laptop camera 1+ for external webcams
    camera = USBCamera(0)
    camera.image(r"C:\Users\tanya\Documents\MANU 430\Camera Module\test1")
    time.sleep(5)
    camera.image(r"C:\Users\tanya\Documents\MANU 430\Camera Module\test2")
    camera.disconnect()
