from __future__ import division, absolute_import, print_function
from unrealcv import client
import os, sys, time, re, json
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image

frame_time = 0.01


# Function to read image from a PNG byte stream
def read_png(res):
    img = Image.open(BytesIO(res))
    return np.asarray(img)


if __name__ == '__main__':
    client.connect()

    if not client.isconnected():
        print('UnrealCV server is not running.')
        sys.exit(-1)

    # Set up the plot
    plt.ion()  # Turn on interactive mode
    fig, ax = plt.subplots()  # Create a figure and a set of subplots

    try:
        # Initial request to get the first frame
        res = client.request('vget /camera/0/lit png')
        im = read_png(res)
        implot = ax.imshow(im)

        while True:
            # Request the next frame
            res = client.request('vget /camera/0/normal png')
            im = read_png(res)
            implot.set_data(im)

            # Update the plot
            plt.draw()
            plt.pause(frame_time)

    except Exception as e:
        print(f'An error occurred: {e}')

    finally:
        client.disconnect()
