import disnake
from disnake import Embed
from disnake.ext import commands
from datetime import datetime


class profile(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.slash_command(name='profile', description='Посмотреть свой профиль')
    async def userinfo(self, inter, member: disnake.Member = None):
        if member is None:
            member = inter.author

        роли = member.roles  
        упоминаемые_роли = []  
        for роль in роли: 
            упоминаемые_роли.append(роль.mention) 
        упоминаемые_роли = str(упоминаемые_роли).replace('[', '').replace(']', '').replace("'", '') 
        верхняя_роль = member.top_role.mention 

        embed = disnake.Embed(
            title=f' Информация о пользователе {member.name}',
            color=0x2f3136
        )
        embed.set_thumbnail(url=member.avatar)
        embed.add_field(name='** ID  **', value=f'<:icons_text1:1223137135335575695> {member.id}', inline=False)
        embed.add_field(name='** Никнейм  **', value=f'<:icons_text1:1223137135335575695> {member.name}', inline=False)
        embed.add_field(name='** Отображаемое имя **', value=f'<:icons_text1:1223137135335575695> {member.display_name}', inline=False)
        embed.add_field(name='** Создан в **', value=f"<:icons_text1:1223137135335575695> <t:{int(member.created_at.timestamp())}>", inline=False)
        embed.add_field(name='** Присоединился в **', value=f"<:icons_text1:1223137135335575695> <t:{int(member.joined_at.timestamp())}>", inline=False)
        embed.add_field(name='** Роли **', value=f'<:icons_text1:1223137135335575695> {упоминаемые_роли}', inline=False)
        embed.add_field(name='** Высшая роль **', value=f'<:icons_text1:1223137135335575695> {верхняя_роль}', inline=False)
        embed.add_field(name='** Статус **', value=f'<:icons_text1:1223137135335575695> {member.status}', inline=False)
        await inter.response.send_message(embed=embed)


def setup(client: commands.Bot):
    client.add_cog(profile(client))