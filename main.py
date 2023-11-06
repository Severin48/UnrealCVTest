from __future__ import division, absolute_import, print_function
from unrealcv import client
import os, sys, time, re, json
import numpy as np
import matplotlib.pyplot as plt
from io import StringIO, BytesIO
from PIL import Image

imread = plt.imread
n_frames = 60


def imread8(im_file):
    ''' Read image as a 8-bit numpy array '''
    im = np.asarray(Image.open(im_file))
    return im


def read_png(res):
    img = Image.open(BytesIO(res))
    return np.asarray(img)


def read_npy(res):
    return np.load(StringIO(res))


if __name__ == '__main__':
    client.connect()

    if not client.isconnected():
        print('UnrealCV server is not running.')
        sys.exit(-1)

    try:
        res = client.request('vget /camera/0/lit png')
        im = read_png(res)
        window = plt.imshow(im)
        for _ in range(n_frames):
            res = client.request('vget /camera/0/lit png')
            im = read_png(res)
            window.set_data(im)

        # Ground truth acquisition
        objects = client.request('vget /objects')
        print("Objects:\t\t", objects)
        chair = objects.split(" ")[2]
        chair_loc = client.request(f'vget /object/{chair}/location')
        print("Chair location:\t", chair_loc)

        plt.show()

    except Exception as e:
        print(f'An error occurred: {e}')

client.disconnect()
