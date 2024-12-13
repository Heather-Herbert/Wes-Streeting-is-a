from dotenv import load_dotenv
import os
from atproto import Client, client_utils
from openai import OpenAI

client = OpenAI(api_key=OPENAI_API_KEY)

load_dotenv()

# Configuration from .env
BLUESKY_HANDLE = os.getenv('BLUESKY_HANDLE')
APP_PASSWORD = os.getenv('APP_PASSWORD')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def main():
    client = Client()
    profile = client.login(BLUESKY_HANDLE, APP_PASSWORD)

    # Set up OpenAI API credentials

    # Get the insult from OpenAI
    response = client.completions.create(engine="text-davinci-003",  # Or a different model
    prompt="Finish the sentence 'Wes Streeting is a ' with an insult (but keep it lighthearted and not overly offensive).",
    max_tokens=50,
    n=1,
    stop=None,
    temperature=0.7)

    insult = response.choices[0].text.strip()

    # Check if the text is already in the insult
    if "Wes Streeting is a" not in insult:
        # If not, prepend the text to the start of the insult
        insult = "Wes Streeting is a " + insult

    text = client_utils.TextBuilder().text(insult)
    post = client.send_post(text)
    client.like(post.uri, post.cid)

if __name__ == '__main__':
    main()