import disnake
import sqlite3
from disnake.ext import commands
import typing

class mutechat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="mchat", description="Блокировка доступа к Текстовым каналам")
    @commands.has_permissions(administrator=True)
    async def warn(self, ctx, user: disnake.Member, reason: str):
        conn = sqlite3.connect('warn.db')
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS bad_words (word TEXT)")
        c.execute('''CREATE TABLE IF NOT EXISTS warnings (user_id INTEGER PRIMARY KEY, num_warnings INTEGER)''')

        embed = disnake.Embed(title="Блокировка доступа к Текстовым каналам", color=0x2f3136)
        embed.add_field(name="Пользователь", value=f"<:icons_text1:1223137135335575695> {user.mention}")
        embed.add_field(name="Причина", value=f"<:icons_text1:1223137135335575695> `{reason}`")
        await ctx.response.send_message(embed=embed, ephemeral=True)

        try:
            role = await ctx.guild.create_role(name="mute", reason="Автоматическая роль для блокирвки доступа к Текстовым каналам")
            for channel in ctx.guild.channels:
                await channel.set_permissions(role, send_messages=False)
            await user.add_roles(role)

            dm_channel = await user.create_dm()
            embed = disnake.Embed(title="Вы получили блокировку Текстовых каналов", color=0x2f3136)
            embed.add_field(name="Сервер", value=f"<:icons_text1:1223137135335575695> {ctx.guild.name}")
            embed.add_field(name="Причина", value=f"<:icons_text1:1223137135335575695> `{reason}`")
            await dm_channel.send(embed=embed)

            c.execute("SELECT * FROM warnings WHERE user_id=?", (user.id,))
            row = c.fetchone()
            if row:
                num_warnings = row[1] + 1
                c.execute("UPDATE warnings SET num_warnings=? WHERE user_id=?", (num_warnings, user.id))
            else:
                c.execute("INSERT INTO warnings VALUES (?, ?)", (user.id, 1))

            conn.commit()
            c.execute("SELECT * FROM warnings WHERE user_id=?", (user.id,))
            row = c.fetchone()
            if row and row[1] >= 5:
                kick_embed = disnake.Embed(title="Пользователь был исключен за многочисленные нарушения", color=0x2f3136)
                kick_embed.add_field(name="Участник", value=f"<:icons_text1:1223137135335575695> {user.mention}")
                kick_embed.add_field(name="Причина", value=f"<:icons_text1:1223137135335575695> Получено `{row[1]}` предупреждений")
                await ctx.response.send_message(embed=kick_embed, ephemeral=True)
                await dm_channel.send(embed=kick_embed)
                await dm_channel.send(f"<:icons_kick:1223137566123884606> Вы были исключены с сервера `{ctx.guild.name}` за многочисленные нарушения.")
                await user.kick(reason="Получено 5 предупреждения")
        except disnake.errors.Forbidden:
            await ctx.response.send_message("У меня нет прав, чтобы предупредить этого пользователя", ephemeral=True)


    @commands.slash_command(name="unmchat", description="Разблокировка доступа к Текстовым каналам")
    @commands.has_permissions(administrator=True)
    async def unwarn(self, ctx, user: disnake.Member):
        conn = sqlite3.connect('warn.db')
        c = conn.cursor()

        c.execute("SELECT * FROM warnings WHERE user_id=?", (user.id,))
        row = c.fetchone()
        if row:
            num_warnings = row[1] - 1
            if num_warnings <= 0:
                c.execute("DELETE FROM warnings WHERE user_id=?", (user.id,))
            else:
                c.execute("UPDATE warnings SET num_warnings=? WHERE user_id=?", (num_warnings, user.id))
            conn.commit()
            role = disnake.utils.get(ctx.guild.roles, name="mute")
            if role:
                await user.remove_roles(role)

            admin_name = ctx.author.name
            admin_avatar = ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url

            embed = disnake.Embed(title="У вас сняли блокировку доступа к Текстовым каналам", color=0x2f3136)
            embed.add_field(name="Сервер", value=f"<:icons_text1:1223137135335575695> {ctx.guild.name}", inline=False)
            embed.add_field(name="Предупреждения", value=f"<:icons_text1:1223137135335575695> У вас осталось {num_warnings} предупреждений.", inline=False)
            embed.add_field(name="Снял блокировку ", value=f"<:icons_text1:1223137135335575695> Администратор: {admin_name}", inline=False)
            embed.set_thumbnail(url=ctx.guild.icon.url)
            await user.send(embed=embed)

            await ctx.response.send_message(embed=disnake.Embed(title="Предупреждение снято", color=0x2f3136).add_field(name="Пользователь", value=user.mention), ephemeral=True)
        else:
            await ctx.response.send_message(embed=disnake.Embed(title="У пользователя нет предупреждений", color=0x2f3136).add_field(name="Пользователь", value=user.mention), ephemeral=True)


    @commands.slash_command(name="mchatinfo", description="Показать список пользователей с блокировкой Текстовых каналов")
    async def warnings(self, ctx, user: typing.Optional[disnake.Member] = None):
        conn = sqlite3.connect('warn.db')
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS warnings
                 (user_id INTEGER PRIMARY KEY, num_warnings INTEGER)''')
        c = conn.cursor()

        c.execute("CREATE TABLE IF NOT EXISTS bad_words (word TEXT)")
        if user is None:
            c.execute("SELECT * FROM warnings")
            rows = c.fetchall()
            if rows:
                embed = disnake.Embed(title="Список блокировок на сервере", color=0x2f3136)
                for row in rows:
                    user = ctx.guild.get_member(row[0])
                    if user:
                        embed.add_field(name=f"Участник: {user.display_name}", value=f"Предупреждений: {row[1]}", inline=False)
            else:
                embed = disnake.Embed(title=" На сервере нет блокировок", color=0x2f3136)
            await ctx.response.send_message(embed=embed, ephemeral=True)
        else:
            c.execute("SELECT * FROM warnings WHERE user_id=?", (user.id,))
            row = c.fetchone()
            if row:
                embed = disnake.Embed(title=f" Предупреждения пользователя {user.display_name}", color=0x2f3136)
                embed.add_field(name="Предупреждений", value=row[1])
            else:
               embed = disnake.Embed(title=f"У пользователя {user.display_name} нет предупреждений", color=0x2f3136)
            await ctx.response.send_message(embed=embed, ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(mutechat(bot))
