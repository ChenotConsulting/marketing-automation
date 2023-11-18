from fastapi import FastAPI, Header
from typing import Union
from typing_extensions import Annotated
import uvicorn
import os
from dotenv import load_dotenv
from main import Main
import logging
import traceback

load_dotenv()
app = FastAPI()

def authoriseRequest(x_api_key):
   auth_api_key = os.getenv('AUTH_API_KEY')
   if auth_api_key == x_api_key:
      return True
   else:
      return False

@app.get("/marketing/user/{userId}/feedly/insights", status_code=200)
def generateFeedlyInsights(userId, days: int = 1, x_api_key: Annotated[Union[str, None], Header()] = None):
  try: 
    if authoriseRequest(x_api_key):
      main = Main()
      insights = main.generateInsights(days=days, userId=userId)
      logging.info(f'Insights retrieved: {insights}')
      results = {
        "status": "OK" if insights is not None else "Not Found",
        "results": {
          "insights": insights[0] if insights is not None else "No insights.",
          "urls": insights[1] if insights is not None else "No URLs."
        }
      }
      return results
    else:
      results = {
        "status": "Not Authorized",
        "message": "You are not authorized to access this service."
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
def generateFeedlyInsightsLinkedInPost(userId, days: int = 2, x_api_key: Annotated[Union[str, None], Header()] = None):
  try: 
    if authoriseRequest(x_api_key):
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
    else:
      results = {
        "status": "Not Authorized",
        "message": "You are not authorized to access this service."
      }
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

    # generateFeedlyInsights(userId='1699685958170x317202834451805900', days=3)