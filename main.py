from fastapi import FastAPI,Depends
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
# import app.routes.mainRoute as mainRoute
from app.routes import mainRoute

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend's actual origin(s)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# connect()
mainRoute.mainRouter(app)


    

