import cv2 
import depthai as dai

#create a pipeline
pipeline = dai.Pipeline()

#define the source and output
Rgb = pipeline.create(dai.node.ColorCamera)
xoutVideo = pipeline.create(dai.node.XLinkOut)
# set name for output stream
xoutVideo.setStreamName("stream")

#properties of the source
Rgb.setBoardSocket(dai.CameraBoardSocket.RGB)
#setting resolution of RGB camera
Rgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
#resizing frames
Rgb.setVideoSize(1920, 1080)

xoutVideo.input.setBlocking(False)
xoutVideo.input.setQueueSize(1)

# Link input to output
Rgb.video.link(xoutVideo.input)
# start pipeline
with dai.Device(pipeline) as device:
     # output queue will be used to get the rgb frames from the output defined above
    video = device.getOutputQueue(name="stream", maxSize=1, blocking=False)
    # counter for frames
    img_count=0
    frames = []
    while True:
        # get frame
        videoIn = video.get()
        output = videoIn.getCvFrame()
        #Get BGR from NV12 encoded video frame to show with opencv
        cv2.imshow("video", output)

        # when c is pressed, save the frame 
        if cv2.waitKey(1) == ord('c'):
            frames.append(output)
            img_count +=1
            print(len(frames))
        # when p is pressed, create panaroma
        if cv2.waitKey(1) == ord('p'):
            print('Creating Panaroma')
            # check if there are atleast 2 frames
            if img_count < 2:
                print('click more pictures for a panaroma')
            # if there are more than 2 frames, create a panaroma
            else:
                stitcher=cv2.Stitcher.create()
                code,panaroma =stitcher.stitch(frames)
                # if code is not cv2.Stitcher_OK, then there is an error
                if code != cv2.STITCHER_OK:
                    print("stitching not successful")
                # show the panaroma 
                else:
                    print('Your Panorama is ready!!!')
                    cv2.imshow('final result',panaroma)
                    # save the panaroma
                    cv2.imwrite('panaroma.jpg', panaroma)

        
        if cv2.waitKey(1) == ord('q'):
            break