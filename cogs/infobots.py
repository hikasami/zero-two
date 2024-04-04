import disnake
from disnake.ext import commands
from random import randint, random




class infobots(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name= "bot", description="Информация о Zero Two")
    async def bot(self, ctx):
        info=disnake.Embed(title = "Информация о боте", color=0x2f3136)
        info.add_field(name = "Разработчик:", value = "<:icons_text1:1223137135335575695> `python_maksim_dev`")
        info.add_field(name = "Моя библиотека:", value="<:icons_text1:1223137135335575695> Disnake", inline=False)
        info.add_field(name = "Моя версия:", value = "<:icons_text1:1223137135335575695> `v4.0.2`", inline=False)
        info.add_field(name = "Кол-во команд:", value = f"<:icons_text1:1223137135335575695> {len(self.bot.slash_commands)}")
        info.add_field(name = "Кол-во гильдий:", value = f"<:icons_text1:1223137135335575695> {len(self.bot.guilds)}")
        info.add_field(name = "Кол-во пользователей:", value = f"<:icons_text1:1223137135335575695> {len(self.bot.users)}", inline=False)
        info.add_field(name="Ping:", value=f"<:icons_text1:1223137135335575695> {round(self.bot.latency * 1000)}ms")
        info.set_footer(text="Hikasami (Creativity Community) © 2024 Все права защищены")
        await ctx.send(embed=info, ephemeral=True)


def setup(bot):
    bot.add_cog(infobots(bot))
