import stat
import psycopg2
import psycopg2.extras


class ConnectionManager:
    def __init__(self):
        self.conn = None
        self.DB_HOST = "localhost"
        self.DB_PORT = "5432"
        self.DB_NAME = "db_colorization"
        self.DB_USER = "postgres"
        self.DB_PASS = "djmn@1234"
    
    def getConnection(self):
        
        # creating the connection object
        self.conn =  psycopg2.connect(host=self.DB_HOST,
                                    port=self.DB_PORT, 
                                    dbname=self.DB_NAME, 
                                    user=self.DB_USER, 
                                    password=self.DB_PASS)
        return self.conn

# con = ConnectionManager()
# con.getConnection()
# print('connection successfull')        