import sys
sys.path.append('/home/pi/dunker_mail/')
import dunker_mail as orenda_mail
import threading
import time

from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np
import os
from queue import Queue
import select
event = threading.Event()

(reader, writer) = os.pipe()
images_queue=Queue(maxsize=0)

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

def send_mail_with_attachments(server, msg_str, file_attached, file_showed):
    try:
        print("begin to send_mail_with_attachments")
        orenda_mail.send_mail_with_attachments(server, msg_str, file_attached, file_showed)
    except:
        print('error occured')

def select_pipe(reader_file, target_str):
    
    input_list = list()
    input_list.append(reader_file)
    print("begin to select")
    (readyInput,readyOutput,readyException) = select.select(input_list, [], [])
    for indata in readyInput:
        if indata == reader_file:
            # read data
            data = reader_file.read()
            print("read data: ", data)
            if target_str in data:
                return True
        else:
            data = indata.read()
            print("read data: ", data)
    return False

def mail_handler(server, time_interval):
    # open_file = os.fdopen(writer, "w")
    # global server
    
    while True:
        # print(orenda_mail, server)
        (Time, Title, From, To, Id, Msg) = orenda_mail.handle_mail(server)
        # open_file.write("dunker_capture")
        # open_file.write(Msg)
        if Msg is not None and "dunker_capture" in Msg:
            event.set()
        time.sleep(time_interval)
    # open_file.close()
'''
wait for event and capture img.
if capturing success, send to a queue to send as mail attachment.
'''
def camera_operation():
    reader_file = os.fdopen(reader, "r")
    index=0
    while True:
        event.wait()
        event.clear()
        print("    begin to capture")
        with PiCamera() as camera:
            file_name = 'test{}.jpg'.format(index)
            camera.resolution = (320, 240)
            # camera.framerate = 24
            
            image = np.empty((240 * 320 * 3,), dtype=np.uint8)
            camera.capture(image, 'bgr')
            image = image.reshape((240, 320, 3))
            cv2.imwrite(file_name, image)
            
            print('    capture success')
            
            # put img info to queue.
            images_queue.put(file_name)
            
            # wake queue_handler.
                # orenda_mail.send_mail_with_attachments(server, file_name, file_name, file_name)
                # print('image send successfully')
        
        index =index+1
    reader_file.close()

def camera_operation2():
    index=0
    camera = PiCamera()
    while True:
        event.wait()
        event.clear()
        print("    begin to capture")
        file_name = 'test{}.jpg'.format(index)
        
        # camera.resolution = (320, 240)
        camera.capture(file_name, use_video_port = False)
        
        images_queue.put(file_name)
        index =index+1
        


def queue_operation(server, num):
    
    while True:
        time.sleep(5)
        if images_queue.empty():
            continue
        file_name = images_queue.get()
        images_queue.task_done()
        
        orenda_mail.send_mail_with_attachments(server, file_name, file_name, file_name)
        os.remove(file_name)
        

if __name__ == '__main__':
    # event.set()
    server = orenda_mail.load_mail()
    
    t1 = threading.Thread(target=mail_handler, args=(server, 10))
    t1.start()
    
    t2 = threading.Thread(target=camera_operation2)
    t2.start()
    
    t3 = threading.Thread(target=queue_operation, args=(server, 1200))
    t3.start()
    event.clear
