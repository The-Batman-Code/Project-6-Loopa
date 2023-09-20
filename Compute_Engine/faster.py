from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import uuid
import os
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from ydata import ydata_main
import time
from apscheduler.schedulers.background import BackgroundScheduler
from tables import table_queries_1, table_queries_2, data_retrieval_main
import asyncio
from concurrent.futures import ThreadPoolExecutor


app = FastAPI()
scheduler = BackgroundScheduler()
scheduler.start()

session_id_timers = {}

app.mount(
    "/static",
    StaticFiles(directory="/home/ksgcpcloud/myapp/Ver_1/static"),
    name="static",
)

app.mount(
    "/reports",
    StaticFiles(directory="/home/ksgcpcloud/myapp/reports"),
    name="reports",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_session_id(request: Request, call_next):
    global session_id_timers
    print(f"Previous ID : {request.cookies.get('session_id')}")
    if request.url.path == "/reset_chat":
        request.cookies.pop("session_id")

    session_id = request.cookies.get("session_id")
    print(f"New ID : {request.cookies.get('session_id')}")
    if session_id is None:
        session_id = str(uuid.uuid4())
    response = await call_next(request)
    response.set_cookie(key="session_id", value=session_id)
    session_id_timers.update({session_id: time.time()})
    print(f"I am printing here: {session_id_timers}")
    print(session_id)
    return response


@app.get("/")
async def root():
    try:
        with open("Ver_1/static/index.html", "r") as html_file:
            html_content = html_file.read()
        return HTMLResponse(content=html_content)
    except Exception as e:
        print(f"Error loading index.html: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.post("/data_retrieval_text")
async def retrieve_data(request: Request):
    global session_id_timers
    form = await request.form()
    data_retrieval_text = form["data_retrieval_text"]
    print(data_retrieval_text)
    session_id = request.cookies.get("session_id")
    session_id_timers.update({session_id: time.time()})
    return data_retrieval_main(data_retrieval_text, session_id)


@app.post("/data_query_chat_1")
async def data_query_chat_1(request: Request):
    global session_id_timers
    form = await request.form()
    data_query_chat_text = form["data_query_chat_1"]
    session_id = request.cookies.get("session_id")
    session_id_timers.update({session_id: time.time()})
    print(session_id_timers)
    return table_queries_1(data_query_chat_text, session_id)


@app.post("/data_query_chat_2")
async def data_query_chat_2(request: Request):
    global session_id_timers
    form = await request.form()
    data_query_chat_text = form["data_query_chat_2"]
    session_id = request.cookies.get("session_id")
    session_id_timers.update({session_id: time.time()})
    return table_queries_2(data_query_chat_text, session_id)


def get_report_urls(session_id):
    # session_id = request.cookies.get("session_id")
    report_dir = f"/home/ksgcpcloud/myapp/reports/{session_id}/"

    # Check if the session directory exists
    if not os.path.exists(report_dir):
        raise HTTPException(status_code=404, detail="Session reports not found")

    # List the HTML report files in the session directory
    files = [f for f in os.listdir(report_dir) if f.endswith(".html")]

    report_urls = [f"/reports/{session_id}/{file}" for file in files]
    return report_urls


@app.get("/dashboard")
async def dashboard(request: Request):
    global session_id_timers
    session_id = request.cookies.get("session_id")
    session_id_timers.update({session_id: time.time()})

    executor = ThreadPoolExecutor()

    loop = asyncio.get_event_loop()
    loop.set_default_executor(executor)

    # loop = asyncio.get_event_loop()
    task = loop.create_task(ydata_main(session_id))

    await task
    report_urls = get_report_urls(session_id)
    print(report_urls)

    return report_urls


@app.get("/reset_chat")
async def reset_chat(request: Request):
    global session_id_timers
    session_id = request.cookies.get("session_id")
    del session_id_timers[session_id]
    print(session_id_timers)
    list_names = ["csv_data", "data", "reports"]
    location = []
    for name in list_names:
        dir = "/home/ksgcpcloud/myapp/"
        try:
            temp = os.listdir(f"{dir}" + name + "/" + session_id)
            print(f"this is temp : \n{temp}")
        except:
            continue
        try:
            for i in range(len(temp)):
                location.append(f"{dir}" + name + "/" + session_id + "/" + temp[i])
            print(f"this is location : \n{location}")
        except:
            continue
        print(f"this is final location : \n{location}")
    for loc in location:
        if session_id in loc:
            os.remove(loc)


def check_last_request():
    global session_id_timers
    for session_time in session_id_timers.copy():
        if time.time() - session_id_timers.get(session_time) > 600:
            del session_id_timers[session_time]
            print(session_id_timers)
            list_names = ["csv_data", "data", "reports"]
            location = []
            for name in list_names:
                dir = "/home/ksgcpcloud/myapp/"
                try:
                    temp = os.listdir(f"{dir}" + name + "/" + session_time)
                    print(f"this is temp : \n{temp}")
                except:
                    continue
                try:
                    for i in range(len(temp)):
                        location.append(
                            f"{dir}" + name + "/" + session_time + "/" + temp[i]
                        )
                    print(f"this is location : \n{location}")
                except:
                    continue
                print(f"this is final location : \n{location}")
            for loc in location:
                if session_time in loc:
                    os.remove(loc)

    scheduler.add_job(check_last_request, "interval", seconds=60)


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="localhost",
        port=8090,
    )


# def test_read_items():
#     with TestClient(app) as client:

# chat reset
# data reset
# shutdown
