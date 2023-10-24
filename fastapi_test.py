from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import requests
import os
from nrf_ble_lib_helper import dongle_init, scan_start, scan_stop

app = FastAPI(title="Whatever🤔")

# Test for Nordic BLE functions

@app.get("/dongleinit", tags=["nordic"])
async def nordic_dongleinit():
    """Init the BLE dongle"""
    code = dongle_init()
    return {"errorcode": code}

@app.get("/scanstart", tags=["nordic"])
async def nordic_scanstart():
    """Start BLE advertising"""
    code = scan_start()
    return {"errorcode": code}

@app.get("/scanstop", tags=["nordic"])
async def nordic_scanstop():
    """Stop BLE advertising"""
    code = scan_stop()
    return {"errorcode": code}

# Directory to store uploaded files
upload_dir = Path("tmp")

# Ensure the upload directory exists
upload_dir.mkdir(parents=True, exist_ok=True)

# Mount the tmp folder for static route (shouldn't do this but I'm lazy for the crappy design)
app.mount("/tmp", StaticFiles(directory=Path("tmp")), name="tmp")

@app.post("/uploadfile/", tags=["test"])
async def upload_file(file: UploadFile):
    # Annotation also effect the Swagger API description 
    """
    Upload file by given file, return json with filename
    - **return json:** file name and its server path
    """
    # Save the uploaded file to the server
    file_path = upload_dir / file.filename
    with file_path.open("wb") as buffer:
        buffer.write(file.file.read())

    return {"filename": file.filename, "path":f"/{upload_dir}/{file.filename}"}

@app.get("/downloadfile/{file_name}", tags=["test"])
async def download_file(file_name: str):
    """
    Download file by given file name, return file to download directly
    """
    # Prepare the file path for download
    file_path = upload_dir / file_name

    # Check if the file exists
    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")

    # Return the file as a response
    return FileResponse(file_path, headers={"Content-Disposition": f"attachment; filename={file_name}"})

# Hide root endpoint in swagger document
@app.get("/", include_in_schema=False)
def defult_root():
    return {"message": "visit /docs to check APIs"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8765)

