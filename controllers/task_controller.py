from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from models.task_model import Task
from models.user_model import User
from config.database import tasks_collection
from bson import ObjectId

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Create a Task
@router.post("/tasks/create")
async def create_task(
    request: Request,
    title: str = Form(...),
    description: str = Form(...),
    due_date: str = Form(...),
    status: str = Form(...),
):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=403, detail="User not logged in")

    task_data = {
        "title": title,
        "description": description,
        "due_date": due_date,
        "status": status,
        "user_id": ObjectId(user["_id"])
    }

    Task.create_task(task_data)
    return RedirectResponse(url="/welcome", status_code=303)


# Render Create Task Page
@router.get("/tasks/new")
async def new_task(request: Request):
    messages = request.session.pop("messages", []) 
    return templates.TemplateResponse("create.html", {
        "request": request,
        "messages": messages
    })


# Welcome Page with Task List
# FIXME
@router.get("/welcome")
async def get_all_tasks(request: Request):
    user = request.session.get("user")
    if not user:
        return RedirectResponse(url="/", status_code=303)

    tasks = Task.get_all(user["_id"]) 

    messages = request.session.pop("messages", []) 
    response = templates.TemplateResponse("welcome.html", {
        "request": request,
        "user": user,
        "all_tasks": tasks,
        "messages": messages,
    })
    
    # Prevent browser from caching the page
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response





# Delete Task
@router.get("/tasks/{task_id}/delete")
async def delete_task(request: Request, task_id: str):
    Task.delete(task_id)
    request.session["messages"] = ["Task deleted successfully!"]
    return RedirectResponse(url="/welcome", status_code=303)


# Edit Task Page
@router.get("/tasks/{task_id}/edit")
async def edit_task(request: Request, task_id: str):
    this_task = Task.get_one(task_id)
    if not this_task:
        raise HTTPException(status_code=404, detail="Task not found")

    return templates.TemplateResponse("edit.html", {
        "request": request,
        "task": this_task
    })


# Update Task
@router.post("/tasks/{task_id}/update")
async def update_task(
    request: Request,
    task_id: str,
    title: str = Form(...),
    description: str = Form(...),
    due_date: str = Form(...),
    status: str = Form(...)
):
    task_data = {
        "title": title,
        "description": description,
        "due_date": due_date,
        "status": status
    }

    updated = Task.update(task_id, task_data)

    if updated:
        request.session["messages"] = ["Task updated successfully!"]
    else:
        request.session["messages"] = ["Error updating task!"]

    return RedirectResponse(url="/welcome", status_code=303)


# View Task Details
@router.get("/tasks/{task_id}/view")
async def get_one_task(request: Request, task_id: str):
    user = request.session.get("user")
    this_task = Task.get_one(task_id)
    if not this_task:
        raise HTTPException(status_code=404, detail="Task not found")

    return templates.TemplateResponse("view.html", {
        "request": request,
        "task": this_task,
        "user": user,
    })
