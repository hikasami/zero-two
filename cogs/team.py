import disnake
from disnake.ext import commands
from random import randint, random




class team(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name= "team", description="Наша команда",guild_ids=[973182837735972864, 1218065967196930109])
    async def bot(self, ctx):
        info=disnake.Embed(title = "Команда Hikasami", color=0x2f3136)

        info.add_field(name = "Должность", value = "<:icons_paintpadbrush:1223389462462074910> Front-End Engineer\n<:icons_Bugs:1223389595543277700> Back-End Engineer\n<:icons_wumpus:1223389639839056024> Discord Engineer\n<:icons_Bugs:1223389595543277700> Support TS/JS Engineer\n<:icons_connect:1223389721472925837> Security Engineer", inline=True)
        info.add_field(name = "Назначенный", value = "<@920409051408531466>\n<@849946734666317844>\n<@702187267988652032>\n<@502386908245000192>\n<@1223380541034991660>", inline=True)

        info.set_footer(text="Hikasami (Creativity Community) © 2024 Все права защищены")
        await ctx.send(embed=info)


def setup(bot):
    bot.add_cog(team(bot))
