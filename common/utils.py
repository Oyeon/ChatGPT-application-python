import yaml
from openai import OpenAI

# Load configuration from config.yaml
def load_config(config_path='config.yaml'):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

# Load prompt template from prompts.txt
def load_prompt_template(prompt_path='prompts.txt'):
    with open(prompt_path, 'r') as file:
        return file.read()

def get_gpt_response(client, prompt, model):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": prompt},
        ]
    )
    return response.choices[0].message.content


def get_gpt_image(client, prompt, model):
    response = client.images.generate(
    model=model,
    prompt=prompt,
    size="512x512",
    quality="standard",
    n=1,
    )    
    return response.data[0].url