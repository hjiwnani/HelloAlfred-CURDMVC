from fastapi import APIRouter, Request, status, Response
from ...schemas.patientSchemas import CreationUserschema
from ...controller.patientController import Account_Creation, Update_User_Details, Get_User_Details, Delete_User, User_Login, sym_adder, sym_getter
from typing import Optional


router  = APIRouter()


@router.get('/show_accounts',  status_code=status.HTTP_200_OK)
def show_account(response : Response,req: Optional[dict] = None):
    return Get_User_Details(req,response)

@router.post('/query_symptoms', status_code=status.HTTP_200_OK)
def query_symptoms(response : Response,req:dict):
    return sym_getter(req,response)

@router.post('/login_account', status_code=status.HTTP_200_OK)
def login_account(response : Response,req:dict):
    return User_Login(req,response)

@router.post('/create_account',status_code=status.HTTP_201_CREATED)
def createaccoutnt( response : Response ,req:dict):
        return Account_Creation(req, response)

@router.post('/add_symptoms', status_code=status.HTTP_200_OK)
def add_symptoms(response : Response,req:dict):
    return sym_adder(req,response)

@router.put('/update_details', status_code=status.HTTP_200_OK)
def updateAccount(response : Response,req:dict):
    return Update_User_Details(req,response)

@router.delete('/delete_account', status_code=status.HTTP_202_ACCEPTED)
def deleteAccount(response : Response,req:dict):
    return Delete_User(req,response)

