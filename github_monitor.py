from fastapi import FastAPI, Request, HTTPException
import uvicorn
from notifier import send_alert

app = FastAPI(title="GitHub Webhook Monitor")

@app.get("/")
def health():
    return {
        "status": "running",
        "service": "github-repository-monitor"
    }

@app.post("/webhook/github")
async def github_webhook(request: Request):
    """
    Listens for GitHub webhook events.
    Configure this endpoint in your GitHub repo settings to trigger on workflow runs.
    """
    payload = await request.json()
    
    # Check if this is a workflow run event
    if "workflow_run" in payload:
        workflow = payload["workflow_run"]
        status = workflow.get("conclusion")
        
        # Only alert on failure
        if status == "failure":
            repository = payload.get("repository", {}).get("full_name", "Unknown Repo")
            workflow_name = workflow.get("name", "Unknown Workflow")
            html_url = workflow.get("html_url", "No URL provided")
            
            print(f"\n🚨 GitHub Action Failed: {repository} - {workflow_name}")
            
            subject = f"🚨 GitHub CI/CD Failure - {repository}"
            body = f"""GitHub Repository Incident Detected

Repository:
{repository}

Workflow:
{workflow_name}

Status:
{status}

Details:
Your GitHub CI/CD workflow has failed.

View GitHub Actions:
{html_url}

--------------------------------
GitHub Repository Monitor"""
            
            send_alert(subject, body)
            
            return {"status": "alert_sent"}

    return {"status": "ignored"}


if __name__ == "__main__":
    print("🚀 Starting GitHub Webhook Monitor on port 8000...")
    uvicorn.run("github_monitor:app", host="0.0.0.0", port=8000, reload=True)
