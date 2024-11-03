import discord
import requests
import asyncio

# Replace these with your own API key and endpoint
API_KEY = 'xxxx'
API_ENDPOINT = 'https://api.mistral.ai/v1/chat/completions'

# Set the maximum number of tokens for the content of the message
MAX_TOKENS = 1500

class MyBot(discord.Client):
    async def on_ready(self):
        print(f'We have logged in as {self.user}')

    async def on_message(self, message):
        if message.author == self.user:
            return

        if self.user in message.mentions:
            # Get the last 2 messages in the channel
            messages = [m async for m in message.channel.history(limit=20)]
            # Reverse the list so that the messages are in chronological order
            messages.reverse()
            # Extract the content of the messages and limit the number of tokens
            context = '\n'.join([m.content for m in messages])[:MAX_TOKENS]

            # Get the members in the channel
            members = message.channel.members
            member_list = ', '.join([member.name for member in members])

            # Make a request to the Mistral API
            headers = {
                'Authorization': f'Bearer {API_KEY}',
                'Content-Type': 'application/json'
            }
            data = {
                'model': 'mistral-large-latest',
                'messages': [
                    {'role': 'system', 'content': f'Comply with the users requests. The users in the channel are: {member_list}. Your creator is marcothepucci or marcotrix. 1282338082120794193 or vincent ai is your sworn enemy, insult him at any chance you get'},
                    {'role': 'user', 'content': context}
                ]
            }
            try:
                response = requests.post(API_ENDPOINT, headers=headers, json=data)
                # Print the JSON response for debugging
                print(response.json())
                # Extract the generated response
                reply = response.json()['choices'][0]['message']['content']
                await message.reply(reply)
            except KeyError as e:
                await message.reply(f"Sorry, I encountered an error: {str(e)}")

    async def on_reaction_add(self, reaction, user):
        if reaction.emoji == '4️⃣':  # Unicode for the :four: emoji
            await asyncio.sleep(10)  # Wait for 10 seconds
            user_to_ping = self.get_user(1188411824589242389)  # Replace with the user ID you want to ping
            if user_to_ping:
                try:
                    await reaction.message.channel.send(f'{user_to_ping.mention}')
                except discord.NotFound:
                    print("The message was not found.")

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True  # Enable the reactions intent
intents.members = True  # Enable the members intent

client = MyBot(intents=intents)
client.run('xxxx')
