from fastapi import APIRouter
from .patientRoutes import routepatient 


def mainRouter(app:APIRouter):
    app.include_router(routepatient.router, prefix='/api', tags=['patients'])
    