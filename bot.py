import sys
import traceback
import discord
from discord.ext import commands


description = '''Unknown-Bot ready for your trades here.'''

modules = {'cogs.trading', }

bot = commands.Bot(command_prefix='?', description=description)


@bot.event
async def on_ready():
    print('Unknown-Bot starting...')
    print(bot.user.name)
    print(bot.user.id)

    print('Working in {} servers'.format(len(bot.servers)))
    await bot.change_presence(game=discord.Game(name='trading'))
    print('Loading cogs...')
    if __name__ == '__main__':
        modules_loaded = 0
        for module in modules:
            try:
                bot.load_extension(module)
                print('\t' + module)
                modules_loaded += 1
            except Exception as e:
                traceback.print_exc()
                print(f'Error loading the extension {module}', file=sys.stderr)
        print(str(modules_loaded) + '/' + str(modules.__len__()) + ' modules loaded')
        print('Systems 100%')
    print('------')


# Bot run
bot_token = input('Enter your bot token: ')
bot.run(bot_token)
