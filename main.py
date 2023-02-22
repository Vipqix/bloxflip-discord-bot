from discord import app_commands
import discord
import json
import cloudscraper
import random

requests = cloudscraper.create_scraper()

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

            with open("database.json", "r") as ff:
                tokenss = json.load(ff)
            tokenss[str(interaction.user.id)] = auth
            with open("database.json", "w") as ff:
                json.dump(tokenss, ff)
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
        await interaction.response.send_message(embed=discord.Embed(title="Error!", description="You have not linked your token yet, use `/link` to link your account :)"), ephemeral=True)

@tree.command(name='privuser', description='gives info about a user')
async def privuser(interaction: discord.Interaction):
    if str(interaction.user.id) not in tokens:
        await interaction.response.send_message(embed=discord.Embed(title="Error!", description="You have not linked your token yet, use `/link` to link your account :)"), ephemeral=True)
        return

    await interaction.response.send_message(embed=discord.Embed(title="Getting user info...", description="Please wait while we get your info...", color=0xffff00), ephemeral=True)
    aheader = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
        'x-auth-token': json.load(open("database.json", "r"))[str(interaction.user.id)]
    }
    request = requests.get(url="https://api.bloxflip.com/user", headers=aheader).json()
    await interaction.edit_original_response(content='', embed=discord.Embed(title="User info", description=f"```json\n{json.dumps(request, indent=4)}```", color=0x1aff00))

@tree.command(name='pubuser', description='gives info about a user')
async def pubuser(interaction: discord.Interaction):
    if str(interaction.user.id) not in tokens:
        await interaction.response.send_message(embed=discord.Embed(title="Error!", description="You have not linked your token yet, use `/link` to link your account :)"), ephemeral=True)
        return

    await interaction.response.send_message(embed=discord.Embed(title="Getting user info...", description="Please wait while we get your info...", color=0xffff00), ephemeral=False)
    aheader = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
        'x-auth-token': json.load(open("database.json", "r"))[str(interaction.user.id)]
    }
    request = requests.get(url="https://api.bloxflip.com/user", headers=aheader).json()['user']
    embed = discord.Embed(title=f"User info from {interaction.user}", color=0x1aff00)
    embed.add_field(name="Roblox ID", value=request['robloxId'])
    embed.add_field(name="Roblox Username", value=request["robloxUsername"])
    embed.add_field(name="Wallet", value=request['wallet'])
    await interaction.edit_original_response(content='', embed=embed)

@tree.command(name='autotowers', description='plays a towers game for you')
async def autotowers(interaction: discord.Interaction, bet_amount: int, difficulty: str, clicks: int):

    if str(interaction.user.id) not in tokens:
        await interaction.response.send_message(embed=discord.Embed(title="Error!", description="You have not linked your token yet, use `/link` to link your account :)"), ephemeral=True)
        return

    if bet_amount < 5:
        await interaction.response.send_message(embed=discord.Embed(title="Error!", description="Bet amount must be greater than 5", color=0xff0000), ephemeral=True)
        return

    if difficulty.lower() not in ['easy', 'medium', 'hard']:
        await interaction.response.send_message(embed=discord.Embed(title="Error!", description="Your difficulty is not [easy, normal, hard].", color=0xff0000), ephemeral=True)
        return

    if clicks < 1:
        await interaction.response.send_message(embed=discord.Embed(title="Error!", description="You must click at least once.", color=0xff0000), ephemeral=True)
        return

    await interaction.response.send_message(embed=discord.Embed(title="Starting...", description="We're starting a game for you, good luck.", color=0xffff00))

    aheader = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
        'x-auth-token': json.load(open("database.json", "r"))[str(interaction.user.id)]
    }
    savedwallet = requests.get(url="https://api.bloxflip.com/user", headers=aheader).json()['user']['wallet']
    try:
        """ creates a game """
        requests.post(url="https://api.bloxflip.com/games/towers/create", headers=aheader, json={"difficulty":difficulty,"betAmount":bet_amount}).json()

        """" makes clicks """
        towers_stage = 0
        await interaction.edit_original_response(content='', embed=discord.Embed(title="Clicking...", color=0xffff00))
        for i in range(clicks):
            play_request = requests.post(url="https://api.bloxflip.com/games/towers/action", headers=aheader,
                                         json={"cashout": False, "tile": random.randint(0, 2), "towerLevel": towers_stage}).json()
            if play_request['exploded']:
                embed = discord.Embed(title="Game ended!", description=f"Game ended, you lost.", color=0xff0000)
                wallet = requests.get(url="https://api.bloxflip.com/user", headers=aheader).json()['user']['wallet']
                embed.add_field(name='balance:', value=f'```{wallet}```')
                embed.add_field(name='loss:', value=f'```{savedwallet - wallet}```')
                await interaction.edit_original_response(content='', embed=embed)
                return
            if towers_stage == 7:
                break

        """ tells you if the game is over """
        requests.post(url="https://api.bloxflip.com/games/towers/action", headers=aheader, json={"cashout": True}).json()
        embed = discord.Embed(title="Game ended!", description=f"Game ended, you won.", color=0x1aff00)
        wallet = requests.get(url="https://api.bloxflip.com/user", headers=aheader).json()['user']['wallet']
        embed.add_field(name='balance:', value=f'```{wallet}```')
        embed.add_field(name='profit:', value=f'```{wallet - savedwallet}```')
        await interaction.edit_original_response(content='', embed=embed)


    except Exception as e:
        await interaction.edit_original_response(content='', embed=discord.Embed(title="Error", description=f"Token invalid!, or this error : {e}", color=0xff0000))


client.run(open("run", 'r').read())
