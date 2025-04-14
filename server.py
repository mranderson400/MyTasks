import uvicorn
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from controllers import chatbot_controller, user_controller, task_controller, reminder_controller
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
load_dotenv()


app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))

app.mount("/static", StaticFiles(directory="static"), name="static")

# Include controllers (routers)
app.include_router(user_controller.router)
app.include_router(task_controller.router)
app.include_router(chatbot_controller.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001, reload=True)
