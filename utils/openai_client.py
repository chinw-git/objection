from openai import OpenAI

client = None


def get_client(api_key):
    global client

    if client is None:
        client = OpenAI(api_key=api_key)

    return client


def chat_completion(
    messages,
    api_key,
    model,
    temperature
):
    """
    Send the conversation to OpenAI and
    return the assistant response as text.
    """

    client = get_client(api_key)

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        response_format={"type": "json_object"}
    )

    print("========== OpenAI Response ==========")
    print(response)
    print("=====================================")

    return response.choices[0].message.content