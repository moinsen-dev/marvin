"""FastAPI server for Marvin."""

from datetime import datetime

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from marvin import __version__

app = FastAPI(
    title="Marvin API",
    description="API for Marvin, the intelligent task generator for AI coding assistants",
    version=__version__,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Data models for the API
class AnalyzeRequest(BaseModel):
    """Request to analyze a PRD."""

    prd_url: str | None = None
    codebase_url: str | None = None
    output_format: str = "xml"


class AnalyzeResponse(BaseModel):
    """Response to an analyze request."""

    job_id: str
    status: str
    created_at: datetime
    estimated_completion: datetime | None = None


class JobStatus(BaseModel):
    """Status of an analysis job."""

    job_id: str
    status: str
    progress: float
    created_at: datetime
    updated_at: datetime
    estimated_completion: datetime | None = None
    results: list[dict] | None = None
    error: str | None = None


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "Marvin API",
        "version": __version__,
        "status": "running",
        "description": "The intelligent task generator for AI coding assistants",
    }


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    """Analyzes a PRD and returns a job ID."""
    # Here, the actual analysis would be started
    job_id = "job_" + datetime.now().strftime("%Y%m%d%H%M%S")

    return AnalyzeResponse(
        job_id=job_id,
        status="queued",
        created_at=datetime.now(),
        estimated_completion=datetime.now(),
    )


@app.post("/analyze/upload", response_model=AnalyzeResponse)
async def analyze_upload(
    prd_file: UploadFile = File(...),
    codebase_zip: UploadFile | None = None,
    output_format: str = "xml",
):
    """Analyzes an uploaded PRD and returns a job ID."""
    # Here, the actual analysis would be started
    job_id = "job_" + datetime.now().strftime("%Y%m%d%H%M%S")

    return AnalyzeResponse(
        job_id=job_id,
        status="queued",
        created_at=datetime.now(),
        estimated_completion=datetime.now(),
    )


@app.get("/jobs/{job_id}", response_model=JobStatus)
async def get_job_status(job_id: str):
    """Returns the status of a job."""
    # Here, the actual job status would be queried
    if not job_id.startswith("job_"):
        raise HTTPException(status_code=404, detail="Job not found")

    return JobStatus(
        job_id=job_id,
        status="processing",
        progress=0.5,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        estimated_completion=datetime.now(),
    )


@app.get("/version")
async def version():
    """Returns the version."""
    return {"version": __version__}


def start_server(host: str = "127.0.0.1", port: int = 8000):
    """Starts the API server."""
    import uvicorn

    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    start_server()
