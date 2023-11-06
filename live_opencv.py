from __future__ import division, absolute_import, print_function
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

        while True:
            # Request the next frame
            res = client.request('vget /camera/0/lit png')
            frame = read_png(res)
            cv2.imshow('UE4 Live View', frame)

            # Break the loop if ESC is pressed
            if cv2.waitKey(frame_time_ms) == 27:
                break

        # Close the window after the loop is finished
        cv2.destroyAllWindows()

    except Exception as e:
        print(f'An error occurred: {e}')

    finally:
        client.disconnect()
