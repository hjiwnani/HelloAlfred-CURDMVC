from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# import azure.functions as func
import pandas as pd
import ast
import urllib
import uuid
import datetime
import jwt
import json

def createconnection():
    # TODO : Convert this to use Azure sql
    params = urllib.parse.quote_plus(r'Driver={ODBC Driver 17 for SQL Server};Server=tcp:helloalfredpudb.database.windows.net,1433;Database=HelloAlfredUser;Uid=adminalfred;Pwd={Admin@hello};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    conn_str = 'mssql+pyodbc:///?odbc_connect={}'.format(params)
    engine = create_engine(conn_str,echo=True, pool_size=10, max_overflow=20)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
    # conn_string = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:sqldemotrial.database.windows.net,1433;Database=hemang_trial;Uid=admin1hemang;Pwd=admin@3210;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

def parse_header(req):
    req_body_bytes = req
    req_body = req_body_bytes.decode("utf-8")
    req_body = ast.literal_eval(req_body)
    return req_body

def patient_id_generator(req_body):  
    return str(uuid.uuid4())[:18]   


def jsonCommonStatus(message, data, code, status):
    if data :
        return {
            "statuscode":code,
            "status":status,
            "message":message,
            "data":data
            }
        
    return {
            "statuscode":code,
            "status":status,
            "message":message
            }
    

SECRET_KEY = "helloAlfredo"
ALGORITHM = "HS256"


def create_jwt_token(data: dict):
    expire = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=5)
    data["exp"] = expire
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def verify_jwt_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return "Token expired. Please log in again."
    except jwt.InvalidTokenError:
        return "Invalid token. Please log in again."
