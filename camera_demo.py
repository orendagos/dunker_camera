from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import os
import datetime

# initialize the camera and grab a reference to the raw camera capture
def test0():
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

def test0_0():
    imgPath = "images"  # 读取图片路径
    videoPath = "."  # 保存视频路径
 
    images = os.listdir(imgPath)
    fps = 25  # 每秒25帧数
 
    # VideoWriter_fourcc为视频编解码器 ('I', '4', '2', '0') —>(.avi) 、('P', 'I', 'M', 'I')—>(.avi)、('X', 'V', 'I', 'D')—>(.avi)、('T', 'H', 'E', 'O')—>.ogv、('F', 'L', 'V', '1')—>.flv、('m', 'p', '4', 'v')—>.mp4
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
 
    # image = Image.open(imgPath + images[0])
    videoWriter = cv2.VideoWriter("00.mp4", fourcc, fps, (640, 480))
    
    for im_name in range(len(images)):
        print('handle: ', imgPath + '/' +images[im_name])
        frame = cv2.imread(imgPath + '/' +images[im_name])  # 这里的路径只能是英文路径
        print(frame.shape)
        # frame = cv2.imdecode(np.fromfile((imgPath + images[im_name]), dtype=np.uint8), 1)  # 此句话的路径可以为中文路径
        print(im_name)
        videoWriter.write(frame)
        
    print("图片转视频结束！")
    videoWriter.release()
    cv2.destroyAllWindows()



def get_video(time_interval):
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera)
    # allow the camera to warmup
    time.sleep(0.1)
    t0 = datetime.datetime.now()
 
    # VideoWriter_fourcc为视频编解码器 ('I', '4', '2', '0') —>(.avi) 、('P', 'I', 'M', 'I')—>(.avi)、('X', 'V', 'I', 'D')—>(.avi)、('T', 'H', 'E', 'O')—>.ogv、('F', 'L', 'V', '1')—>.flv、('m', 'p', '4', 'v')—>.mp4
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
 
    # image = Image.open(imgPath + images[0])
    videoWriter = cv2.VideoWriter("01.mp4", fourcc, 25, (640, 480))
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        if (datetime.datetime.now() - t0).total_seconds() > time_interval:
            break
        image = frame.array
        print(image.shape)
        videoWriter.write(image)
        rawCapture.truncate(0)
    videoWriter.release()
    cv2.destroyAllWindows()

if __name__=="__main__":
    # test0()
    test0_0()
    get_video(2)
    