# marketing-automation
This application can be run locally as a script or can be deployed as an API. To run it locally simply type the command ```python3 main.py``` in the terminal and select an option from the prompt.
When running it as an API, use the command ```python3 app.py```.

The application retrieves the articles in a defined folder created in Feedly and for each article extracts the key insights and trends. An email is sent to the specified recipient with the insights.
It also allows the creation of a LinkedIn post with GPT-4 and an accompanying image generated with DALL-E 3. Both are sent as an email to the specified recipient. 

To run this application locally, you need to add a .env file with the following key/value pairs. To run it as an API in a Cloud-based platform, you will need to add the environment variables where relevant. You will also need a MongoDB Atlas database, which you can create for free: [Getting Started with MongoDB Atlas](https://www.mongodb.com/docs/atlas/getting-started/). 

#FEEDLY \
FEEDLY_USER_ID=[YOUR FEEDLY USER ID] \
FEEDLY_ACCESS_TOKEN=[YOUR FEEDLY ACCESS TOKEN] # https://developer.feedly.com/v3/developer \
FEEDLY_REFRESH_TOKEN=[YOUR FEEDLY REFRESH TOKEN] \
FEEDLY_SANDBOX_URL=https://sandbox7.feedly.com \
FEEDLY_API_URL=https://cloud.feedly.com \
FEEDLY_FOLDERS=[YOUR FEEDLY FOLDER IDs]  \

#OPENAI \
OPENAI_API_KEY=[YOUR OPENAI API KEY] \

#GOOGLE EMAIL \
EMAIL_USERNAME=[YOUR GOOGLE EMAIL ADDRESS] \
EMAIL_PASSWORD=[YOUR GOOGLE APP PASSWORD] \
EMAIL_RECIPIENT=[THE RECIPIENT'S EMAIL ADDRESS] \

#LINKEDIN \
LINKEDIN_USERNAME=[YOUR LINKEDIN USERNAME] \
LINKEDIN_PASSWORD=[YOUR LINKEDIN PASSWORD] \
LINKEDIN_ACCESS_TOKEN=[YOUR LINKEDIN ACCESS TOKEN] \

#ONLY REQUIRED TO RUN THE APPLICATION AS AN API
#MONGODB \
MONGODB_URL=[YOUR MONGODB DB DOMAIN] \
MONGODB_USERNAME=[YOUR MONGODB DB USERNAME] \
MONGODB_PASSWORD=[YOUR MONGODB DB PASSWORD] \

#AUTHORIZATION \
AUTH_API_KEY=[YOUR APPLICATION API KEY. MUST BE GENERATED] # This is used to secure access to the API \

