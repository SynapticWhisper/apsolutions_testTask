"""
Document API router module.

This module defines the API routes for managing documents, including searching and deleting
documents. It utilizes FastAPI's `APIRouter` to define endpoints related to document operations,
integrating with the `DocumentCRUD` service for database and Elasticsearch interactions.

Key Endpoints:
- `/docs/search`:               Search for documents based on a query phrase, returning a list of
                                documents that match the query.
- `/docs/delete/{document_id}`: Delete a document by its ID, removing it from both the database
                                and Elasticsearch.

All routes are prefixed with `/docs` and tagged with "Documents" for easy organization within the
API documentation.
"""

from typing import List, Annotated, Optional
from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import JSONResponse
from src.docs.schemas import DocumentSchema, CreateDocument
from src.docs.service import DocumentCRUD

router = APIRouter(
    prefix="/docs",
    tags=["Documents"]
)


@router.post(
    "/add_documnet",
    status_code=status.HTTP_201_CREATED,
    response_class=JSONResponse
)
async def add_document(
    new_document: CreateDocument,
    service: DocumentCRUD = Depends()
):
    """
    Adds a new document to the database.

    Parameters:
    - new_document (CreateDocument): An object containing the data for the document to be added.

    Returns:
    - JSONResponse with the created document's data and a 201 (Created) status on success.
    """
    return await service.create(new_document)


@router.get("/search", response_model=Optional[List[DocumentSchema]])
async def get_documents(
    query: str,
    limit: Annotated[int, Query(title="Number of items to return", ge=0, le=20)] = 20,
    service: DocumentCRUD = Depends()
):
    """
    Search for documents by a query phrase.

    This endpoint allows users to search for documents based on a specified query string.
    The search is performed using an integrated Elasticsearch service, which returns documents
    matching the query. The number of returned documents is limited by the `limit` parameter.

    Args:
        query (str): The query string used to search for documents.
        limit (int, optional): The maximum number of documents to return. Defaults to 20.

    Returns:
        List[DocumentSchema]: A list of documents that match the search query.
    """
    return await service.search_and_get_many(query=query, limit=limit)


@router.delete("/delete/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_documnet(
    document_id: int,
    service: DocumentCRUD = Depends()
):
    """
    Delete a document by its ID.

    This endpoint deletes a document from the database and Elasticsearch index based on the provided
    document ID. It raises a 404 error if the document is not found.

    Args:
        document_id (int): The ID of the document to be deleted.

    Returns:
        None: Returns HTTP 204 status code indicating successful deletion with no content in the response.
    """
    return await service.delete(document_id)
