from __future__ import division, absolute_import, print_function
from unrealcv import client
import os, sys, time, re, json
import numpy as np
import matplotlib.pyplot as plt
from io import StringIO, BytesIO
from PIL import Image

imread = plt.imread


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
        print('UnrealCV server is not running. Run the game downloaded from http://unrealcv.github.io first.')
        sys.exit(-1)

    res = client.request('vget /unrealcv/status')
    print(res)

    try:
        # Get image
        img_path = os.path.abspath(os.path.dirname(__file__)) + "/output/"
        if not os.path.exists(img_path):
            os.mkdir(img_path)
        img_filename = img_path + "lit.png"
        res = client.request(f'vget /camera/0/lit {img_filename}')
        print('The image is saved to %s' % img_filename)

        depth_filename = img_path + "depth.png"
        res = client.request(f'vget /camera/0/depth {depth_filename}')
        print('The image is saved to %s' % depth_filename)

        # It is also possible to get the png directly without saving to a file
        res = client.request('vget /camera/0/lit png')
        im = read_png(res)
        print(im.shape)

        # Ground truth acquisition
        objects = client.request('vget /objects')
        print(objects)
        chair = objects.split(" ")[2]
        chair_loc = client.request(f'vget /object/{chair}/location')
        print("Chair location: ", chair_loc)

        plt.imshow(im)
        plt.show()

    except Exception as e:
        print(f'An error occurred: {e}')

client.disconnect()
