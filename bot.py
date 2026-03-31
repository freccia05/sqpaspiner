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
intents.members = True

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
    await ctx.send("bruh")


@bot.command()
async def pickName(ctx):
    data = load_data()
    if not data["namesleft"]:
        data["namesleft"] = data["names"].copy()
    name = pick_random_name(data["namesleft"])
    data["namesleft"].remove(name)
    save_data(data)

    usermention = ctx.guild.get_member(name)
    await ctx.send(f"Congrats! {usermention.mention} has been picked to complete the merge request!")

@bot.command()
async def remainingNames(ctx):
    data = load_data()
    mentions = []

    for name_id in data["namesleft"]:
        member = ctx.guild.get_member(name_id)
        if member is not None:
            mentions.append(member.name)
        else:
            mentions.append(f"`{name_id}` (not in server)")

    await ctx.send("Remaining members:\n" + "\n".join(mentions))

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
    `!pickName` - Pick a random name from the list.
    `!resetNames` - Reset the list of names.
    `!remainingNames` - Show the remaining names.
    `!spqahelp` - Show this help message.
    `!addall` - Add all members of the server to the list (excluding bots and the bot itself).
    """
    await ctx.send(help_message)



@bot.command()
async def addall(ctx):
    data = load_data()

    existing = set(data["names"])
    added = 0

    for member in ctx.guild.members:
        if member.bot:
            continue
        if member.id == 913527606954053673:
            continue
        if member.id not in existing:
            data["names"].append(member.id)
            data["namesleft"].append(member.id)
            added += 1

    save_data(data)
    await ctx.send(f"Added {added} members from this server.")


bot.run(TOKEN)
