from fastapi import APIRouter
from .patientRoutes import routepatient 
from .chatgptRouter import routeChatgpt


def mainRouter(app:APIRouter):
    app.include_router(routepatient.router, prefix='/api', tags=['patients'])
    app.include_router(routeChatgpt.router, prefix='/api', tags=['chatgpt'])
    
    