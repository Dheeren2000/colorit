import numpy as np
import tensorflow as tf
from skimage.io import imread
from skimage.transform import resize
from skimage.color import rgb2lab, lab2rgb
from utils.ImageUtils import ImageUtils


class Colorizer:
    '''Description : Class to Colorize the images'''

    # To predict the lab channels of given image
    def __predictLAB(self, model, imgPath, img_w, img_h):

        '''
        Description :
                Method to takes RGB Image filepath, then convert it to LAB to extract the L channel and 
                predict the remaining two channels (A` & B`)
        Input : 
                model => Pretrained NN model to predict the A` and B` channels
                imgPath => RGB image file path
        Returns : 
                Tuple (L channel and Predicted AB channels)

        '''

        image = ImageUtils.getRGBData(imgPath, img_w, img_h)

        labImage = ImageUtils.getLABData(image)

        _l, _ab = ImageUtils.getXYData(labImage, img_w, img_h)
        # print(f'_fn_predLAB _l Shape : {_l.numpy().shape}')
        _l = _l.numpy()
        _l = _l.reshape((1,) + _l.shape)
        # print(f'_fn_predLAB _l re-Shape : {_l.shape}')
        _abPred = model.predict(_l)
        return _l, _abPred


    # To Postprocess the L and AB channel
    # i.e. merge the L and AB channel and convert them into RGB image
    def __imgPostProcess(self, _l, _ab):

        '''
        Description : 
                Method to perform the processing on the predicted images
        Input : 
                _l => L channel of the Image
                _ab => Predicted AB channel of Image
        Returns : 
                np.array (RGB Image - w * h* 3)
        '''
        w = _ab.shape[1]
        h = _ab.shape[2]
        result = np.zeros((w, h, 3))

        # de normalizing the values
        # _l *= 100
        _ab *= 128
        # merging all the channels
        result[:,:,0] = _l[0,:,:,0] 
        result[:,:,1:] = _ab[0,:,:,:]


        result = result.astype('float32')

        rgb = lab2rgb(result)
        # ########
        
        # print(rgb.shape)
        return np.array(rgb)

    # To predict the RGB Images from given images
    def predictRGB(self, model, imgPath):
        
        '''
        Description : 
                Method to predict the RGB Image 
        Input : 
                model => Pretrained NN model to predict the A` and B` channels
		imgPath => path to image
        Returns : 
                np.array (RGB Image - w * h* 3)
        '''
        # getting the image original height and width

        image = imread(imgPath)
        ori_h, ori_w = image.shape[0], image.shape[1]

        img_w, img_h = 256, 256
        _l, predAB = self.__predictLAB(model, imgPath, img_w, img_h) 
        rgbImage = self.__imgPostProcess(_l, predAB)

        # resizing the regbImage result to original shape
        rgbImage = resize(rgbImage, (ori_h, ori_w))

        return np.array(rgbImage)