from fastapi import APIRouter, Depends, HTTPException, status
from datetime import date
import datetime as dt
from beanie import PydanticObjectId

from ..models import (
    CreateUpdateTodoItem,
    TodoItem,
)


router = APIRouter(prefix="/todo-list", tags=["todo-item"])


@router.get("/{list_id}/", response_model=list[TodoItem])
async def get_lists():
    query = TodoItem.all()
    return await query.to_list()


@router.post(
    "/{list_id}/", status_code=status.HTTP_201_CREATED, response_model=TodoItem
)
async def create_list(list: CreateUpdateTodoItem):
    return await TodoItem(**list.dict(), date_created=date.today()).save()


@router.get("/{list_id}/{todo_item_id}", response_model=TodoItem)
async def get_list(list_id: PydanticObjectId) -> TodoItem:
    todo_item = await TodoItem.get(document_id=list_id)
    if not todo_item:
        raise HTTPException(status_code=404, detail="Todo list not found")
    return todo_item


@router.put("/{list_id}/{todo_item_id}", response_model=TodoItem)
async def update_todo(
    list_id: PydanticObjectId, body: CreateUpdateTodoItem
) -> TodoItem:
    todo_list = await TodoItem.get(document_id=list_id)

    if not todo_list:
        raise HTTPException(status_code=404, detail="Todo list not found")

    await todo_list.update({"$set": body.dict(exclude_unset=True)})
    todo_list.updatedDate = date.today()
    return await todo_list.save()


@router.delete("/{list_id}/{todo_item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(list: PydanticObjectId) -> None:
    todo_item = await TodoItem.get(document_id=list_id)
    if not todo_item:
        raise HTTPException(status_code=404, detail="Todo list not found")
    await todo_item.delete()
