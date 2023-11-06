import time
import cv2
import numpy as np
from unrealcv import client
import sys

fps = 30
frame_time_ms = int(1000 / fps)


def request_image(image_type):
    res = client.request(f'vget /camera/0/{image_type} png')
    return cv2.imdecode(np.frombuffer(res, np.uint8), cv2.IMREAD_UNCHANGED)


def resize_images(*images):
    # Find the minimum height and width
    min_height = min(image.shape[0] for image in images)
    min_width = min(image.shape[1] for image in images)
    resized_images = [cv2.resize(image, (min_width, min_height)) for image in images]
    return resized_images


if __name__ == '__main__':
    client.connect()

    if not client.isconnected():
        print('UnrealCV server is not running.')
        sys.exit(-1)

    try:
        # Display window setup
        cv2.namedWindow('UE4 Grid Views', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('UE4 Grid Views', 800, 600)
        elapsed_times = []

        while True:
            start_time = time.time()
            # Request different types of images
            lit_image = request_image('lit')
            normal_image = request_image('normal')
            depth_image = request_image('depth')
            segmented_image = request_image('object_mask')

            # Resize images to match the smallest one
            lit_image, normal_image, depth_image, segmented_image = resize_images(
                lit_image, normal_image, depth_image, segmented_image
            )

            # Create two rows of images
            top_row = np.hstack((lit_image, normal_image))
            bottom_row = np.hstack((depth_image, segmented_image))

            # Stack the two rows vertically to make a grid
            images_grid = np.vstack((top_row, bottom_row))

            # Show the grid of images
            cv2.imshow('UE4 Grid Views', images_grid)

            elapsed_time_ms = (time.time() - start_time) * 1000
            elapsed_times.append(elapsed_time_ms)
            if len(elapsed_times) > 100:
                print("Max. FPS: ", int(1000/(sum(elapsed_times)/len(elapsed_times))))
                elapsed_times = []
            delay_time_ms = max(1, frame_time_ms - int(elapsed_time_ms))
            if cv2.waitKey(frame_time_ms) == 27:  # 27 is the ESC key
                break

    except Exception as e:
        print(f'An error occurred: {e}')
    finally:
        cv2.destroyAllWindows()
        client.disconnect()
