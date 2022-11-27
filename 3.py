import cv2
import depthai as dai
import numpy as np
# Start defining a pipeline
pipeline = dai.Pipeline()
# Define a source - color camera
rgb = pipeline.create(dai.node.ColorCamera)
# creatiing a board socket for RGB camera
rgb.setBoardSocket(dai.CameraBoardSocket.RGB)
# setting resolution of RGB camera
rgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
# resizing frames 
rgb.setVideoSize(720, 640)
#creating a output stream for RGB camera
output_rgb = pipeline.create(dai.node.XLinkOut)
# setting name for output stream
output_rgb.setStreamName('colorcam')
# connecting RGB camera to output stream
rgb.video.link(output_rgb.input)

# start pipeline
with dai.Device(pipeline) as device:
    # output queue will be used to get the rgb frames from the output defined above
    rgb_stream = device.getOutputQueue(name='colorcam', maxSize=1)
    while True:
        # get frame
        color_frame = rgb_stream.get().getCvFrame()
        # convert frame to float
        color_frame = np.array(color_frame, dtype=np.float32)
        # take sum along columns then take sum along rows
        output_manual = np.cumsum(color_frame, axis=1).cumsum(axis=0)
        # scale integral image between 0 and 255 range
        output_manual = cv2.normalize(output_manual, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC1)
        # convert frames back to uint8
        color_frame = np.uint8(color_frame)
        output_manual = np.uint8(output_manual)
        # show frames
        cv2.imshow("Original Frame", color_frame)
        cv2.imshow("Integral Image", output_manual)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
    cv2.destroyAllWindows()
