import time
from unrealcv import client
import sys
import numpy as np
import cv2
from io import BytesIO
from PIL import Image

frame_time_ms = 1


# Function to read image from a PNG byte stream
def read_png(res):
    img = Image.open(BytesIO(res))
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)


if __name__ == '__main__':
    client.connect()

    if not client.isconnected():
        print('UnrealCV server is not running.')
        sys.exit(-1)

    try:
        # Initial request to get the first frame
        res = client.request('vget /camera/0/lit png')
        frame = read_png(res)

        # Display the window
        cv2.imshow('UE4 Live View', frame)
        elapsed_times = []

        while True:
            start_time = time.time()
            # Request the next frame
            res = client.request('vget /camera/0/lit png')
            frame = read_png(res)
            cv2.imshow('UE4 Live View', frame)

            elapsed_time_ms = (time.time() - start_time) * 1000
            elapsed_times.append(elapsed_time_ms)
            if len(elapsed_times) > 100:
                print("Max. FPS: ", int(1000 / (sum(elapsed_times) / len(elapsed_times))))
                elapsed_times = []
            delay_time_ms = max(1, frame_time_ms - int(elapsed_time_ms))
            if cv2.waitKey(delay_time_ms) == 27:  # 27 is the ESC key
                break

    except Exception as e:
        print(f'An error occurred: {e}')

    finally:
        cv2.destroyAllWindows()
        client.disconnect()
