import sys
sys.path.append('/home/pi/0630/mail/')
import dunker_mail as orenda_mail
import threading
import time

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

def camera_test():
    # initialize the camera and grab a reference to the raw camera capture
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera)
    # allow the camera to warmup
    time.sleep(0.1)
    # capture frames from the camera
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array
        # show the frame
        cv2.imshow("Frame", image)
        # prepare for net stream
        rawCapture.truncate(0)

        if(cv2.waitKey(1) == ord('q')):
            cv2.destroyAllWindows()
            break;

def hello(msg, server):
    print("msg:", msg, "server:", type(server))
    while True:
        orenda_mail.handle_mail(server);
        time.sleep(10)

def send_mail_with_attachments(server, msg_str, file_attached, file_showed):
    try:
        print("begin to send_mail_with_attachments")
        server = orenda_mail.load_mail()
        orenda_mail.send_mail_with_attachments(server, msg_str, file_attached, file_showed)
    except:
        print('error occured')

def camera_operation(server, interval):
    index=0
    while True:
        server = orenda_mail.load_mail()
        with PiCamera() as camera:
            # file_name = str(index)+'test.jpg'
            file_name = 'test.jpg'
            camera.resolution = (320, 240)
            camera.framerate = 24
            print("    begin to capture")
            
            time.sleep(2)
            image = np.empty((240 * 320 * 3,), dtype=np.uint8)
            camera.capture(image, 'bgr')
            image = image.reshape((240, 320, 3))
            cv2.imwrite(file_name, image)
            
            print('    capture success')
            send_mail_with_attachments(server, file_name, file_name, file_name)
            # orenda_mail.send_mail_with_attachments(server, file_name, file_name, file_name)
            print('image send successfully')
        time.sleep(interval)
        index =index+1
        
        

if __name__ == '__main__':
    server = orenda_mail.load_mail()
    # orenda_mail.send_mail_with_attachments(server, "123456", 'img.jpg', 'img.jpg')
    
    t1 = threading.Thread(target=hello, args=("hawk", server))
    # t1.start()
    
    t2 = threading.Thread(target=camera_operation, args=(server, 1200))# interval is 2min
    t2.start()
