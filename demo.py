import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.environ.get("OPENAI_API_KEY")

response = openai.Image.create(
    prompt="An italian man eating mooncake, and shows thumbs up",
    n=1,
    size="512x512",
)

print(response['data'][0]['url'])