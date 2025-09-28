import discord
from discord.ext import commands
from discord import app_commands
from terms.constants import CONSENT_TEXT
from terms.consent import record_consent
from terms.roles import grant_sharps, remove_sharps

AGREE_ID   = "terms:consent:agree"
DECLINE_ID = "terms:consent:decline"

class ConsentView(discord.ui.View):
    """Interactive consent card for onboarding."""

    def __init__(self, *, persistent: bool = False):
        super().__init__(timeout=None if persistent else 180)
        self.add_item(
            discord.ui.Button(label="I Agree", style=discord.ButtonStyle.success, custom_id=AGREE_ID)
        )
        self.add_item(
            discord.ui.Button(label="Decline", style=discord.ButtonStyle.danger, custom_id=DECLINE_ID)
        )

class Onboarding(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        try:
            embed = discord.Embed(title="Welcome to Xedge Beta", description=CONSENT_TEXT, color=0xF39C12)
            await member.send(embed=embed, view=ConsentView())
        except discord.Forbidden:
            pass  # DMs closed; they'll use /start

    @app_commands.command(name="start", description="Read & accept the Risk Notice to receive the Sharps role")
    async def start(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Xedge Terms & Conditions", description=CONSENT_TEXT, color=0xF39C12)
        await interaction.response.send_message(embed=embed, view=ConsentView(), ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Onboarding(bot))
    bot.add_view(ConsentView(persistent=True))  # persistent view
