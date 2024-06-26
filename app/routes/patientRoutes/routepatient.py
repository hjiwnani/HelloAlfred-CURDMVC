from fastapi import APIRouter, Request, status, Response
from ...schemas.patientSchemas import CreationUserschema
from ...controller.patientController import Account_Creation, Update_User_Details, Get_User_Details, Delete_User, User_Login, sym_adder, sym_getter
from typing import Optional


router  = APIRouter()


@router.get('/show_accounts',  status_code=status.HTTP_200_OK)
def show_account(req: Optional[dict] = None):
    return Get_User_Details(req)

@router.post('/query_symptoms', status_code=status.HTTP_200_OK)
def query_symptoms(req:dict):
    return sym_getter(req)

@router.post('/login_account')
def login_account(req:dict):
    return User_Login(req)

@router.post('/create_account')
def createaccoutnt(req:dict):
        return Account_Creation(req)

@router.post('/add_symptoms')
def add_symptoms(req:dict):
    return sym_adder(req)

@router.put('/update_details')
def updateAccount(req:dict):
    return Update_User_Details(req)

@router.delete('/delete_account')
def deleteAccount(req:dict):
    return Delete_User(req)

