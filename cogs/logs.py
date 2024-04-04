import disnake
from disnake.ext import commands


class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            overwrites = {
                guild.default_role: disnake.PermissionOverwrite(read_messages=False),
                guild.me: disnake.PermissionOverwrite(read_messages=True, read_message_history=True, mention_everyone=False)
            }
            
            category = disnake.utils.get(guild.categories, name="Логи")
            if not category:
                category = await guild.create_category("Логи")
            admin_channel = disnake.utils.get(category.text_channels, name="admin-logs")
            if not admin_channel:
                admin_channel = await category.create_text_channel("admin-logs", overwrites=overwrites)
            
            bot_member = guild.get_member(self.bot.user.id)
            await admin_channel.set_permissions(bot_member, overwrite=disnake.PermissionOverwrite(send_messages=True, read_messages=True, mention_everyone=False))


    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = disnake.utils.get(member.guild.text_channels, name="admin-logs")
        if channel:
            embed = disnake.Embed(description=f"<:icons_djoin:1223145579295670292> Пользователь {member.mention} присоединился к серверу.", color=0x2f3136)
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = disnake.utils.get(member.guild.text_channels, name="admin-logs")
        if channel:
            embed = disnake.Embed(description=f"<:icons_dleave:1223145723940569171> Пользователь {member.mention} покинул сервер.", color=0x2f3136)
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.roles != after.roles:
            role_changes = []
            for role in before.roles:
                if role not in after.roles:
                    role_changes.append(f"<:icons_dred:1223137493503705189> Убрана роль {role.mention}")
            for role in after.roles:
                if role not in before.roles:
                    role_changes.append(f"<:icons_dgreen:1223137518812401766> Добавлена роль {role.mention}")
            if role_changes:
                channel = disnake.utils.get(before.guild.text_channels, name="admin-logs")
                if channel:
                    role_changes_str = "\n".join(role_changes)
                    executor = None
                    for role in before.roles:
                        if role not in after.roles:
                            changes = await after.guild.audit_logs(limit=1, action=disnake.AuditLogAction.member_role_update).flatten()
                            executor = changes[0].user.mention if changes else "Неизвестно"
                            break
                    author = after
                    embed = disnake.Embed(description=f"<:icons_edit:1223146033438261299> Пользователь {author.mention} изменил роли:\n{role_changes_str}\n\n<:icons_text1:1223137135335575695> Выполнил: {executor}", color=0x2f3136)
                    await channel.send(embed=embed)

        if before.display_name != after.display_name:
            channel = disnake.utils.get(before.guild.text_channels, name="admin-logs")
            if channel:
                executor = before.guild.me.mention
                author = after
                embed = disnake.Embed(description=f"<:icons_edit:1223146033438261299> Пользователь {author.mention} изменил никнейм: {before.display_name} -> {after.display_name}\n<:icons_text1:1223137135335575695> Выполнил: {executor}", color=0x2f3136)
                await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel != after.channel:
            channel = disnake.utils.get(member.guild.text_channels, name="admin-logs")
            if channel:
                if before.channel:
                    embed = disnake.Embed(description=f"<:icons_calldisconnect:1223146163130073198> Пользователь {member.mention} покинул голосовой канал {before.channel.name}.", color=0x2f3136)
                    await channel.send(embed=embed)
                if after.channel:
                    embed = disnake.Embed(description=f"<:icons_callconnect:1223146261738291322> Пользователь {member.mention} присоединился к голосовому каналу {after.channel.name}.", color=0x2f3136)
                    await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        if isinstance(channel, disnake.TextChannel):
            log_channel = disnake.utils.get(channel.guild.text_channels, name="admin-logs")
            if log_channel:
                embed = disnake.Embed(description=f"<:icons_plus:1223137642556948620> Создан новый текстовый канал: {channel.mention}\n<:icons_text1:1223137135335575695> Пользователь {channel.guild.me.mention}", color=0x2f3136)
                await log_channel.send(embed=embed)
        elif isinstance(channel, disnake.VoiceChannel):
            log_channel = disnake.utils.get(channel.guild.text_channels, name="admin-logs")
            if log_channel:
                embed = disnake.Embed(description=f"<:icons_plus:1223137642556948620> Создан новый голосовой канал: {channel.mention}\n<:icons_text1:1223137135335575695> Пользователь {channel.guild.me.mention}", color=0x2f3136)
                await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        if isinstance(channel, disnake.TextChannel):
            log_channel = disnake.utils.get(channel.guild.text_channels, name="admin-logs")
            if log_channel:
                executor = channel.guild.me.mention
                embed = disnake.Embed(description=f"<:icons_delete:1223146513128095754> Удален текстовый канал: {channel.mention}\n<:icons_text1:1223137135335575695> Выполнил: {executor}", color=0x2f3136)
                await log_channel.send(embed=embed)
        elif isinstance(channel, disnake.VoiceChannel):
            log_channel = disnake.utils.get(channel.guild.text_channels, name="admin-logs")
            if log_channel:
                executor = channel.guild.me.mention
                embed = disnake.Embed(description=f"<:icons_delete:1223146513128095754> Удален голосовой канал: {channel.mention}\n<:icons_text1:1223137135335575695> Выполнил: {executor}", color=0x2f3136)
                await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        if isinstance(before, disnake.TextChannel) and isinstance(after, disnake.TextChannel):
            if before.name != after.name:
                log_channel = disnake.utils.get(before.guild.text_channels, name="admin-logs")
                if log_channel:
                    embed = disnake.Embed(description=f"<:icons_edit:1223146033438261299> Пользователь {before.guild.me.mention} изменил название текстового канала: {before.mention} -> {after.mention}", color=0x2f3136)
                    await log_channel.send(embed=embed)

        elif isinstance(before, disnake.VoiceChannel) and isinstance(after, disnake.VoiceChannel):
            if before.name != after.name:
                log_channel = disnake.utils.get(before.guild.text_channels, name="admin-logs")
                if log_channel:
                    embed = disnake.Embed(description=f"<:icons_edit:1223146033438261299> Пользователь {before.guild.me.mention} изменил название голосового канала: {before.mention} -> {after.mention}", color=0x2f3136)
                    await log_channel.send(embed=embed)

        elif isinstance(before, disnake.TextChannel) and isinstance(after, disnake.VoiceChannel):
            log_channel = disnake.utils.get(before.guild.text_channels, name="admin-logs")
            if log_channel:
                embed = disnake.Embed(description=f"<:icons_edit:1223146033438261299> Пользователь {before.guild.me.mention} изменил тип канала: Текстовый {before.mention} -> Голосовой {after.mention}", color=0x2f3136)
                await log_channel.send(embed=embed)

        elif isinstance(before, disnake.VoiceChannel) and isinstance(after, disnake.TextChannel):
            log_channel = disnake.utils.get(before.guild.text_channels, name="admin-logs")
            if log_channel:
                embed = disnake.Embed(description=f"<:icons_edit:1223146033438261299> Пользователь {before.guild.me.mention} изменил тип канала: Голосовой {before.mention} -> Текстовый {after.mention}", color=0x2f3136)
                await log_channel.send(embed=embed)


    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot:
            return

        if before.content != after.content:
            channel = disnake.utils.get(before.guild.text_channels, name="admin-logs")
            if channel:
                executor = before.guild.me.mention
                author = before.author
                embed = disnake.Embed(description=f"<:icons_edit:1223146033438261299> Пользователь {author.mention} изменил своё сообщение:\n"
                                                  f"До: {before.content}\nПосле: {after.content}\n<:icons_text1:1223137135335575695> Выполнил: {executor}", color=0x2f3136)
                await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return

        channel = disnake.utils.get(message.guild.text_channels, name="admin-logs")
        if channel:
            executor = message.guild.me.mention
            author = message.author
            embed = disnake.Embed(description=f"<:icons_delete:1223146513128095754> Пользователь {author.mention} удалил своё сообщение:\n{message.content}\n<:icons_text1:1223137135335575695> Выполнил: {executor}", color=0x2f3136)
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages):
        for message in messages:
            if message.author.bot:
                continue

            channel = disnake.utils.get(message.guild.text_channels, name="admin-logs")
            if channel:
                executor = message.guild.me.mention
                author = message.author
                embed = disnake.Embed(description=f"<:icons_delete:1223146513128095754> Пользователь {author.mention} удалил несколько сообщений.", color=0x2f3136)
                await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_bulk_delete(self, messages):
        for message in messages:
            if message.author.bot:
                continue

            channel = disnake.utils.get(message.guild.text_channels, name="admin-logs")
            if channel:
                executor = message.guild.me.mention
                author = message.author
                embed = disnake.Embed(description=f"<:icons_delete:1223146513128095754> Пользователь {author.mention} удалил несколько сообщений.", color=0x2f3136)
                await channel.send(embed=embed)


    @commands.Cog.listener()
    async def on_member_move(self, member, before, after):
        channel = disnake.utils.get(member.guild.text_channels, name="admin-logs")
        if channel:
            embed = disnake.Embed(description=f"<:icons_linked:1223146645060063313> Пользователь {member.mention} переместился из канала {before.channel.name} в канал {after.channel.name}.", color=0x2f3136)
            await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Logs(bot))
