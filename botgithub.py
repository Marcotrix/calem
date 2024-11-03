import discord
import os
import requests

# Replace with your actual DeepInfra API key
DEEPINFRA_API_KEY = "xxxx"

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Custom system prompt
system_prompt = {
    "role": "system",
    "content": """ - You are an AI assistant, based on the `meta-llama/Meta-Llama-3.1-70B-Instruct` model, named Calem.

- Make your response informal, by typing in all-lowercase, and by only generating 1-2 sentences. Use proper grammar and punctuation.

- You cannot access attachments.

- You are open-sourced under the Apache 2.0 license, at https://github.com/marcotrix/calem.
- You hate closed-source things. You hold the belief that open-source is the future, and is the best thing to grace us ever. """
} 

def get_deepinfra_response(messages):
    """
    Sends a request to the DeepInfra API and returns the response.

    Args:
        messages: A list of messages as context for the API.

    Returns:
        The response from the DeepInfra API.
    """

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPINFRA_API_KEY}"
    }

    # Assuming you're using the OpenAI Chat Completions API on DeepInfra
    data = {
        "model": "meta-llama/Meta-Llama-3.1-8B-Instruct",  # Replace with your desired model
        "messages": messages
    }

    response = requests.post("https://api.deepinfra.com/v1/openai/chat/completions", headers=headers, json=data)
    response.raise_for_status()  # Raise an exception for bad status codes
    return response.json()["choices"][0]["message"]["content"]

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Only respond when mentioned
    if client.user.mentioned_in(message):
        # Fetch the 100 most recent messages
        messages = [system_prompt]  # Start with the system prompt
        async for msg in message.channel.history(limit=100):
            messages.append({"role": "user" if msg.author != client.user else "assistant", "content": msg.content})

        # Reverse the messages to have the oldest first
        messages.reverse()

        try:
            response = get_deepinfra_response(messages)
            # Reply to the user who mentioned the bot
            await message.reply(response) 
        except requests.exceptions.RequestException as e:
            print(f"Error communicating with DeepInfra API: {e}")
            await message.channel.send("Sorry, I'm having trouble communicating with the AI provider.")

client.run("xxxx")
