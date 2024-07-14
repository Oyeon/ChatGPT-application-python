import sys
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='../../config/.env')

def main():
    from openai import OpenAI
    client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

    response = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    response_format={ "type": "json_object" },
    messages=[
        {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
        {"role": "user", "content": "Who won the world series in 2020?"}
    ]
    )
    print(response.choices[0].message.content)
if __name__ == "__main__":
    main()
