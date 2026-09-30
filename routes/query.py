from fastapi import APIRouter, UploadFile
from Backend.controllers.query_controllers import process_query

router = APIRouter()

@router.post("/query")
async def query(file: UploadFile):
    return await process_query(file)