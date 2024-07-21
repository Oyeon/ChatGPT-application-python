from openai import OpenAI
import os
from dotenv import load_dotenv
from common.utils import load_config, load_prompt_template, get_gpt_response
from jinja2 import Environment, FileSystemLoader

# Load configuration and prompt template
config = load_config()
prompt_template = load_prompt_template()

load_dotenv('../../config/.env')
openai_api_key = os.getenv("OPENAI_API_KEY")

# Set default values if environment variables are not set
if openai_api_key is None:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

os.environ["OPENAI_API_KEY"] = openai_api_key

def get_gpt_response(client, prompt, model):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": prompt},
        ]
    )
    return response.choices[0].message.content

def main():
    blog_title = "soccer history"
    client = OpenAI(api_key=openai_api_key)
    prompt = prompt_template.format(topic="soccer") # ex..
    response = get_gpt_response(client, prompt, config['openai_model'])

    # 템플릿 디렉토리 설정
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('template.html')
    output = template.render(title=blog_title, content=response)

    with open('blog_post.html', 'w') as file:
        file.write(output)

if __name__ == "__main__":
    main()