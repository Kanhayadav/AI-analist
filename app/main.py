
from fastapi import FastAPI,HTTPException
from app.service.uploadfile import upload_csv
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pathlib import Path
from pydantic import BaseModel
from app.llm.userQuerySQLtype import answer_query
import shutil

class QueryRequest(BaseModel):
    query: str
    analysis: dict


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://127.0.0.1:5173",],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/query")
async def query_analysis(request: QueryRequest):

    try:

        answer = answer_query(
            request.query,
            request.analysis
        )

        return {
            "answer": answer
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.get("/")
def home():
    return {"message": "Business Intelligence Copilot API"}

app.post("/upload_file/")(upload_csv)


@app.get("/sample-data")
async def sample_data():

    file_path = Path("data/sample/sales.csv")

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Sample dataset not found."
        )

    return FileResponse(
        path=file_path,
        filename="sales.csv",
        media_type="text/csv"
    )



@app.delete("/cleanup")
async def cleanup_storage():

    folders = [
        Path("data/raw"),
        Path("data/cleaned"),
        Path("data/processed"),
    ]

    deleted = 0

    for folder in folders:

        if not folder.exists():
            continue

        for file in folder.iterdir():

            if file.is_file():
                file.unlink()
                deleted += 1

            elif file.is_dir():
                shutil.rmtree(file)
                deleted += 1

    return {
        "message": "Temporary storage cleaned.",
        "deleted_items": deleted
    }