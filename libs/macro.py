import discord


class Macro:
    """the BEST macro class :D"""

    @staticmethod
    async def msg(desc=None, title=None, color: discord.Color = discord.Color.blurple(), thumb: str = None,
                  footer: str = None, icon: str = None):
        embed = discord.Embed(
            type='rich',
            description=desc,
            title=title,
            color=color
        )
        if not thumb:
            return embed
        embed.set_thumbnail(url=thumb)
        if not footer and not icon:
            return embed
        embed.set_footer(text=footer, icon_url=icon)
        return embed

    @classmethod
    async def img(cls, image: str, desc: str = None, title: str = None):
        message = await cls.msg(desc=desc, title=title)
        message.set_image(url=image)
        return message

    @classmethod
    async def error(cls, desc: object = None, title: object = None, footer: str = None, icon: str = None) -> object:
        """

        :rtype: object
        """
        return await cls.msg(desc=desc, title=title,
                             color=discord.Color.red())


err, error = Macro.error, Macro.error
send, msg = Macro.msg, Macro.msg
img, pic = Macro.img, Macro.img
