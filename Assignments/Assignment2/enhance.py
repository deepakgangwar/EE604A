import cv2
import numpy as np
from scipy import signal, misc
from PIL import Image
# import skimage

def enhance(path):
    print "executing image Enhancement"
    input = cv2.imread(path,0)
    # input = cv2.cvtColor(input, cv2.COLOR_BGR2GRAY)

    img = input.copy()
    # img = cv2.bilateralFilter(img,9,75,75)
    # img = cv2.fastNlMeansDenoising(img,None,3,7,21)


    # img = cv2.GaussianBlur( img,(3,3),0 )
    # laplacian = cv2.Laplacian(img, cv2.CV_8U)#, 3, 1, cv2.BORDER_DEFAULT)
    # img = cv2.add(img ,laplacian)

    # img = cv2.equalizeHist(img)

    # img = cv2.bilateralFilter(img,9,75,75)
    img = cv2.fastNlMeansDenoising(img,None,3,7,21)

    # img = cv2.GaussianBlur( img,(3,3),0 )
    # laplacian = cv2.Laplacian(img, cv2.CV_8U)#, 3, 1, cv2.BORDER_DEFAULT)
    # img = cv2.add(img ,laplacian)

    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(10,10))
    img = cl1 = clahe.apply(img)
    #
    img = cv2.fastNlMeansDenoising(img,None,3,7,21)
    return input, img
