import disnake
from disnake.ext import commands
import os 
import sys


class Restart(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.developer_ids = {
            702187267988652032: True,  # Developer ID 1
            920409051408531466: True,  # Developer ID 2
            1139274531580694580: True, # Developer ID 3
            502386908245000192: True,  # Developer ID 4
            # Add more developer IDs as needed
        }

    @commands.slash_command(name='restart', description='Выполняет полную перезагрузку бота')
    async def restart(self, inter):
        if inter.author.id not in self.developer_ids:
            await inter.response.send_message("<:icons_Wrong:1223137173797343243> Вы не являетесь разработчиком бота и не можете использовать эту команду.", ephemeral=True)
            return

        embed = disnake.Embed(
            description="<:icons_Correct:1223137153140392018> Команда перезагрузки была успешно выполнена, ожидайте включения!",
            color=0x2f3136

        )
        await inter.response.send_message(embed=embed, ephemeral=True)
        restart()

def restart():
    print('Выполняется рестарт. Бот будет включен через пару секунд!')
    os.system('cls')
    os.execl(sys.executable, sys.executable, *sys.argv)

def setup(client: commands.Bot):
    client.add_cog(Restart(client))
