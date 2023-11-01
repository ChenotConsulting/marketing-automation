from lILogin import LILogin
from fastapi import FastAPI

app = FastAPI()

@app.get("/linkedin/profile/{profile_name}")
async def getProfileData(profile_name):
    try:
        return getLIProfileDetails(profile_name)
    except Exception as e:
        return {"Exception": e}

@app.post("/linkedin/profile/{profile_name}/message/send")
async def generateMessageForLinkedInProfile(profile_name: str):
    try:
        return {"message": "Hello World"}
    except Exception as e:
        return {"Exception": e}

def getLIProfileDetails(profileLink):
    liLogin = LILogin()
    liLogin.setup_method()    
    details = liLogin.runLILogin(url=f'https://linkedin.com/in/{profileLink}')
    liLogin.teardown_method()

    # return details
    if(details != []):
        print(details)
        return details
    else:
        for d in details: 
            print(f'Name: {d[0]}')
            print(f'Title: {d[1]}')
            print(f'About: {d[2]}')
            return d

# profileLink = input("Please enter the link to the LinkedIn profile: ")
# getLIProfileDetails(profileLink)