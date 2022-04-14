import psycopg2
import psycopg2.extras


class ConnectionManager:
    conn=''
    def __init__(self):
        
        self.DB_HOST = "localhost"
        self.DB_PORT = "5432"
        self.DB_NAME = "test_color"
        self.DB_USER = "postgres"
        self.DB_PASS = "Dheeren123$"
    
    def getConnection(self):
        
        ConnectionManager.conn =  psycopg2.connect(host=self.DB_HOST, port=self.DB_PORT, dbname=self.DB_NAME, user=self.DB_USER, password=self.DB_PASS)
        return ConnectionManager.conn
# con = ConnectionManager()
# con.getConnection()
# print('connection successfull')        