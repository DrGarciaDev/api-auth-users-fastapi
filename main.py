# Python 

# FastAPI
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

# modulos locales
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.auth_router import auth_router
from routers.user_router import user_router
from routers.role_router import role_router
from routers.user_roles_router import user_roles_router
from routers.permission_router import permission_router
from routers.role_permissions_router import role_permissions_router

app = FastAPI()
app.title = 'Mi app con FastAPI'
app.version = '0.0.1'

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
    "http://localhost:4200",
    "http://localhost:3000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(ErrorHandler)

# Base.metadata.create_all(bind=engine)

@app.get(path='/', tags=['Home'])
def home():
    return RedirectResponse(url='/docs/')

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(user_roles_router)
app.include_router(role_router)
app.include_router(role_permissions_router)
app.include_router(permission_router)