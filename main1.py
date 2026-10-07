from fastapi import FastAPI

from github_webhook import router


app = FastAPI(
    title="GitHub Repository Monitor"
)

app.include_router(router)


@app.get("/")
def health():
    return {
        "status": "running",
        "service": "github-repository-monitor"
    }