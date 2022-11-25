from fastapi import APIRouter, Depends, HTTPException, status
from datetime import date
import datetime as dt
from beanie import PydanticObjectId

from ..models import (
    CreateUpdateTodoList,
    TodoList,
)


router = APIRouter(prefix="/todo-list", tags=["todo-list"])


@router.get("/", response_model=list[TodoList])
async def get_lists():
    query = TodoList.all()
    return await query.to_list()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TodoList)
async def create_list(body: CreateUpdateTodoList):
    todo_list = await TodoList(
        **body.dict(), createdDate=dt.datetime.now(dt.timezone.utc)
    ).save()
    return todo_list


@router.get("/{list_id}", response_model=TodoList)
async def get_list(list_id: PydanticObjectId) -> TodoList:
    todo_list = await TodoList.get(document_id=list_id)
    if not todo_list:
        raise HTTPException(status_code=404, detail="Todo list not found")
    return todo_list


@router.put("/{list_id}", response_model=TodoList)
async def update_todo(
    list_id: PydanticObjectId, body: CreateUpdateTodoList
) -> TodoList:
    todo_list = await TodoList.get(document_id=list_id)
    if not todo_list:
        raise HTTPException(status_code=404, detail="Todo list not found")
    await todo_list.update({"$set": body.dict(exclude_unset=True)})
    todo_list.updatedDate = dt.datetime.now(dt.timezone.utc)
    return await todo_list.save()


@router.delete("/{list_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(list_id: PydanticObjectId) -> None:
    todo_list = await TodoList.get(document_id=list_id)
    if not todo_list:
        raise HTTPException(status_code=404, detail="Todo list not found")
    await todo_list.delete()
