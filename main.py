import os
from dotenv import load_dotenv
import requests
import json
from datetime import datetime, timedelta
import openai
import smtplib
import tiktoken
import sys

# Load environment variables
load_dotenv()
FEEDLY_USER_ID = os.getenv('FEEDLY_USER_ID')
FEEDLY_ACCESS_TOKEN = os.getenv('FEEDLY_ACCESS_TOKEN')
FEEDLY_API_URL = os.getenv('FEEDLY_API_URL')
FEEDLY_FOLDERS = os.getenv('FEEDLY_FOLDERS')
FEEDLY_FOLDERS_LIST = FEEDLY_FOLDERS.split(',')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
EMAIL_USERNAME = os.getenv('EMAIL_USERNAME')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_RECIPIENT = os.getenv('EMAIL_RECIPIENT')
MODEL = 'gpt-4-1106-preview'
MAX_TOKENS = 4097

# Setup clients
feedly = requests.Session()
feedly.headers = {'authorization': 'OAuth ' + FEEDLY_ACCESS_TOKEN}
openai.api_key = OPENAI_API_KEY

def count_tokens(text):
    enc = tiktoken.get_encoding("cl100k_base")
    token_count = enc.encode(text)
    
    return len(token_count)

def callOpenAIChat(role, prompt):
  response = openai.ChatCompletion.create(
    model=MODEL, 
    temperature=0.2,
    n=1,
    messages=[
      {'role': 'system', 'content': role}, 
      {'role': 'user', 'content': prompt}
    ]
  )
  return response['choices'][0]['message']['content']

def callOpenAIImage(prompt):
  response = openai.Image.create(
    model="dall-e-3",
    prompt=prompt,
    size="1024x1024",
    quality="standard",
    n=1,
  )

  return response.data[0].url

def generateInsights(articles, folder_name, urls, titles, summaries, contents):
  """
  Generate insights from the articles
  """
  print(f'Generating insights from articles in folder: {folder_name}')
  article_prompts = [f'URL: {url}\nTitle: {title}\nSummary: {summary}\nContent: {content}\n' for url, title, summary, content in zip(urls, titles, summaries, contents)]
  
  role = 'You are a research analyst writing in UK English.'
  insights = ""
  current_prompt = f'Extract the key insights & trends from these {len(articles)} articles and highlight any resources worth checking. For each key insight, mention the source article:\n'
  for article_prompt in article_prompts:
    if count_tokens(current_prompt + article_prompt) > MAX_TOKENS:
      insights = callOpenAIChat(role, current_prompt)
      current_prompt = article_prompt
    else:
      current_prompt += article_prompt

  # Process remaining articles
  if current_prompt:
    insights = callOpenAIChat(role, current_prompt)

  # print('========================================================================================')
  # print(f'Insights for folder {folder_name}:')
  # print(f'Number of articles analysed: {len(articles)}\n')
  # print(insights)
  # print('========================================================================================')

  sendEmail(subject=f'Feedly Insights from {len(articles)} articles for folder {folder_name}', body=insights, urls=urls)

def generateLinkedInPost(articles, folder_name, urls, titles, summaries, contents):
  """
  Generate a LinkedIn post from the articles
  """
  print(f'Generating LinkedIn post from articles in folder: {folder_name}')
  role = 'You are a marketing manager working for a consultancy called ProfessionalPulse.'
  prompt = f'Imagine that you are a marketing manager for a consultancy called ProfessionalPulse.'
  prompt += f'\nContext: At ProfessionalPulse, we\'re passionate about leveraging technology to transform the operations of Business Services teams within Professional Services Firms.'
  prompt += f'Our journey began in the dynamic realm of IT and consultancy, and was inspired by real-life challenges faced by these teams.'
  prompt += f'Today, we use our expertise and unique approach to help these teams navigate their challenges, boost efficiency, and strike a balance between their professional and personal lives.'
  prompt += f'Discover more about our ethos, our journey, and how we can help you.'
  prompt += f'\nYou are tasked with extracting insights and generate a LinkedIn post including the links to the relevant articles from these {len(articles)} articles:'
  for url, title, summary, content in zip(urls, titles, summaries, contents):
    prompt += f'\nURL: {url}\nTitle: {title}\nSummary: {summary}\nContent: {content}\n'
  prompt += f'\nDo not use the context in the post. It\'s for your information only.'
  prompt += f'\nYou should only talk about the insights extracted from these articles with a bias towards process automation, and the links to the articles should be neatly listed at the very end of the post, after everything else.'
  prompt += f'\nUse numbers for each insight to point to the relevant article URL.'
  prompt += f'\nWord the insights as if I was commeting on the article rather than just writing an extract. Each insight must be a short paragraph rather than a single sentence.'
  prompt += f'\nThe post must be written in UK English, focused on the key insights around AI and technology, and sound professional as the target audience are professionals.'
  prompt += f'\nMention that the links are in the first comment and add the links at the bottom, listed by the number of the insight they belong to.'
  prompt += f'\nFinish with a call to action asking readers to message me on LinkedIn if they are interested in discussing either the insights or how I could help them.'
  prompt += f'\nAll posts must include this at the bottom: Image source: DALL-E 3'

  post = callOpenAIChat(role, prompt)
  image = callOpenAIImage(f'Generate an image based on the following LinkedIn post: \n{post}')
  body = post + f'\n\nImage URL: {image}'
  sendEmail(subject=f'LinkedIn post from {len(articles)} articles for folder {folder_name}', body=body, urls=urls)

  # print('========================================================================================')
  # print(f'LinkedIn post for {folder_name}:')
  # print(f'Number of articles analysed: {len(articles)}\n')
  # print(post)
  # print('========================================================================================')

