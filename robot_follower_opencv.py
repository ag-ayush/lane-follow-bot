from __future__ import division

import cv2
import numpy as np
from matplotlib import pyplot as plt


def color_filter_hsv(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hue = [0, 75]
    saturation = [0, 100]
    value = [175, 255]
    lower_white = np.array([hue[0],saturation[0],value[0]], dtype = "uint8")
    upper_white = np.array([hue[1],saturation[1],value[1]], dtype = "uint8")

    mask = cv2.inRange(hsv, lower_white, upper_white)
    output = cv2.bitwise_and(hsv, hsv, mask=mask)

    # cv2.imshow("images", np.hstack([img, output]))
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return output


def canny_edge_detection(img):
    grayscale = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    thres = 200
    edges = cv2.Canny(grayscale, 0.4*thres, thres)

    # plt.subplot(121), plt.imshow(img, cmap='gray')
    # plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    # plt.subplot(122), plt.imshow(edges, cmap='gray')
    # plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
    # plt.show()
    # px = img[100, 100]

    return edges


def erode_dialte(bin_img):
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
    lines = cv2.HoughLinesP(image=edges, rho=.21, theta=np.pi / 500, threshold=7, lines=np.array([]),
                            minLineLength=20, maxLineGap=10)

    height, width = img.shape[:2]
    L1 = int((1/10)*width)
    L2 = int((3/10)*width)
    M = int((1 / 2) * width)
    R1 = int((7/10)*width)
    R2 = int((9/10)*width)
    cv2.line(img, (M, 0), (M, height), (0, 255, 0), 3, 16)

    cv2.line(img, (L1, 0),(L1, height), (255, 0, 0), 3)
    cv2.line(img, (L2, 0),(L2, height), (255, 0, 0), 3)
    cv2.line(img, (R1, 0),(R1, height), (255, 0, 0), 3)
    cv2.line(img, (R2, 0),(R2, height), (255, 0, 0), 3, 16)

    a, b, c = lines.shape
    for i in range(a):
        width1 = lines[i][0][0]
        width2 = lines[i][0][2]
        avg = (width1+width2)/2

        # TODO: Somehow quantify differences in lines and output a number between -1 and 1.

        if avg < L1 or M<avg<R1:
            print "turn left"
        elif avg > R2 or L2<avg<M:
            print "turn right"

    for i in range(a):
        point1 = (lines[i][0][0], lines[i][0][1])
        point2 = (lines[i][0][2], lines[i][0][3])

        cv2.line(img, point1, point2, (0, 0, 255), 3, cv2.LINE_AA)

    cv2.imwrite('assets/houghlines75.jpg', img)


if __name__ == '__main__':
    # TODO: Figure out how to do this frame by frame for a video
    img = cv2.imread('assets/images/A6821.jpg')
    blur = blur(img)
    res = color_filter_hsv(blur)
    bin_img = erode_dialte(res)
    edges = canny_edge_detection(bin_img)
    hough_line_transform(edges)


