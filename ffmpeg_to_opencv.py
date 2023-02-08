import cv2
import numpy as np
import subprocess
import time
import datetime

# Use public RTSP Stream for testing
in_stream = 'rtsp://admin:abcd1234@10.61.212.41:554/Streaming/Channels/1/'

start = datetime.datetime.now()
width = 1920
height = 1080

# Define the codec and create a VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output_cam41_ffmpeg.avi', fourcc, 20.0, (1920, 1080))
end = datetime.datetime.now()
print(f"estimate2: {(end-start)}")

command = ['ffmpeg', # Using absolute path for example (in Linux replacing 'C:/ffmpeg/bin/ffmpeg.exe' with 'ffmpeg' supposes to work).
           #'-rtsp_flags', 'listen',   # The "listening" feature is not working (probably because the stream is from the web)
           '-rtsp_transport', 'tcp',   # Force TCP (for testing)
           '-max_delay', '3000000',   # 3 seconds (sometimes needed because the stream is from the web).
           '-i', in_stream,
           '-f', 'rawvideo',           # Video format is raw video
           '-pix_fmt', 'bgr24',        # bgr24 pixel format matches OpenCV default pixels format.
           '-an', 'pipe:']

# Open sub-process that gets in_stream as input and uses stdout as an output PIPE.
ffmpeg_process = subprocess.Popen(command, stdout=subprocess.PIPE)

while True:
    # Read width*height*3 bytes from stdout (1 frame)
    raw_frame = ffmpeg_process.stdout.read(width*height*3)

    if len(raw_frame) != (width*height*3):
        print('Error reading frame!!!')  # Break the loop in case of an error (too few bytes were read).
        break

    # Convert the bytes read into a NumPy array, and reshape it to video frame dimensions
    frame = np.frombuffer(raw_frame, np.uint8).reshape((height, width, 3))
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cv2.putText(frame, timestamp, (10, 470), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    out.write(frame)


ffmpeg_process.stdout.close()  # Closing stdout terminates FFmpeg sub-process.
ffmpeg_process.wait()  # Wait for FFmpeg sub-process to finish

