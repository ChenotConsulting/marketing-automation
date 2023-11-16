from fastapi import FastAPI, Header
import uvicorn
import os
from dotenv import load_dotenv
from main import Main
import logging
import traceback

load_dotenv()
app = FastAPI()

@app.get("/marketing/user/{userId}/feedly/insights", status_code=200)
def generateFeedlyInsights(userId, days: int = 1):
  try: 
    main = Main()
    insights = main.generateInsights(days=days, userId=userId)
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
      "message": f"Error generating insights: {e}",
      "traceback": traceback.print_exc()
    }
    logging.error(error)
    return error

@app.get("/marketing/user/{userId}/feedly/insights/linkedinpost", status_code=200)
def generateFeedlyInsightsLinkedInPost(userId, days: int = 2):
  try: 
    main = Main()
    post = main.generateLinkedInPost(userId=userId, days=days)
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
      "message": f"Error generating LinkedIn post: {e}"
    }
    return error

@app.get("/marketing/health", status_code=200)
def checkHealth():
  result = {
    "status": "OK"
  }
  logging.info(result)
  return result

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.info("Starting webserver...")

    try:
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=int(os.getenv("PORT", 8080)),
            log_level=os.getenv('LOG_LEVEL', "info"),
            proxy_headers=True
        )
    except Exception as e:
        error = {
           "status": "error",
           "message": f"Error launching application: {e}"
        }
        logging.error(error)