from fastapi import FastAPI, UploadFile, File, Query, HTTPException
import os
import aiofiles
from fastapi.responses import FileResponse
from app.services.documents import DocumentsService
from app.services.embeddings import EmbeddingsService

embeddings_service = EmbeddingsService()
documents_service = DocumentsService()

app = FastAPI()


@app.get("/search")
async def fetch_document_by_query(query: str, limit: int = Query(3)):
    try:
        query_vector = await embeddings_service.embed(query)

        similar_documents = documents_service.get_similar_by_query(query_vector, limit)

        if not similar_documents or "ids" not in similar_documents:
            raise ValueError("Wrong response format")

        # now paths to files saved as ids for simplicity, should be saved in metadata
        file_paths = similar_documents["ids"][0]
    except Exception as e:
        # more exceptions should be handled separately, unexpected one shouldn't provide reason but log it
        raise HTTPException(status_code=500, detail=f"Error while fetching related files: {e}")

    return {'files': file_paths}


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    """
        On production this method has to be async with queue approach with stages and custom exceptions
        Stages:
            Check if file already exists and if it updated with hash sum (could be separate method)
            1. Upload file (validation, chunking if needed), storing data with s3
            2. Retrieving content from the file and sending to embedding service (handling with rate-limit)
            3. Saving vectors and metadata in vector DB
        I would make current service stateless, DB, file storage should be placed on separate nodes
    """

    try:
        file_path = os.path.join('documents', file.filename)

        """
            Now it doesn't support binary files as pdf, could be handled with external libraries
            For example tika or langchain document loader
        """

        async with aiofiles.open(file_path, 'wb') as buffer:
            content = await file.read()
            await buffer.write(content)

        content_vector = await embeddings_service.embed(content.decode('utf-8'))
        documents_service.save_new_embedding(file_path, content_vector)
    except Exception as e:
        # more exceptions should be handled separately, unexpected one shouldn't provide reason but log it
        raise HTTPException(status_code=500, detail=f"Error while uploading file: {e}")

    return {"message": 'file uploaded'}


@app.get("/documents/{file_name}")
def get_document(file_name: str):
    """
        Providing content by file path
        This could be handled by file storage server (nginx) itself without application layer
    """

    file_path = os.path.join('documents', file_name)
    if os.path.exists(file_path):
        return FileResponse(file_path)

    return {"error": "File not found"}
