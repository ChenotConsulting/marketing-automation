import os
from dotenv import load_dotenv
import requests
import json
from datetime import datetime, timedelta
import openai
import smtplib
import tiktoken

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
MODEL = 'gpt-3.5-turbo-0613'
MAX_TOKENS = 4092

# Setup clients
feedly = requests.Session()
feedly.headers = {'authorization': 'OAuth ' + FEEDLY_ACCESS_TOKEN}
openai.api_key = OPENAI_API_KEY

def count_tokens(text):
    enc = tiktoken.get_encoding("cl100k_base")
    token_count = enc.encode(text)
    
    return len(token_count)

def callOpenAI(prompt):
  response = openai.ChatCompletion.create(
    model=MODEL, 
    temperature=0.2,
    n=1,
    messages=[
      {'role': 'system', 'content': 'You are a research analyst writing in UK English.'}, 
      {'role': 'user', 'content': prompt}
    ]
  )
  return response['choices'][0]['message']['content']

def generateInsights(articles, folder_name, urls, titles, summaries, contents):
  """
  Generate insights from the articles
  """
  article_prompts = [f'URL: {url}\nTitle: {title}\nSummary: {summary}\nContent: {content}\n' for url, title, summary, content in zip(urls, titles, summaries, contents)]
  
  insights = ""
  current_prompt = f'Extract the key insights & trends from these {len(articles)} articles and highlight any resources worth checking. For each key insight, mention the source article:\n'
  for article_prompt in article_prompts:
    if count_tokens(current_prompt + article_prompt) > MAX_TOKENS:
      insights = callOpenAI(current_prompt, insights)
      current_prompt = article_prompt
    else:
      current_prompt += article_prompt

  # Process remaining articles
  if current_prompt:
    insights = callOpenAI(current_prompt)

  sendEmail(len(articles), folder_name, insights, urls)

  print('========================================================================================')
  print(f'Insights for folder {folder_name}:')
  print(f'Number of articles analysed: {len(articles)}\n')
  print(insights)
  print('========================================================================================')

def generateLinkedInPost(articles, folder_name, urls, titles, summaries, contents):
  """
  Generate a LinkedIn post from the articles
  """
  prompt = f'Extract insights and generate a LinkedIn post including the links to the relevant articles from these {len(articles)} articles:\n'
  for url, title, summary, content in zip(urls, titles, summaries, contents):
    prompt += f'URL: {url}\nTitle: {title}\nSummary: {summary}\nContent: {content}\n'
  prompt += f'\nYou should only talk about the insights extracted from these articles with a bias towards process automation, and there shouldn\'t be more than 2 articles linked to in the post.'
  prompt += f'\nMake sure to include the actual URL to the articles.'

  response = openai.Completion.create(
    engine='text-davinci-003', 
    prompt=prompt, 
    max_tokens=1500,
    n=1,
    temperature=0.2
  )
  post = response['choices'][0]['text']

  print('========================================================================================')
  print(f'LinkedIn post for {folder_name}:')
  print(f'Number of articles analysed: {len(articles)}\n')
  print(post)
  print('========================================================================================')

def sendEmail(articles_count, folder_name, body, urls):
  """
  Set up SMTP server
  """
  smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
  smtp_server.ehlo()
  smtp_server.starttls()
  smtp_server.login(EMAIL_USERNAME, EMAIL_PASSWORD) # https://support.google.com/accounts/answer/185833

  # Send email 
  msg = f'Subject: Feedly Insights from {articles_count} articles for folder {folder_name}\n\n{urls}\n\n{body}'
  smtp_server.sendmail(EMAIL_USERNAME, EMAIL_USERNAME, msg)
  smtp_server.quit()

def main():
  # Get articles from last 24 hours
  yesterday = datetime.now() - timedelta(days=1)
  timestamp_ms = int(yesterday.timestamp() * 1000)

  for folder_id in FEEDLY_FOLDERS_LIST:

    folder_name = 'Sustainability' if folder_id == '9bb0acab-0d68-431e-89ca-d4136dcaad5b' else 'Consultancy' if folder_id == '7fbce7bc-11dc-4bcb-986a-0116094a4c0b' else 'AI'
    # Get articles ids for this folder
    feedly_url = f'{FEEDLY_API_URL}/v3/streams/ids?streamId=user/{FEEDLY_USER_ID}/category/{folder_id}&newerThan={timestamp_ms}&count=20'
    response = feedly.get(feedly_url)
    
    # print(f'Feedly response: {json.dumps(json.loads(response.text), indent=4)}')
    ids = json.loads(response.text)['ids']
    # print(f'IDs: {ids}')

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
      
      generateInsights(articles, folder_name=folder_name, urls=urls, titles=titles, summaries=summaries, contents=contents)
      # generateLinkedInPost(articles, folder_name=folder_name, urls=urls, titles=titles, summaries=summaries, contents=contents)
    else: 
      print('========================================================================================')
      print(f'There are no articles to analyse for folder {folder_name}.')
      print('========================================================================================')   

if __name__ == "__main__":
    main()