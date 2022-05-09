# 
# Creating the model to represent the ImageData

class ImageData:
    
    # constructor 
    def __init__(self, fileName, grayImage, rgbImage,  uniqueId, datetime='NA', id=-1):
        """
        Constructor:
        Param: id, firstName, lastName, email, password
        """
        self.id = id
        self.fileName = fileName
        self.grayImage = grayImage
        self.rgbImage = rgbImage
        self.datetime = datetime
        self.uniqueId = uniqueId
        
    # method to get the image data 
    def getImageData(self):
        """
        Method to get the image data
        returns: dict()
        """
        # creating the dict to store the data of image
        data = dict()

        data['id'] = self.id
        data['fileName'] = self.fileName
        data['grayImage'] = self.grayImage
        data['rgbImage'] = self.rgbImage
        data['datetime'] = self.datetime
        data['uniqueId'] = self.uniqueId

        return data

    # method to set the image data
    def setImageData(self, data):
        """
        Method to set the data of image
        param: dict() {id, fileName, grayImage, rgbImage, datetime}
        """
        self.id = data['id']        
        self.fileName = data['fileName'] 
        self.grayImage = data['grayImage']
        self.rgbImage = data['rgbImage'] 
        self.datetime = data['datetime'] 
        self.uniqueId = data['uniqueId']