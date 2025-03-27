import discord
from discord.ext import commands
from discord.ui import View, Button
import asyncio
import os

TOKEN = os.getenv("TOKEN")
GUILD_ID = 1176953174553272320
TEXT_CHANNEL_ID = 1354437448796471406

ROLES = {
    "Slot 1 ": 1351400004887121940,
    "Slot 2 ": 1351410394710675486,
    "Slot 3 ": 1354443506558697553,
    "Slot 4 ": 1354443924764229764,
    "Slot 5 ": 1354445824800587786,
    "Slot 6 ": 1354446105563234374,
    "Slot 7 ": 1354446222018215986,
    "Slot 8 ": 1354446355279515891,
    "Slot 9 ": 1354446462615814414,
    "Slot 10": 1354446560225919128,
    "Slot 11": 1354447244782473366,
    "Slot 12": 1354447380530991316,
    "Slot 13": 1354447512840306808,
    "Slot 14": 1354447616976359625,
    "Slot 15": 1354447710765187163,
}

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

class SlotView(View):
    def __init__(self):
        super().__init__(timeout=None)
        row = 0
        for i, (slot_name, role_id) in enumerate(ROLES.items()):
            self.add_item(SlotButton(slot_name, role_id, row))
            if (i + 1) % 4 == 0:
                row += 1

class SlotButton(Button):
    def __init__(self, label, role_id, row):
        super().__init__(label=label, style=discord.ButtonStyle.green, row=row)
        self.role_id = role_id

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        user = interaction.user
        role = guild.get_role(self.role_id)

        if any(r.id in ROLES.values() for r in user.roles):
            await interaction.response.send_message(
                "⚠️ Ya tienes un slot asignado. Espera a que expire para cambiarlo.", ephemeral=True
            )
            return

        role_members = len([member for member in guild.members if role in member.roles])
        if role_members >= 6:
            await interaction.response.send_message(
                f"⚠️ El slot **{self.label}** ya tiene el máximo de 6 personas.", ephemeral=True
            )
            return

        await user.add_roles(role)
        await interaction.response.send_message(
            f"✅ Has elegido **{self.label}**. Tienes acceso por 24 horas.", ephemeral=True
        )

        await asyncio.sleep(86400)  # 24 horas
        await user.remove_roles(role)
        await user.send(f"❌ Tu acceso a **{self.label}** ha expirado.")

@bot.event
async def on_ready():
    print(f"{bot.user} conectado.")
    channel = bot.get_channel(TEXT_CHANNEL_ID)
    if channel:
        await channel.purge()
        embed = discord.Embed(
            title="🎟️ Selección de Slots Scrims",
            description="Haz clic en un botón para elegir tu slot. Solo puedes tener **uno** cada **24 horas**. Máximo 6 personas por slot.",
            color=0x43A700
        )
        await channel.send(embed=embed, view=SlotView())

if __name__ == "__main__":
    bot.run(TOKEN)