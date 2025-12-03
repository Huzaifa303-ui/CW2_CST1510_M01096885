
import os
import dotenv  
from openai import OpenAI


dotenv.load_dotenv() # Load variables from .env
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

completion = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello! What is AI?"}
    ]
)

print(completion.choices[0].message.content)
