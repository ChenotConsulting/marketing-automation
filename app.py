from fastapi import FastAPI
import uvicorn
import os
from dotenv import load_dotenv
from main import Main

load_dotenv()
app = FastAPI()

@app.get("/marketing/feedly/insights", status_code=200)
def generateFeedlyInsights(days: int = 1):
  try: 
    main = Main()
    insights = main.generateInsights(days)
    results = {
      "status": "OK",
      "results": {
        "insights": insights[0],
        "urls": insights[1]
      }
    }
    return results
  except Exception as e:
    error = {
      "status": "Error", 
      "error": e
    }
    return error

@app.get("/marketing/feedly/insights/linkedinpost", status_code=200)
def generateFeedlyInsightsLinkedInPost(days: int = 2):
  try: 
    main = Main()
    post = main.generateLinkedInPost(days)
    results = {
      "status": "OK",
      "results": {
        "post": post[0],
        "urls": post[1]
      }
    }
    return results
  except Exception as e:
    error = {
      "status": "Error", 
      "error": e
    }
    return error

@app.get("/marketing/health", status_code=200)
def checkHealth():
  result = {
    "status": "OK"
  }
  return result

if __name__ == "__main__":
    print("Starting webserver...")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8080)),
        debug=os.getenv("DEBUG", False),
        log_level=os.getenv('LOG_LEVEL', "info"),
        proxy_headers=True
    )