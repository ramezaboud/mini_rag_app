from fastapi import FastAPI, APIRouter, Depends
from helpers.config import get_settings, settings
import os

base_router = APIRouter(
    prefix="/api/v1",
    tags=["v1"],
    )

@base_router.get("/welcome")

async def welcome(app_settings: settings= Depends(get_settings)):
        
        app_name = app_settings.APP_NAME
        app_version = app_settings.APP_VERSION

        return {
            'App name' : app_name,
            'App version' : app_version
        }