import cv2
from PIL import Image
import numpy as np
import tensorflow as tf
from skimage.io import imread
from skimage.transform import resize
from skimage.color import rgb2lab, lab2rgb

class ImageUtils:

    '''
    Description : ImageUtils class to get the RGB, LAB and to split the LAB channel into L and AB
    '''

    # Method to get the RGB images
    @staticmethod
    def getRGBData(filePath, img_width, img_height):
        '''
        Description : 
                Method to get the RGB image from the given path
        Input :
                filePath => File path to the image (dType - String)
                img_width => Width of the Image 
                img_height => Height of the Image
        Returns :
                tf.Tensor 
        '''
        image = imread(filePath)
        image = resize(image, output_shape=[img_width, img_height])         
        # resize method gives resized image along with normalization
        return image

    # Method to get the LAB images
    @staticmethod
    def getLABData(image):
        '''
        Description : 
                Method to get the LAB image from the given image
        Input :
                image => RGB Image 
        Returns :
                tf.Tensor 
        '''
        labImage = rgb2lab(image)
        return labImage


    # Method to get the X(L) and Y(AB) data
    @staticmethod
    def getXYData(labImage, img_width, img_height):
        '''
        Description : 
                Method to split LAB image into L and AB channels as X and Y
        Input :
                labImage => LAB Image
                img_width => Width of the Image 
                img_height => Height of the Image
        Returns :
                tf.Tensor, tf.Tensor 
        '''
        _l = tf.reshape(labImage[:,:,0], shape=[img_width,img_height,1])
        _ab = tf.reshape(labImage[:,:,1:] / 128, shape=[img_width,img_height,2])
        return _l, _ab

    # to fix the shape
    def fixup_shape(_l, _ab, w, h):
        _l.set_shape([w, h, 1])
        _ab.set_shape([w, h, 2])
        return _l, _ab


    # Method to check whether given image is grayscale or not
    @staticmethod
    def isGrayImage(imgPath):

        """
        Description : 
                Method to check whether given image is grayscale or not
        Parameters : 
                imgPath => Image File Path
        Retruns : 
                True (if grayscale) | False (if not grayscale)
        """

        # using tensorflow to check if the image is grayscale or not
        image = tf.io.read_file(imgPath)
        image = tf.image.decode_jpeg(image)
        print(image.numpy().shape)

        isGrayScale = True

        if len(image.shape) == 3 and image.shape[2] == 3:
            isGrayScale = False

        print(f'is gray : {isGrayScale}')

        # if tensorflow give result as false then checking with cv2
        if not isGrayScale:
            # reading the image
            img = cv2.imread(imgPath)

            # if the image shape length is less than 3
            if len(img.shape) < 3: 
                return True

            # if the image has only one channel
            if img.shape[2] == 1: 
                return True

            # checking the all pixel are equal or not
            b,g,r = img[:,:,0], img[:,:,1], img[:,:,2]
            if (b==g).all() and (b==r).all(): 
                return True

        return False

