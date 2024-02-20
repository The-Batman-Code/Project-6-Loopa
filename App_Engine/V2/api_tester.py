import vertexai
from fastapi import FastAPI
from fastapi import Request
import uvicorn
import uuid
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import HTMLResponse
import os
from chat_session import CreateChatSession
import time
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi.responses import FileResponse
from google.oauth2 import service_account

app = FastAPI()
scheduler = BackgroundScheduler()
scheduler.start()

credentials = service_account.Credentials.from_service_account_file("loopa_key.json")

vertexai.init(
    project="ENTER YOUR GCP PROJECT ID HERE",
    location="us-central1",
    credentials=credentials,
)
sessions = {}
session_id_timers = {}

app.mount(
    "/static",
    StaticFiles(directory="static/"),
    name="static",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_session_id(request: Request, call_next):
    global session_id_timers

    if request.url.path == "/reset_chat":
        request.cookies.pop("session_id")

    session_id = request.cookies.get("session_id")
    if session_id is None:
        session_id = str(uuid.uuid4())
    response = await call_next(request)
    response.set_cookie(key="session_id", value=session_id)
    session_id_timers.update({session_id: time.time()})
    print(f"I am printing here: {session_id_timers}")
    print(session_id)
    return response


@app.get("/")
async def get_index():
    return FileResponse("static/index.html")


@app.post("/chat")
async def chat(request: Request):
    session_id = request.cookies.get("session_id")
    if not session_id:
        return {"error": "Session ID not found"}
    if session_id not in sessions:
        sessions.update({session_id: CreateChatSession()})
        session_id_timers.update({session_id: time.time()})
    print(f"I am in /chat endpoint:{sessions}")
    form = await request.form()
    user_text = form["chat"]
    if session_id in sessions.keys():
        session = sessions[session_id]
        print(session)
        ans = session.create_chat_session(user_text)
        session_id_timers.update({session_id: time.time()})
        print(ans)
    return ans


@app.get("/reset_chat")
async def chat_reset(request: Request):
    global session_id_timers
    to_be_deleted_session_id = request.cookies.get("session_id")
    print(f"To be deleted : {to_be_deleted_session_id}")
    print(f"Old sessions : {sessions},\n Old session timers ; {session_id_timers}")
    if to_be_deleted_session_id in sessions:
        del sessions[to_be_deleted_session_id]
        del session_id_timers[to_be_deleted_session_id]
    print(f"Sessions : {sessions},\n New session Id timer : {session_id_timers}")


def check_last_request():
    global sessions
    for session_time in session_id_timers.copy():
        if time.time() - session_id_timers.get(session_time) > 600:
            print(f"this is session_time : {session_time}")
            print(f"this is session_id_timers : {session_id_timers}")
            del session_id_timers[session_time]
            del sessions[session_time]
            print(f"this is session_id_timers updated: {session_id_timers}")
            print(sessions)


scheduler.add_job(check_last_request, "interval", seconds=60)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost")
