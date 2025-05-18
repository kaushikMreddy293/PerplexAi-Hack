import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

client = OpenAI(api_key=PERPLEXITY_API_KEY, base_url="https://api.perplexity.ai")

def get_perplexity_response(user_query: str):
    messages = [
        {
            "role": "system",
            "content": (
                "You are an artificial intelligence assistant and you need to "
                "engage in a helpful, detailed, polite conversation with a user."
            ),
        },
        {
            "role": "user",
            "content": user_query,
        },
    ]

    response = client.chat.completions.create(
        model="sonar-pro",
        messages=messages,
    )

    reply = response.choices[0].message.content

    citations = []
    try:
        if hasattr(response.choices[0], 'citations'):
            citations = response.choices[0].citations
        elif hasattr(response, 'citations'):
            citations = response.citations
        elif hasattr(response.choices[0].message, 'citations'):
            citations = response.choices[0].message.citations
        elif "citations" in response.model_dump():
            citations = response.model_dump().get("citations", [])
    except:
        pass

    return {
        "response": reply,
        "citations": citations
    }

