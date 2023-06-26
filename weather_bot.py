import discord
import requests

intents = discord.Intents.all()
client = discord.Client(intents=intents)
intents.typing = False
intents.presences = False
intents.messages = True

bot = discord.Client(intents=intents)
prefix = '!'

@bot.event
async def on_ready():
    print(f'Bot is ready! Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    print('Message content:', message.content)
    print('Message author:', message.author)

    if message.author == bot.user:
        return

    if message.content.startswith(prefix):
        command = message.content[len(prefix):].lower()

        if command.startswith('weather'):
            location = command[len('weather'):].strip()

            if not location:
                await message.channel.send('Please provide a location.')
                return

            try:
                weather_data = fetch_weather_data(location)
                await message.channel.send(f"The weather in {location} is {weather_data['weather']} with {weather_data['temperature']}\N{DEGREE SIGN}C")
            except Exception as e:
                print(e)
                await message.channel.send('An error occurred while fetching the weather.')

def fetch_weather_data(location):
    api_key = 'YOUR_WEATHER_API'
    api_url = f'https://api.weatherapi.com/v1/current.json?key={api_key}&q={location}'

    response = requests.get(api_url)
    data = response.json()

    if response.status_code != 200 or 'error' in data:
        raise Exception('Invalid location or error in weather API response.')

    return {
       'weather': data['current']['condition']['text'],
        'temperature': data['current']['temp_c'],
    }

bot.run('YOUR_BOT_TOKEN')
