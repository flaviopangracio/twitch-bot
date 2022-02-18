import os
from twitchio.ext import commands
from dotenv import load_dotenv
from spotify import CreatePlaylist

load_dotenv()

irc_token = os.getenv('TWITCH_TOKEN')
client_id = os.getenv('TWITCH_CLIENT_ID')

spotify = CreatePlaylist()

bot = commands.Bot(
    token=irc_token,
    client_id=client_id,
    nick="PangracioBot",
    prefix="!",
    initial_channels=['flaviopangracio'],
)


# https://twitchapps.com/tmi

@bot.event
async def event_message(ctx):
    print(ctx.author.name)
    print(ctx.content)


@bot.event()
async def event_ready():
    print(f'Logged into Twitch | {bot.nick}')


@bot.command(name='oi')
async def test_command(ctx):
    await ctx.send(
        f'''
        Opa! Seja bem vindo {ctx.author.display_name}!
        \nEu sou o PangracioBot, digite !help para saber mais sobre mim!
        '''
    )


@bot.command(name='help')
async def help_command(ctx):
    await ctx.send(
        '''
        Aqui estão algumas informações sobre mim:
        \n!oi - Mostra a mensagem de boas vindas
        \n!help - Mostra esta mensagem de ajuda
        \n!add - Adiciona uma música à playlist
        '''
    )


@bot.command(name='queue')
async def queue_command(ctx):
    await ctx.send(
        f'''
        A playlist possui {len(spotify.songs)} músicas'''
    )


@bot.command(name='add')
async def add_music_command(ctx, music_name='', author=''):
    if music_name and author:
        uri = spotify.get_spotify_uri(
            music_name, author, owner=ctx.author.display_name)

        if uri:
            spotify.add_song_to_playlist(uri)

            await ctx.send(
                f'''
                {music_name} - {author} adicionada com sucesso!
                '''
            )
        else:
            await ctx.send(
                f'''
                Não foi possível encontrar a música "{music_name} - {author}"
                '''
            )

    else:
        await ctx.send(
            '''
            Para adicionar músicas, digite !add <nome da música> <autor>
            '''
        )


@bot.command(name='skip')
async def skip_command(ctx):
    atual_uri = spotify.get_player_state()

    owner = ''

    for song in spotify.songs:
        if song['uri'] == atual_uri:
            owner = song['owner']
            break

    if owner == ctx.author.display_name:
        spotify.skip_song()
        await ctx.send(
            '''
            Pulando a música atual...
            '''
        )
    else:
        await ctx.send(
            '''
            Você só pode pular músicas que você adicionou!
            '''
        )


@bot.command(name="easter_egg")
async def easter_egg(ctx):
    await ctx.send(
        '''
        Não tem easter egg aqui!
        '''
    )


@bot.command(name="easter_egg_v")
async def easter_egg(ctx):
    await ctx.send(
        '''
        Já falei que não tem caralho!
        '''
    )


@bot.command(name="easter_egg_vv")
async def easter_egg(ctx):
    await ctx.send(
        '''
        Você é chato em mano!
        '''
    )


@bot.command(name="easter_egg_vvv")
async def easter_egg(ctx):
    await ctx.send(
        '''
        Vá caçar easter eggs na casa da sua vói!
        '''
    )


@bot.command(name="easter_egg_vvvv")
async def easter_egg(ctx):
    await ctx.send(
        '''
        ...
        '''
    )


@bot.command(name="easter_egg_vvvvv")
async def easter_egg(ctx):
    await ctx.send(
        '''
        Pede com carinho que eu solto um easter egg...
        '''
    )


@bot.command(name="easter_egg_bot_gostoso")
async def easter_egg(ctx):
    await ctx.send(
        '''
        Hmmmmmmm, me chama pra jantar primeiro, tá achando que é bagunça?
        '''
    )


@bot.command(name="easter_egg_bora_jantar")
async def easter_egg(ctx):
    await ctx.send(
        '''
        Eu não quero mais jantar!
        '''
    )


@bot.command(name="news")
async def news_command(ctx, type):
    await ctx.send(
        f'''
        Breaking News: {ctx.author.display_name}, acaba de pedir uma notícia sobre {type}!
        '''
    )

# This event thanks the user for following the bot


@bot.event
async def event_join(ctx, channel, user):
    await ctx.send(
        f'''
        Oi {user.display_name}! Seja bem vindo ao canal {channel.name}!
        '''
    )

if __name__ == '__main__':
    bot.run()
