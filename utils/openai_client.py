from openai import OpenAI

client = None


def get_client(api_key):
    global client

    if client is None:
        client = OpenAI(api_key=api_key)

    return client


def stream_chat(messages, api_key):
    client = get_client(api_key)

    return client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        stream=True,
    )