# marketing-automation
This application retrieves the articles in a defined folder created in Feedly and for each article extracts the key insights and trends. An email is sent to the specified recipient with the insights.
It also allows the creation of a LinkedIn post with GPT-4 and an accompanying image generated with DALL-E 3. Both are sent as an email to the specified recipient. 

To run this application, you need to add a .env file with the following key/value pairs.

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
LINKEDIN_ACCESS_TOKEN=[YOUR LINKEDIN ACCESS TOKEN] \

