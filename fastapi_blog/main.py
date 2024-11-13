from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI()

app.mount('/static', StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
HR = templates.TemplateResponse # HR -> HtmlResponse


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
	return HR("index.html", context={"request": request})


@app.get("/about/", response_class=HTMLResponse)
def about(request: Request):
	return HR("about.html", context={"request": request})


@app.get("/user/", response_class=HTMLResponse)
def user(request: Request, user="default"):
	return HR("user.html", context={"request": request, "user":user})


@app.get("/post/", response_class=HTMLResponse)
def post(request: Request):
	return HR("post.html", context={"request": request})


@app.get("/signup/", response_class=HTMLResponse)
def signup(request: Request):
	return HR("signup.html", context={"request": request})


@app.get("/login/", response_class=HTMLResponse)
def login(request: Request):
	return HR("login.html", context={"request": request})