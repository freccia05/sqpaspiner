import discord
from discord.ext import commands
import os
import random
import json

def load_data():
    with open("data.json", "r") as f:
        return json.load(f)
    
def save_data(data):
    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)


TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

def pick_random_name(remaining_names):
    if not remaining_names:
        return None
    return random.choice(remaining_names)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("Your Coordinates are 40.376188, -80.623031")


@bot.command()
async def addname(ctx, *, name):
    data = load_data()
    if name in data["names"]:
        await ctx.send(f"{name} is already in the list.")
        return
    data["names"].append(name)
    data["namesleft"].append(name)
    save_data(data)
    await ctx.send(f"Added {name} to the list.")

@bot.command()
async def pickName(ctx):
    data = load_data()
    if not data["namesleft"]:
        data["namesleft"] = data["names"].copy()
    name = pick_random_name(data["namesleft"])
    data["namesleft"].remove(name)
    save_data(data)
    await ctx.send(f"Congrats! {name} has been picked to complete the merge request!")


@bot.command()
async def resetNames(ctx):
    data = load_data()
    data["namesleft"] = data["names"].copy()
    save_data(data)
    await ctx.send("The list of names has been reset.")

@bot.command()
async def spqahelp(ctx):
    help_message = """
    **Available Commands:**
    `!ping` - get doxxed
    `!addname <name>` - Add a name to the list.
    `!pickName` - Pick a random name from the list.
    `!resetNames` - Reset the list of names.
    `!help` - help
    """
    await ctx.send(help_message)
bot.run(TOKEN)
