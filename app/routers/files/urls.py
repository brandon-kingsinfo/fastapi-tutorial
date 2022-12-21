from fastapi import APIRouter, Request, HTTPException, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
import shutil
import aiofiles

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/upload", response_class=HTMLResponse)
async def get_upload_form(request:Request):
    return templates.TemplateResponse("basic-upload.html", {"request":request})

@router.post("/upload")
async def post_upload_form(in_file: UploadFile = File(...)):
    out_file_path = Path("static") / in_file.filename
    async with aiofiles.open(out_file_path, 'wb') as out_file:
        content = await in_file.read()  # async read
        await out_file.write(content)  # async write  

    return {'file':in_file.filename}