def sendEmail(subject, body, urls):
  """
  Set up SMTP server
  """
  smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
  smtp_server.ehlo()
  smtp_server.starttls()
  smtp_server.login(EMAIL_USERNAME, EMAIL_PASSWORD) # https://support.google.com/accounts/answer/185833

  # Send email 
  print(f'Sending email...')

  try:
    msg = f'Subject: {subject}\n\n{urls}\n\n{body}'
    smtp_server.sendmail(EMAIL_USERNAME, EMAIL_RECIPIENT, msg.encode('utf-8'))
    print('Email sent!')
    smtp_server.quit()
  except Exception as e:
    print(f'Error sending email: \n{e}')

def refreshFeedlyToken():
  refresh_token = os.getenv('FEEDLY_REFRESH_TOKEN')
  client_id = 'YOUR_CLIENT_ID'
  client_secret = 'YOUR_CLIENT_SECRET'

  url = 'https://cloud.feedly.com/v3/auth/token'
  params = {
      'refresh_token': refresh_token,
      'client_id': client_id,
      'client_secret': client_secret,
      'grant_type': 'refresh_token'
  }

  response = requests.post(url, data=params)
  access_token = response.json()['access_token']

def main(args):
  print(f'Starting process for option: {args}')
  # Get articles from last 24 hours
  yesterday = datetime.now() - timedelta(days=1)
  timestamp_ms = int(yesterday.timestamp() * 1000)

  if args == 'Create LinkedIn post':
    last48hours = datetime.now() - timedelta(days=2)
    timestamp_ms = int(last48hours.timestamp() * 1000)

  for folder_id in FEEDLY_FOLDERS_LIST:
    folder_name = 'Sustainability' if folder_id == '9bb0acab-0d68-431e-89ca-d4136dcaad5b' else 'Consultancy' if folder_id == '7fbce7bc-11dc-4bcb-986a-0116094a4c0b' else 'AI'
    print(f'Getting articles for folder: {folder_name}')
    # Get articles ids for this folder
    feedly_url = f'{FEEDLY_API_URL}/v3/streams/ids?streamId=user/{FEEDLY_USER_ID}/category/{folder_id}&newerThan={timestamp_ms}&count=20'
    response = feedly.get(feedly_url)
    
    if(response.status_code == 200):
      # print(f'Feedly response: {json.dumps(json.loads(response.text), indent=4)}')
      ids = json.loads(response.text)['ids']
      # print(f'IDs: {ids}')
      print(f'Retrieved {len(ids)} articles.')

      # Get articles from the ids
      feedly_entries_url = f'{FEEDLY_API_URL}/v3/entries/.mget'
      entries_response = feedly.post(feedly_entries_url, None, ids)
      # print(f'Entries response: {json.dumps(json.loads(entries_response.text), indent=4)}')
      articles = json.loads(entries_response.text)

      if(len(articles) > 0):
        # Concatenate articles this folder
        urls = [a['alternate'][0]['href'] for a in articles]
        titles = [a['title'] for a in articles]
        summaries = [a['summary']['content'] if 'summary' in a else '' for a in articles]
        contents = [a['fullContent'] if 'fullContent' in a else '' for a in articles]
        
        if args == 'Generate Insights':
          generateInsights(articles, folder_name=folder_name, urls=urls, titles=titles, summaries=summaries, contents=contents)
        if args == 'Create LinkedIn post':
          generateLinkedInPost(articles, folder_name=folder_name, urls=urls, titles=titles, summaries=summaries, contents=contents)
      else: 
        print('========================================================================================')
        print(f'There are no articles to analyse for folder {folder_name}.')
        print('========================================================================================') 
    else:
      print(f'Could not get articles with status code: {response.status_code}. Details: \n{response.content}')  

if __name__ == "__main__":
  if len(sys.argv) > 1:
    if sys.argv[1] == '1':
      main('Generate Insights')
    if sys.argv[1] == '2':
      main('Create LinkedIn post')
  else:
    options = ['Generate Insights', 'Create LinkedIn post']
    print("Select an option:")
    for index, option in enumerate(options):
        print(f"{index+1}) {option}")

    selection = input("Enter the number of your choice: ")
    if selection.isdigit() and 1 <= int(selection) <= len(options):
        selected_option = options[int(selection) - 1]
    
    main(selected_option)