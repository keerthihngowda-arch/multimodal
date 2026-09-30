from fastapi import FastAPI
from Backend.routes.query import router
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

# Serve audio files
app.mount("/audio", StaticFiles(directory="Backend/audio"), name="audio")

@app.get("/")
def root():
    return {"message": "Voice AI Backend Running"}