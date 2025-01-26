from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import discussions

app = FastAPI(title="TokenCourt API", description="Web3 Project Evaluation System")

# Disable CORS. Do not remove this for full-stack development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(discussions.router, prefix="/api/v1", tags=["discussions"])

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}
