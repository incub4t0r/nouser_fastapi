################################
# General imports
################################

import uvicorn
from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import os

################################
# Variable setup
################################

ROOT = os.path.dirname(os.path.abspath(__file__))

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="DONTUSEMEINPRODUCTION")

################################
# Custom functions
################################

@app.middleware("http")
async def session_middleware(request: Request, call_next):
    response = await call_next(request)
    session = request.cookies.get('session')
    return response

def check_session(request: Request):
    session = request.cookies.get('session')
    if "user_id" in request.session:
        print(f"user_id found in session: {request.session['user_id']}")
        return True
    else:
        print("no session cookie found, starting new session...")
        return False

def new_session(request: Request):
    request.session["user_id"] = os.urandom(32).hex()
    return request

################################
# FastAPI Endpoints
################################

@app.get("/")
def root(request: Request):
    if not check_session(request):
        request = new_session(request)
    return {"message": "Hello, your uuid is " + request.session["user_id"]}

################################
# Main
################################

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
