from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from rss import retrieveRSS

app = FastAPI()

origins = [
    "*",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow specific origins
    allow_credentials=True,  # Allow cookies and credentials
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


@app.get("/status")
async def serverStatus():
    return {"message": "RSS Api is online"}


@app.get("/rss")
async def rss(url: str):
    """
    - `url`: The RSS feed URL to parse (passed as a query parameter).
    """
    feed = retrieveRSS(url)
    if feed.bozo:
        return {"message": "Failed to parse feed", "details": str(feed.bozo_exception)}
    response = {"data": feed}
    return JSONResponse(response)
