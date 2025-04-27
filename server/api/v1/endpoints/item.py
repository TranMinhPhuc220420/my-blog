from typing import List, Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi import File, UploadFile, status

from pymongo.database import Database
from schemas.item import ItemCreate, Item
from crud import item as crud_item
from db.mongodb import get_mongo_db, set_namespace

from utils import func

router = APIRouter()

@router.post("/{namespace}/items", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_new_item(
    namespace: str, 
    item: ItemCreate, 
    db: Database = Depends(get_mongo_db)
) -> Item:
    """
    Create a new item in the specified namespace.

    Args:
        namespace (str): The namespace to set for the database.
        item (ItemCreate): The item data to create.
        db (Database): The MongoDB database instance.

    Returns:
        Item: The newly created item.
    """
    db = set_namespace(db, namespace)
    new_item = crud_item.create_item(db=db, item=item)
    return new_item

@router.get("/{namespace}/items/", response_model=List[Item], status_code=status.HTTP_200_OK)
def read_items(
    namespace: str, 
    skip: int = 0, 
    limit: int = 100, 
    db: Database = Depends(get_mongo_db)
) -> List[Item]:
    """
    Retrieve a list of items from the specified namespace.

    Args:
        namespace (str): The namespace to set for the database.
        skip (int): The number of items to skip. Defaults to 0.
        limit (int): The maximum number of items to return. Defaults to 100.
        db (Database): The MongoDB database instance.

    Returns:
        List[Item]: A list of items.
    """
    db = set_namespace(db, namespace)
    items = crud_item.get_items(db=db, skip=skip, limit=limit)
    return items

@router.get("/{namespace}/items/{item_id}", response_model=Item, status_code=status.HTTP_200_OK)
def read_item(
    namespace: str, 
    item_id: str, 
    db: Database = Depends(get_mongo_db)
) -> Item:
    """
    Retrieve a specific item by its ID from the specified namespace.

    Args:
        namespace (str): The namespace to set for the database.
        item_id (str): The ID of the item to retrieve.
        db (Database): The MongoDB database instance.

    Returns:
        Item: The requested item.

    Raises:
        HTTPException: If the item is not found.
    """
    db = set_namespace(db, namespace)
    item = crud_item.get_item(db=db, item_id=item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/{namespace}/uploadfile")
async def create_upload_file(
    files: Annotated[
        list[UploadFile], File(description="Multiple files as UploadFile")
    ],
    status_code=status.HTTP_201_CREATED
) -> dict:
    
    storage_dir = func.get_root_path_project() / "storage"
    storage_dir.mkdir(parents=True, exist_ok=True)
    
    for file in files:
        file_path = storage_dir / file.filename
        with open(file_path, "wb") as f:
            f.write(file.file.read())
        
    return {"filenames": [file.filename for file in files]}
