from datetime import datetime

import disnake
from disnake.ext import commands


class ServerInfo(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.slash_command(name='serverinfo', description='Отображает информацию о сервере')
    async def serverinfo(self, inter: disnake.ApplicationCommandInteraction):
        guild = inter.guild

        if guild.id == 973182837735972864:
            desc = '<:icons_colorserververified:1223137462403072091> **Официальный сервер Hikasami**'
        elif guild.id == 1218065967196930109: 
            desc = '<:icons_colorstaff:1223155324803088406> **Официальный тестовый сервер Hikasami**'
        else:
            desc = ''

        embed = disnake.Embed(
            title='Информация о сервере',
            color=0x2f3136,
            description=desc
        )
        embed.set_thumbnail(url=guild.icon.url)
        embed.set_author(name=guild.name)

        embed.add_field(name='**Уровень верификации**', value=f"<:icons_text1:1223137135335575695> {str(guild.verification_level).title()}",
                        inline=True)
        
        if guild.id == 973182837735972864:
            embed.add_field(name='**Владелец**', value=f"<:icons_text1:1223137135335575695> Creativity Community", inline=False)
        else:
            embed.add_field(name=' **Владелец**', value=f"<:icons_text1:1223137135335575695> {guild.owner}", inline=False)

        embed.add_field(name='**Дата создания**', value=f"<t:{int(guild.created_at.timestamp())}>", inline=False)
        embed.add_field(name='**Количество каналов**', inline=False,
                        value=f" <:icons_text5:1223138578117169213> Всего `{len(guild.channels)}`\n <:icons_text2:1223137393347919902> Текстовые `{len(guild.text_channels)}`\n <:icons_text2:1223137393347919902> Голосовые `{len(guild.voice_channels)}`\n <:icons_text1:1223137135335575695> Категории `{len(guild.categories)}`")
        embed.add_field(name='**Участники**',  inline=False,
                        value=f" <:icons_text5:1223138578117169213> Всего `{guild.member_count}`\n <:icons_text2:1223137393347919902> Пользователей `{len([x for x in guild.members if not x.bot])}`\n <:icons_text1:1223137135335575695> Ботов `{len([bot for bot in guild.members if bot.bot])}`")

        await inter.response.send_message(embed=embed)


def setup(client: commands.Bot):
    client.add_cog(ServerInfo(client))
