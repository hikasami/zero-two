import disnake
from disnake.ext import commands



class helpc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.slash_command(name="help", description="Помощь по командам.", permissions=[disnake.Permissions().none()])
    async def __help(self, ctx):
        view = design_help_cmd()
        embed = disnake.Embed(title=f'**Список команд**', description='Пожалуйста, выберите категорию.', color=0x2f3136)
        embed.set_footer(text=f"Запросил команду: {ctx.author.name}")
        await ctx.send(embed=embed, view=view, ephemeral=True)


class design_help_cmd(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(help_cmd())

class help_cmd(disnake.ui.Select):
    def __init__(self):
        options = [
            disnake.SelectOption(label='Для разработчиков', description='Команды для разработчиков Creativity Community.', emoji='<:icons_hammer:949635040424374342>'),
            disnake.SelectOption(label='Модерация', description='Команды для Модераторов/Администрации.', emoji='<:icons_stagemoderator:988409363255410688>'),
            disnake.SelectOption(label='Общее', description='Общие команды.', emoji='<:icons_shine1:859424400959602718>'),
        ]
        super().__init__(placeholder='Выбор категории', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: disnake.Interaction):
        if "Модерация" in self.values:
            embed = disnake.Embed(color=0x2f3136)
            embed.add_field(name='Модерация', value=(
                '`/clear` >  Очистка чата\n'
                '`/embed` > Эмбед от имени бота\n'
                '`/kick` > Выгнать пользователя с сервера\n'
                '`/ban` > Забанить пользователя на сервере\n'
                '`/join` > Зайти в голосовой канал\n'
                '`/leave` > Выйти из голосового канала\n'
                '`/echo` > Отправить сообщение от имени бота\n'
                '`/stay` > Оставить Zero Two в голосовом канале\n'
                '`/create_role` > Создание новой роли\n'
                '`/assign_role` > Выдача роли пользователю\n'
                '`/setroleap` > Установить роль для Автовыдачи\n'
                '`/remove_role` > Удаление роли у пользователя\n'
                '`/setcolorrole` > Изменить цвет роли\n'
                '`/voting` > Провести голосование\n'
                '`/send-dm` > Отправить в лс сообщение от имени бота\n'
                '`/voicemute` > Замьютить пользователя в голосовых каналах\n'
                '`/unvoicemute` > Размьютить пользователя в голосовых каналах\n'
                '`/mchat` > Блокировка чата пользователю\n'
                '`/unmchat` > Снять блокировку чата у пользователя\n'
                '`/mchatinfo` > Показать список пользователей в муте\n'
            ))
            await interaction.response.edit_message(embed=embed)
        if "Для разработчиков" in self.values:
            embed = disnake.Embed(color=0x2f3136)
            embed.add_field(name='Для разработчиков', value=(
                '`/restart` > Выполняет полную перезагрузку бота.\n'
                '`/status` > Информация о статусе бота.\n'
            ))
            await interaction.response.edit_message(embed=embed)
        if "Общее" in self.values:
            embed = disnake.Embed(color=0x2f3136)
            embed.add_field(name='Общее', value=(
                '`/help` > Посмотреть все команды\n'
                '`/profile` > Узнать свою статистику\n'
                '`/server` > Просмотр информации о сервере\n'
                '`/ticket` > Создать тикет для связи с администрацией\n'
            ))
            await interaction.response.edit_message(embed=embed)

def setup(bot):
    bot.add_cog(helpc(bot))