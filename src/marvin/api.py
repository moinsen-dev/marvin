"""
API server for Marvin.

Exposes the Marvin agents through a FastAPI server for remote access.
"""

import os
import tempfile

import uvicorn
from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel

from marvin.agents.main_agent import process_prd

# Create FastAPI app
app = FastAPI(
    title="Marvin API",
    description="API for converting PRDs into AI-Coding-Tasks",
    version="1.0.0",
)


class ProcessResponse(BaseModel):
    """Response model for processing requests"""

    status: str
    results: list[str] | None = None
    error_message: str | None = None


@app.post("/process", response_model=ProcessResponse)
async def process_prd_api(
    prd_file: UploadFile = File(...), codebase_zip: UploadFile | None = File(None)
):
    """
    Process a PRD file and optional codebase zip to generate AI coding task templates.

    Args:
        prd_file: The PRD file to process
        codebase_zip: Optional zip file containing the codebase

    Returns:
        ProcessResponse with results or error
    """
    # Create temporary files for uploads
    prd_temp = None
    codebase_temp = None

    try:
        # Save PRD to temp file
        prd_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".md")
        prd_temp.write(await prd_file.read())
        prd_temp.close()

        # Save and extract codebase if provided
        codebase_path = None
        if codebase_zip:
            import zipfile

            codebase_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".zip")
            codebase_temp.write(await codebase_zip.read())
            codebase_temp.close()

            # Extract to temp directory
            codebase_path = tempfile.mkdtemp()
            with zipfile.ZipFile(codebase_temp.name, "r") as zip_ref:
                zip_ref.extractall(codebase_path)

        # Process the PRD
        result = process_prd(prd_temp.name, codebase_path)

        # Return results
        if result["status"] == "success":
            return ProcessResponse(status="success", results=result["results"])
        else:
            return ProcessResponse(
                status="error",
                error_message=result.get("error_message", "Unknown error"),
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

    finally:
        # Clean up temporary files
        if prd_temp and os.path.exists(prd_temp.name):
            os.unlink(prd_temp.name)

        if codebase_temp and os.path.exists(codebase_temp.name):
            os.unlink(codebase_temp.name)

        # Note: We don't clean up codebase_path as it may still be in use


@app.get("/health")
async def health_check():
    """Simple health check endpoint"""
    return {"status": "ok"}


def start_server(host: str = "0.0.0.0", port: int = 8000):
    """Start the API server"""
    uvicorn.run("marvin.api:app", host=host, port=port, reload=True)
