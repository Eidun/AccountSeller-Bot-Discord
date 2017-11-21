import discord
from discord.ext import commands
import string
import random
import json


class Trading:

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def send_embed_account(self, channel, file_data, token):
        game = file_data[token]['game']
        region = file_data[token]['region']
        price = file_data[token]['price']
        owner = file_data[token]['owner']

        embed = discord.Embed(title='Account {}'.format(token), colour=0xaf1d1d)
        embed.add_field(name='Game', value=game)
        embed.add_field(name='Region', value=region)
        embed.add_field(name='Price', value=price + '$')
        embed.add_field(name='Owner', value='<@{}>'.format(owner))
        await self.bot.send_message(channel, embed=embed)

    @commands.command(pass_context=True)
    @commands.has_role('Police')
    async def sell(self, ctx, token):
        """<token> Admin required"""
        # Getting data from json file
        with open('data/accounts.json', 'r') as f:
            file_data = json.load(f)
        if token not in file_data:
            await self.bot.say('That token does not exists')
            return
        await self.send_embed_account(ctx.message.channel, file_data, token)
        del file_data[token]
        # Saving data in json file
        with open('data/accounts.json', 'r+') as f:
            f.seek(0)
            json.dump(file_data, f, indent=4)
            f.truncate()
        await self.bot.say('Sale completed by {}!'.format(ctx.message.author.display_name))

    @commands.command(pass_context=True)
    async def accounts(self, ctx, page: int=1):
        """<page> (1 by default)"""
        # Some checks
        if page < 1:
            await self.bot.send_message(ctx.message.author, 'Enter a valid page!')
            return
        # Saving data in json file
        with open('data/accounts.json', 'r') as f:
            file_data = json.load(f)

        # Checking length
        accounts = file_data.values()
        if accounts.__len__() < page * 5 - 5:
            await self.bot.send_message(ctx.message.author, 'There are not so many account pages!')
            return

        # Show 5 elements in that page
        page_counter = 0
        max_counter = 5 * page
        for token in file_data:
            page_counter += 1
            if page_counter >= max_counter:
                break

            await self.send_embed_account(ctx.message.author, file_data, token)

    @commands.command(pass_context=True)
    async def account(self, ctx, token):
        """<token>"""
        # Getting data from json file
        with open('data/accounts.json', 'r') as f:
            file_data = json.load(f)
        if token not in file_data:
            await self.bot.say('That token does not exists')
            return

        await self.send_embed_account(ctx.message.author, file_data, token)

    @commands.command(pass_context=True)
    async def upload(self, ctx, *game):
        """<game-account>"""
        # Some checks
        if game.__len__() == 0:
            await self.bot.say('You must pass some value with this command ?upload <game-account>')
            return
        channel = ctx.message.channel
        # Collecting the game account
        game = list(game)
        game_text = ''
        for word in game:
            game_text += word + ' '
        game_text = game_text[:-1]
        # Creating the data
        token = get_token()
        data = {token: {}}

        # Get Region
        await self.bot.send_message(channel, 'What is the region of the account?')
        region = await self.bot.wait_for_message(timeout=60, author=ctx.message.author, channel=channel)
        if region is None:
            await self.bot.send_message(channel, 'You are taking a lot of time, think it better and try again!')
            return
        # Get Price
        await self.bot.send_message(channel, 'What would you like the price be?')
        price = await self.bot.wait_for_message(timeout=60, author=ctx.message.author, channel=channel)
        if price is None:
            await self.bot.send_message(channel, 'You are taking a lot of time, think it better and try again!')
            return

        # Final check
        embed = discord.Embed(title='{} Account'.format(ctx.message.author.display_name),
                              description='Check everything is correct, write y/n', color=0xaf1d1d)
        embed.add_field(name='Game', value=game_text)
        embed.add_field(name='Region', value=region.content)
        embed.add_field(name='Price', value=price.content + '$')
        await self.bot.send_message(channel, embed=embed)
        confirm = await self.bot.wait_for_message(timeout=60, author=ctx.message.author, channel=channel)
        if confirm is None or confirm.content.lower() != 'y':
            await self.bot.send_message(channel, 'Game account discarded')
            return

        # Saving data
        data[token]['game'] = game_text
        data[token]['region'] = region.content
        data[token]['price'] = price.content

        # Saving data in json file
        with open('data/accounts.json', 'r+') as f:
            file_data = json.load(f)
            file_data[token] = {}
            file_data[token]['game'] = game_text
            file_data[token]['region'] = region.content
            file_data[token]['price'] = price.content
            file_data[token]['owner'] = ctx.message.author.id
            f.seek(0)
            json.dump(file_data, f, indent=4)
            f.truncate()

        await self.bot.send_message(channel, 'Game account saved')


def get_token():
    alphabet = string.ascii_letters + string.digits
    token = ''.join(random.choice(alphabet) for i in range(8))
    return token


def setup(bot: commands.Bot):
    bot.add_cog(Trading(bot))

