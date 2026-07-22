from openai import OpenAI

client = None


def get_client(api_key):
    global client

    if client is None:
        client = OpenAI(api_key=api_key)

    return client



def stream_chat(messages, api_key, model):
    """
    Send the messages to OpenAI and return the streaming response.
    """

    client = get_client(api_key)

    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True,
    )

    return stream