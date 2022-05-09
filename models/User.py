# 
# Creating the model to represent the user

class User:
    
    # constructor 
    def __init__(self, firstName, lastName, email, password='NA', id=-1):
        """
        Constructor:
        Param: id, firstName, lastName, email, password
        """
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password


    # method to get the user details 
    def getUserDetails(self):
        """
        Method to get the User details
        returns: dict()
        """
        # creating the dict to store the details of user
        details = dict()

        details['id'] = self.id
        details['firstName'] = self.firstName
        details['lastName'] = self.lastName
        details['email'] = self.email
        details['password'] = self.password

        return details


    # method to set the user details
    def setUserDetails(self, details):
        """
        Method to set the details of User
        dict() {id, firstName, lastName, email, password}
        """
        self.id = details['id']
        self.firstName = details['firstName']
        self.lastName = details['lastName']
        self.email = details['email']
        self.password = details['password']




    