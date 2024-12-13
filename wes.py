from dotenv import load_dotenv
import os
from atproto import Client, client_utils
from openai import OpenAI

load_dotenv()

# Configuration from .env
BLUESKY_HANDLE = os.getenv('BLUESKY_HANDLE')
APP_PASSWORD = os.getenv('APP_PASSWORD')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Initialize OpenAI client
openai_client = OpenAI(api_key=OPENAI_API_KEY)

def main():
    # Bluesky client
    bluesky_client = Client()
    profile = bluesky_client.login(BLUESKY_HANDLE, APP_PASSWORD)

    # Get the insult from OpenAI
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",  # Updated model
        messages=[
            {"role": "system", "content": "You are a witty assistant."},
            {"role": "user", "content": "Finish the sentence 'Wes Streeting is a ' with an insult (but keep it lighthearted and not overly offensive)."}
        ],
        max_tokens=50,
        temperature=0.7
    )

    # Extract the insult from the response
    insult = response.choices[0].message.content.strip()

    # Check if the text is already in the insult
    if "Wes Streeting is a" not in insult:
        # If not, prepend the text to the start of the insult
        insult = "Wes Streeting is a " + insult

    # Send post to Bluesky
    text = client_utils.TextBuilder().text(insult)
    post = bluesky_client.send_post(text)
    bluesky_client.like(post.uri, post.cid)

if __name__ == '__main__':
    main()