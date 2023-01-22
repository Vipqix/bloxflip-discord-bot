import discord
import json
import requests
from discord import app_commands


class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents = discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
        print(f"logged in as {self.user}.")

client = aclient()
tree = app_commands.CommandTree(client)

headersnoauth = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

with open("database.json", "r") as f:
    tokens = json.load(f)

@tree.command(name='link', description='link your bloxflip account to your discord account')
async def link(interaction: discord.Interaction, auth: str):

    await interaction.response.send_message(embed=discord.Embed(title="Linking...", description="Please wait while we link your account...", color=0xffff00), ephemeral=True)

    aheader = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
        'x-auth-token': auth
    }

    r = requests.get(url="https://api.bloxflip.com/user", headers=aheader).json()
    try:
        if r['success']:

            await interaction.edit_original_response(content='', embed=discord.Embed(title='Linked!', description="you've linked your bloxflip account to our system and can now use the bot", color=0x1aff00))

            with open("database.json", "r") as f:
                tokens = json.load(f)
            tokens[str(interaction.user.id)] = auth
            with open("database.json", "w") as f:
                json.dump(tokens, f)
        else:
            await interaction.edit_original_response(content='', embed=discord.Embed(title='Error!', description="Not a valid token.", color=0xff0000))

    except Exception as e:
        await interaction.edit_original_response(content='', embed=discord.Embed(title="Error", description=f"Token invalid!, or this error : {e}", color=0xff0000))

@tree.command(name='see_auth', description='gives your bloxflip auth')
async def sendquote(interaction: discord.Interaction):

    try:
        auth = tokens[str(interaction.user.id)]
        await interaction.response.send_message(embed=discord.Embed(title="Your auth", description=f"```{auth}```", color=0x1aff00), ephemeral=True)
    except KeyError:
        await interaction.response.send_message("You have not linked your auth!")
        

client.run(open("run", "r").read())
