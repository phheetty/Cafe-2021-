from config import *

def connectToDB():
    dbname = os.getenv("dbname")
    user = os.getenv("user")
    password = os.getenv("password")
    host = os.getenv("host")
    port = os.getenv("port")
    connectionDB = 'dbname=%s user=%s password=%s host=%s port=%s' % (dbname,user,password,host,port)
    try:
        return psycopg2.connect(connectionDB)
    except:
        return jsonify({'status':'fail','message':'Something went wrong'})
