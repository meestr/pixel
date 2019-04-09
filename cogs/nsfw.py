# keep out children

import discord
from discord.ext import commands
from libs import macro
import aiohttp


class NSFW(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='hentai')
    async def hentai(self, ctx):
        if ctx.message.channel.is_nsfw:
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://nekobot.xyz/api/image?typehentai") as res:
                    res = await res.json()
                    await ctx.send(embed=await macro.img(res['message']))
        else:
            await ctx.send(embed=await macro.error(f"You must use this command in an NSFW channel."))

    @commands.command(name='4k')
    async def fourk(self, ctx):
        if ctx.message.channel.is_nsfw:
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://nekobot.xyz/api/image?type=4k") as res:
                    res = await res.json()
                    await ctx.send(embed=await macro.img(res['message']))
        else:
            await ctx.send(embed=await macro.error(f"You must use this command in an NSFW channel."))

    @commands.command(name='gif')
    async def gif(self, ctx):
        if ctx.message.channel.is_nsfw:
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://nekobot.xyz/api/image?type=pgif") as res:
                    res = await res.json()
                    await ctx.send(embed=await macro.img(res['message']))
        else:
            await ctx.send(embed=await macro.error(f"You must use this command in an NSFW channel."))

    @commands.command(name='ass')
    async def ass(self, ctx):
        if ctx.message.channel.is_nsfw:
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://nekobot.xyz/api/image?type=ass") as res:
                    res = await res.json()
                    await ctx.send(embed=await macro.img(res['message']))
        else:
            await ctx.send(embed=await macro.error(f"You must use this command in an NSFW channel."))

    @commands.command(name='gonewild')
    async def hentai(self, ctx):
        if ctx.message.channel.is_nsfw:
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://nekobot.xyz/api/image?type=gonewild") as res:
                    res = await res.json()
                    await ctx.send(embed=await macro.img(res['message']))
        else:
            await ctx.send(embed=await macro.error(f"You must use this command in an NSFW channel."))


def setup(bot: commands.Bot):
    bot.add_cog(NSFW(bot))
