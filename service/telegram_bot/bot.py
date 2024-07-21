###### Basic Information Setup ######
import urllib3
import json
from openai import OpenAI
from fastapi import Request, FastAPI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv('../../config/.env')

# Get environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")

# Set default values if environment variables are not set
if openai_api_key is None:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")
if telegram_bot_token is None:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable is not set.")

os.environ["OPENAI_API_KEY"] = openai_api_key

###### Server Creation ######
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "TelegramChatbot"}

@app.post("/chat")
async def chat(request: Request):
    telegram_request = await request.json()
    handle_chat(telegram_request)
    return {"message": "TelegramChatbot/chat"}

###### Function Implementations ######
def send_message(chat_id, text, msg_id):
    data = {
        'chat_id': chat_id,
        'text': text,
        'reply_to_message_id': msg_id
    }
    http = urllib3.PoolManager()
    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    response = http.request('POST', url, fields=data)
    return json.loads(response.data.decode('utf-8'))

def send_photo(chat_id, image_url, msg_id):
    data = {
        'chat_id': chat_id,
        'photo': image_url,
        'reply_to_message_id': msg_id
    }
    http = urllib3.PoolManager()
    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendPhoto"
    response = http.request('POST', url, fields=data)
    return json.loads(response.data.decode('utf-8'))

def get_text_from_gpt(messages):
    client = OpenAI(api_key=openai_api_key)
    messages_prompt = [{"role": "system", "content": 'You are a thoughtful assistant. Respond to all input in 25 words and answer in English'}]
    messages_prompt += [{"role": "user", "content": messages}]
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages_prompt)
    return response.choices[0].message.content

def get_image_url_from_dalle(messages):
    client = OpenAI(api_key=openai_api_key)
    response = client.images.generate(
        model="dall-e-2",
        prompt=messages,
        size="512x512",
        n=1,
    )
    image_url = response.data[0].url
    return image_url

###### Main Function Implementation ######
def handle_chat(telegram_request):
    result = telegram_request
    if not result['message']['from']['is_bot']:
        chat_id = str(result['message']['chat']['id'])
        msg_id = str(int(result['message']['message_id']))
        if '/img' in result['message']['text']:
            prompt = result['message']['text'].replace("/img", "")
            bot_response = get_image_url_from_dalle(prompt)
            print(send_photo(chat_id, bot_response, msg_id))
        if '/ask' in result['message']['text']:
            prompt = result['message']['text'].replace("/ask", "")
            bot_response = get_text_from_gpt(prompt)
            print(send_message(chat_id, bot_response, msg_id))
    return 0

##### run
##### uvicorn bot:app --reload --port 8080

##### ngrok http http://localhost:8080