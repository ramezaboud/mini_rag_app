from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
import os
load_dotenv("assets/.env")

base_router = APIRouter(
    prefix="/api/v1",
    tags=["v1"])

@base_router.get("/welcome")

async def welcome():
        app_name = os.getenv("APP_NAME")
        app_version = os.getenv("APP_VERSION")

        return {
            'App name' : app_name,
            'App version' : app_version
        }