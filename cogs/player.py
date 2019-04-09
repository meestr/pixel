from libs import macro, client
from discord.ext import commands
import discord


class Player(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.client = client.Client()
        self.bot = bot

    @commands.command(name='create')
    @commands.cooldown(1, 2.5)
    async def create(self, ctx):
        assert not len(await self.client.get_value(ctx.message.author.id)), "You've already created an account. :c"
        await self.client.create_value(ctx.message.author.id)
        return await ctx.send(embed=await macro.send(
            "Congrats! You've successfully created an account! Your starting balance is ``0`` Cubes."))

    @commands.command(name='bal', aliases=['b', 'balance'])
    @commands.cooldown(1, 2.5)
    async def balance(self, ctx, member: discord.Member = False):
        if not member:
            member = ctx.message.author
        bal = await self.client.get_value(member.id)
        balance = bal[0][1]
        await ctx.send(embed=await macro.send(desc=f"** {member.mention} has a balance of {balance} Cubes.**",
                                              thumb='https://i.imgur.com/QXuy2wP.png', footer=ctx.message.author,
                                              icon=ctx.message.author.avatar_url))

    @commands.command(name='help')
    @commands.cooldown(1, 2.5)
    async def help(self, ctx):
        embed = discord.Embed(color=discord.Color.blurple(), type='rich', title='HELP',
                              description="Hey there! To create an account, please use the command p!create.")
        embed.add_field(name='Utilities', value='``create``, ``bal``, ``help``', inline=True)
        embed.add_field(name='Games', value='``coin``, ``dice``, ``roulette``, ``crime``, ``beg``, ''``slots``', inline=True)
        embed.add_field(name='Meme',
                        value='``threat``, ``clyde``, ``trump``, ``jpeg``, ``changemymind``, ``whowouldwin``, ``phcomment``', inline=True)
        embed.add_field(name='NSFW', value="``hentai``, ``4k``, ``gif``, ``gonewild``, ``ass``", inline=True)
        await ctx.send(embed=embed)

    @commands.command(name='daily')
    @commands.cooldown(1, 60 * 60 * 24)
    async def daily(self, ctx):
        try:
            b = await self.client.get_value(ctx.message.author.id)
            bal = b[0][1]
            await self.client.update(bal=200 + bal, _id=ctx.message.author.id)
            return await ctx.send(
                embed=await macro.send(f"Here's your daily ``{200}`` Cubes! Come back in 24 hours for more."))
        except commands.errors.CommandOnCooldown:
            await ctx.send("You're doing that too much. Come back in 24 hours.")
    @commands.command(name='invite')
    async def inv(self, ctx):
        await ctx.send(embed=await macro.send("Check your DMs!"))
        await ctx.message.author.send(embed=await macro.send(f"Hi!\nThanks for taking an interest in me. \n The support server is here: https://discord.gg/zdUSNVM\n and the link to invite me is here: https://discordapp.com/api/oauth2/authorize?client_id=560695413406171156&permissions=0&scope=bot"))


def setup(bot: commands.Bot):
    bot.add_cog(Player(bot=bot))
