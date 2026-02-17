from fastapi import FastAPI, APIRouter, Depends, UploadFile, status
from helpers.config import get_settings, settings
from controllers import DataController , ProjectController, ProcessController
from models import ResponseEnums
from fastapi.responses import JSONResponse
from .schema.data import ProcessRequest
import os
import aiofiles
import logging
from .schema.data import ProcessRequest

logger = logging.getLogger('uvicorn.error')

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["v1","data"],
    )

@data_router.post("/upload/{project_id}")


async def upload_file(project_id: str, file: UploadFile,
                    app_settings: settings= Depends(get_settings)):

    
    data_controller = DataController()

    is_valid, message = data_controller.validate_Uploaded_file(file=file)

    if not is_valid:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                             content={
                                 "message":message
                                 }
                                 )


    project_dir_path = ProjectController().get_project_path(project_id=project_id)
    file_path, file_id = data_controller.generate_unique_filepath(
        orig_file_name=file.filename,
        project_id=project_id
    )

    try:
        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(app_settings.FILE_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:

        logger.error(f"Error while uploading file: {e}")

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseEnums.FILE_UPLOAD_FAILED.value
            }
        )

    return JSONResponse(
            content={
                "signal": ResponseEnums.FILE_UPLOAD_SUCCESS.value,
                "file_id": file_id
            }
        )


@data_router.post("/process/{project_id}")
async def process_endpoint(project_id:str,ProcessRequest:ProcessRequest):

    file_id =ProcessRequest.file_id
    chunk_size = ProcessRequest.chunk_size
    overlap_size = ProcessRequest.overlap_size

    Process_controller = ProcessController(project_id=project_id)

    file_content = Process_controller.get_file_content(file_id=file_id)

    file_cunks = Process_controller.process_file_content(
        file_content=file_content,
        file_id=file_id,
        chunk_size=chunk_size,
        overlap_zize=overlap_size
    )

    if file_cunks is None or len(file_cunks) ==0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseEnums.PROCESSING_FAILED.value
            }
        )
    
    return file_cunks