from libs import client, macro
import asyncio
from discord.ext import commands
import random
import aiohttp


class Games(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.client = client.Client()

    @commands.command(name='coinflip', aliases=['cf', 'coin'])
    #@commands.cooldown(1, 8)
    async def coinflip(self, ctx, bet, side: str):
        assert not type(
            bet) == int, "You likely put the arguments in the wrong order! It should be something like ``p!coin 1 tails``!"
        coin = random.choice(
            [{'heads': 'https://i.imgur.com/ZobMtzv.png'}, {'tails': 'https://i.imgur.com/dBTFERz.png'}])
        temp = await self.client.get_value(ctx.message.author.id)
        current = temp[0][1]
        if str(bet).lower() == 'all':
            bet = current
        bet = int(bet)
        assert current >= bet > 0, "Too low of a bet!"
        if bet > current or side not in ('tails', 'heads'):
            return await ctx.send(embed=await macro.error(
                f"""Sorry! You either don't have enough currency \n(Your balance ``{current}`` vs your bet ``{bet}``), or you didn't enter a correct side. \n(Your side {side} vs ``tails`` or ``heads``) \nPlease re-enter your command.""",
                footer=ctx.message.author, icon=ctx.message.author.avatar_url))
        if side in coin:
            await self.client.update(bal=2 * bet + current, _id=ctx.message.author.id)
            return await ctx.send(
                embed=await macro.send(
                    f'The coin landed on {side}.\nYou won ``{2*bet}`` Cubes.\nYour balance is now ``{bet*2+current}`` Cubes. ',
                    thumb=coin[side], footer=ctx.message.author, icon=ctx.message.author.avatar_url))
        else:
            loss = current - bet
            await self.client.update(bal=loss, _id=ctx.message.author.id)
            return await ctx.send(embed=await macro.send(
                f"""The coin landed on {str(coin.keys()).replace("dict_keys(['", "").replace("'])", "")}. \nYou lost ``{bet}`` Cubes. \nYour balance is now ``{current-bet}`` Cubes.""",
                thumb=coin.get(str(coin.keys()).replace("dict_keys(['", "").replace("'])", "")),
                footer=ctx.message.author, icon=ctx.message.author.avatar_url))

    @commands.command(name='dice', aliases=['die'])
    #@commands.cooldown(1, 8)
    async def dice(self, ctx, bet, side: int):
        assert type(
            bet) == str, 'You likely put the arguments in the wrong order! It should be something like ``p!dice ' \
                         '1 4``! '
        assert side in (
            1, 2, 3, 4, 5,
            6), "You've put an invalid argument for the ``side``! Please use a number from ``1`` to ``6``."
        yes = [{'1': 'https://i.imgur.com/WgRBLTH.png'},
               {'2': 'https://i.imgur.com/0CjljSc.png'},
               {'3': 'https://i.imgur.com/IN4cNr8.png'},
               {'4': 'https://i.imgur.com/Y9ZDa6U.png'},
               {'5': 'https://i.imgur.com/3MIyz6h.png'},
               {'6': 'https://i.imgur.com/nVKKc69.png'}]
        temp = await self.client.get_value(ctx.message.author.id)
        current = temp[0][1]
        if str(bet).lower() == 'all':
            bet = current
        bet = int(bet)
        assert current >= bet > 0, "Too low of a bet!"
        if random.randint(1, 6) == side:
            await self.client.update(bal=bet * 3 + current, _id=ctx.message.author.id)
            await ctx.send(embed=await macro.send(
                f"You rolled a ``{side}``.\nYou won ``{bet*2}`` Cubes.\nYour balance is now ``{bet*3+current}`` Cubes.",
                thumb=yes[side - 1].get(f'{side}'), footer=ctx.message.author, icon=ctx.message.author.avatar_url))
            print(yes[side - 1])
        else:
            ohno = ['1', '2', '3', '4', '5', '6']
            ohno.pop(side - 1)
            false_side = random.choice(ohno)
            await self.client.update(bal=current - bet, _id=ctx.message.author.id)
            await ctx.send(embed=await macro.send(
                f"You rolled a {false_side}.\nYou lost ``{bet}`` Cubes.\nYour balance is now ``{current-bet}`` Cubes.",
                thumb=yes[int(false_side) - 1].get(false_side), footer=ctx.message.author,
                icon=ctx.message.author.avatar_url))
            print(yes[int(false_side) - 1])

    @commands.command(name='roulette')
    #@commands.cooldown(1, 8)
    async def roulette(self, ctx, bet):
        temp = await self.client.get_value(ctx.message.author.id)
        current = temp[0][1]
        if bet == 'all':
            bet = current
        bet = int(bet)
        assert 0 < bet <= current, "You don't have a large enough balance for this. >:c"
        if random.randint(1, 4) == 1:  # this means that the player has fucking shot themselves oh god oh fuck
            await self.client.update(current - bet, _id=ctx.message.author.id)
            if random.randint(1, 50) == 50:
                yes = "You pulled the trigger and... DIED! You DIED dude!! DUDE??! You're DEAD!!!"
            else:
                yes = "You pulled the trigger and... died! :skull:"
            await ctx.send(
                embed=await macro.send(f"{yes}\nYou lost ``{bet}`` Cubes!\nYour balance is now ``{current-bet}`` Cubes",
                                       footer=ctx.message.author,
                                       icon=ctx.message.author.avatar_url,
                                       thumb='https://i.imgur.com/iuGfSe5.png'
                                       ))
        else:
            await self.client.update(int(current + int(bet * 1.25)), _id=ctx.message.author.id)
            await ctx.send(embed=await macro.send(
                f"You pulled the trigger and... lived! :angel:\nYou won ``{int(bet*1.25)}`` Cubes\nYour balance is now ``{current+int(bet*1.25)}`` Cubes",
                footer=ctx.message.author,
                icon=ctx.message.author.avatar_url,
                thumb='https://i.imgur.com/QGlZINT.png'
            ))

    @commands.command(name='slots')
    #@commands.cooldown(1, 8)
    async def slots(self, ctx, bet):
        temp = await self.client.get_value(ctx.message.author.id)
        current = temp[0][1]
        if bet == 'all':
            bet = current
        bet = int(bet)
        assert 0 < bet <= current, "You don't have a large enough balance for this. >:c"
        slots = ['chocolate_bar', 'bell', 'tangerine', 'apple', 'cherries', 'seven']
        slot1 = slots[random.randint(0, 5)]
        slot2 = slots[random.randint(0, 5)]
        slot3 = slots[random.randint(0, 5)]
        msg = await ctx.send(embed=await macro.send('Rolling...'))
        await asyncio.sleep(2.5)
        if slot1 == slot2 and slot2 == slot3 and slot3 != 'seven':
            await self.client.update(bal=2 * bet + current, _id=ctx.message.author.id)
            await msg.edit(embed=await macro.send(
                f"|:{slot1}:|:{slot2}:|:{slot3}:|\nGood! You won ``{bet*2}`` Cubes!\nYour balance is now ``{bet*2+current}`` Cubes",
                footer=ctx.message.author,
                icon=ctx.message.author.avatar_url,
                thumb='https://i.imgur.com/bQZDghw.png'
            ))
        elif slot1 == 'seven' and slot2 == 'seven' and slot3 == 'seven':
            await self.client.update(bal=int(5 * bet + current), _id=ctx.message.author.id)
            await msg.edit(embed=await macro.send(
                f"|:{slot1}:|:{slot2}:|:{slot3}:|\nJACKPOT!! You won ``{bet*5}`` Cubes!\nYour balance is now ``{bet*5+current}`` Cubes",
                footer=ctx.message.author,
                icon=ctx.message.author.avatar_url,
                thumb='https://i.imgur.com/bQZDghw.png'
            ))
        elif slot1 == slot2 or slot1 == slot3 or slot2 == slot3:
            await self.client.update(bal=int(3 * bet + current), _id=ctx.message.author.id)
            await msg.edit(embed=await macro.send(
                f"|:{slot1}:|:{slot2}:|:{slot3}:|\nGreat! You won ``{bet*3}`` Cubes!\nYour balance is now ``{bet*3+current}`` Cubes",
                footer=ctx.message.author,
                icon=ctx.message.author.avatar_url,
                thumb='https://i.imgur.com/bQZDghw.png'
            ))

        else:
            await self.client.update(bal=current - bet, _id=ctx.message.author.id)
            await msg.edit(embed=await macro.send(
                f"|:{slot1}:|:{slot2}:|:{slot3}:|\nOh no... You lost ``{bet}`` Cubes!\nYour balance is now ``{current-bet}`` Cubes",
                footer=ctx.message.author,
                icon=ctx.message.author.avatar_url,
                thumb='https://i.imgur.com/bQZDghw.png'
            ))

    @commands.command(name='beg')
    @commands.cooldown(1, 120)
    async def beg(self, ctx):
        temp = await self.client.get_value(ctx.message.author.id)
        current = temp[0][1]
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://uinames.com/api/?ext&region=canada") as re:
                res = await re.json()
                if random.randint(1, 5) == 1:
                    loss = random.randint(1, 10)
                    if loss > current:
                        loss = current
                    await self.client.update(bal=current - loss, _id=ctx.message.author.id)
                    await ctx.send(embed=await macro.send(
                        f"{res['name']} {res['surname']} has stolen ``{loss}`` Cubes from you!\nYour balance is now ``{current-loss}`` Cubes.",
                        footer=f"{ctx.message.author} Thanks to uinames.com for the name & picture API!",
                        icon=ctx.message.author.avatar_url,
                        thumb=res['photo'],
                        title=":scream: FAILURE :scream:"))
                else:
                    earnings = random.randint(1, 15)
                    await self.client.update(bal=current + earnings, _id=ctx.message.author.id)
                    await ctx.send(embed=await macro.send(
                        f"{res['name']} {res['surname']} has given ``{earnings}`` Cubes to you!\nYour balance is now ``{current+earnings}`` Cubes.",
                        footer=f"{ctx.message.author} Thanks to uinames.com for the name & picture API!",
                        icon=ctx.message.author.avatar_url,
                        thumb=res['photo'],
                        title=':four_leaf_clover: SUCCESS :four_leaf_clover:'))

    @commands.command(name='crime')
    @commands.cooldown(2, 300)
    async def crime(self, ctx, bet):
        temp = await self.client.get_value(ctx.message.author.id)
        current = temp[0][1]
        if bet == 'all':
            bet = current
        bet = int(bet)
        assert bet > 8, "You can't have a target amount 8 or below."
        assert bet <= 10000
        assert current + bet != 0, "Your target amount is too high."
        if bet > current:
            bet = current
        if random.randint(1, bet // 2) == 1:
            await self.client.update(bal=current + bet * 3, _id=ctx.message.author.id)
            await ctx.send(embed=await macro.send(
                f"You got away with stealing ``{random.randint(1,1000)}`` items of \n``{random.choice(('jewelry','video games','gold','coochie'))}`` which is worth ``{bet*3}`` Cubes!\n Your balance is now ``{current+bet}`` Cubes!",
                thumb='https://www.freepngimg.com/thumb/minecraft/11-2-minecraft-diamond-png.png',
                icon=ctx.message.author.avatar_url,
                footer=f"{ctx.message.author} Your chances of winning were {round(100/bet, 2)}%!"))
        else:
            await self.client.update(bal=current - bet, _id=ctx.message.author.id)
            await ctx.send(embed=await macro.send(
                f"You didn't get away with stealing. Ironically, the bail posting is ``{bet}`` Cubes.\n Your balance is now ``{current-bet}`` Cubes.",
                thumb='http://www.blocksandgold.com//media/catalog/product/cache/3/image/200x/6cffa5908a86143a54dc6ad9b8a7c38e/a/r/arbuste_mort_1.png',
                icon=ctx.message.author.avatar_url,
                footer=f"{ctx.message.author} Your chances of winning were {round(100/bet, 2)}%!"))


def setup(bot: commands.Bot):
    bot.add_cog(Games(bot))
