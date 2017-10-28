from __future__ import division
from arduino_bridge import *

import cv2
import numpy as np
from matplotlib import pyplot as plt


def color_filter_hsv(img):
    """ HSV Color Filter"""
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hue = [0, 75]
    saturation = [0, 100]
    value = [150, 255]
    lower_white = np.array([hue[0],saturation[0],value[0]], dtype = "uint8")
    upper_white = np.array([hue[1],saturation[1],value[1]], dtype = "uint8")

    mask = cv2.inRange(hsv, lower_white, upper_white)
    output = cv2.bitwise_and(hsv, hsv, mask=mask)

    # OUTPUT:
    # cv2.imshow("images", np.hstack([img, output]))
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return output


def canny_edge_detection(img):
    """
    Canny Edge Detection
    First argument is our input image.
    Second and third arguments are our minVal and maxVal respectively.
    Third argument is aperture_size, the size of Sobel kernel used for find image gradients.
    """
    grayscale = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    thres = 200
    edges = cv2.Canny(grayscale, 0.4*thres, thres)

    # OUTPUT:
    # plt.subplot(121), plt.imshow(img, cmap='gray')
    # plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    # plt.subplot(122), plt.imshow(edges, cmap='gray')
    # plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
    # plt.show()
    # px = img[100, 100]

    return edges


def erode_dilate(bin_img):
    """ Erodes some noise away,
        then dilates to make lines more visible
        lastly erodes again to make it work able.

        Net is a dilation of 1."""
    kernel = np.ones((3, 3),np.uint8)
    erosion = cv2.erode(bin_img, kernel, iterations=1)
    dilation = cv2.dilate(erosion, kernel, iterations=5)
    erosion = cv2.erode(dilation, kernel, iterations=3)

    # cv2.imshow('image', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return erosion


def blur(img):
    """keep this kernel above a pixel,
    add all the 25 pixels below this kernel,
    take its average and replace the central pixel with the new average value.
    It continues this operation for all the pixels in the image. """

    blur = cv2.blur(img, (10, 10))

    # plt.subplot(121), plt.imshow(img), plt.title('Original')
    # plt.xticks([]), plt.yticks([])
    # plt.subplot(122), plt.imshow(blur), plt.title('Blurred')
    # plt.xticks([]), plt.yticks([])
    # plt.show()

    return blur


def hough_line_transform(edges):
    # The line detector
    lines = cv2.HoughLinesP(image=edges, rho=.21, theta=np.pi / 500, threshold=7, lines=np.array([]),
                            minLineLength=20, maxLineGap=10)

    """
    Find the ideal areas for lines to be. 
    The image is split into 10ths where the ideal locations are 
        3/10 to 5/10 [Left Lane]
        7/10 to 9/10 [Right Lane]
    """
    height, width = img.shape[:2]
    L1 = int((1/10)*width)
    L2 = int((3/10)*width)
    M = int((1 / 2) * width)
    R1 = int((7/10)*width)
    R2 = int((9/10)*width)
    cv2.line(img, (M, 0), (M, height), (0, 255, 0), 3, 16)

    cv2.line(img, (L1, 0),(L1, height), (255, 0, 0), 3, 16)
    cv2.line(img, (L2, 0),(L2, height), (255, 0, 0), 3, 16)
    cv2.line(img, (R1, 0),(R1, height), (255, 0, 0), 3, 16)
    cv2.line(img, (R2, 0),(R2, height), (255, 0, 0), 3, 16)

    # Find the distance a line is away if detected from its should be position and
    # draw that distance.
    a, b, c = lines.shape
    for i in range(a):
        width1 = lines[i][0][0]
        width2 = lines[i][0][2]
        height1 = lines[i][0][1]
        height2 = lines[i][0][3]
        avg_width = int((width1+width2)/2)
        avg_height = int((height1 + height2)/2)

        total_distance = 0

        if avg_width < L1:
            cv2.line(img, (avg_width, avg_height), (L1, avg_height), (0, 0, 0), 3)
            total_distance = total_distance - (L1 - avg_width)
        elif L2<avg_width<M:
            cv2.line(img, (avg_width, avg_height), (L2, avg_height), (0, 0, 0), 3)
            total_distance = total_distance - (avg_width - L2)
        elif M<avg_width<R1:
            cv2.line(img, (avg_width, avg_height), (R1, avg_height), (0, 0, 0), 3)
            total_distance = total_distance + (R1 - avg_width)
        elif avg_width > R2:
            cv2.line(img, (avg_width, avg_height), (R2, avg_height), (0, 0, 0), 3)
            total_distance = total_distance + (avg_width - R2)

    # Draw the lines themselves.
    for i in range(a):
        point1 = (lines[i][0][0], lines[i][0][1])
        point2 = (lines[i][0][2], lines[i][0][3])

        cv2.line(img, point1, point2, (0, 0, 255), 3, cv2.LINE_AA)

    # 1/5 the width because that is worst case scenario
    text = "Travel: " + str(total_distance/((1/5)*width))

    # Print out movement on the image.
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, text, (10, height - 10), font, 1, (0, 0, 0), 2, cv2.LINE_AA)

    cv2.imwrite('assets/houghlines75.jpg', img)

    return total_distance/((1/5)*width)

if __name__ == '__main__':
    # TODO: Figure out how to do this frame by frame for a video
    img = cv2.imread('assets/images/t6.png')

    cap = cv2.VideoCapture("assets/videos/Video_1.mp4")
    blur = blur(img)
    res = color_filter_hsv(blur)
    bin_img = erode_dilate(res)
    edges = canny_edge_detection(bin_img)
    floater = hough_line_transform(edges)

    send_data(floater)

