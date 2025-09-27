import asyncio

import discord
from discord.ext import commands
from terms.config import Settings
from terms.db import ENGINE
from terms.models import Base
from terms.consent import record_consent
from terms.roles import grant_sharps, remove_sharps
from terms.logging import get_logger

settings = Settings()
log = get_logger("terms_and_conditions")

intents = discord.Intents.none()
intents.guilds = True
intents.members = True  # role ops + on_member_join

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def setup_hook():
    await asyncio.to_thread(Base.metadata.create_all, ENGINE)
    await bot.load_extension("terms.cogs.onboarding")

    guild_obj = discord.Object(id=settings.GUILD_ID)
    bot.tree.copy_global_to(guild=guild_obj)
    await bot.tree.sync(guild=guild_obj)
    log.info("Command tree synced for guild %s", settings.GUILD_ID)

@bot.event
async def on_ready():
    log.info("Logged in as %s (%s)", bot.user, bot.user.id)

@bot.event
async def on_interaction(interaction: discord.Interaction):
    data = getattr(interaction, "data", None)
    if not isinstance(data, dict):
        return
    cid = data.get("custom_id")
    if cid not in ("terms:consent:agree", "terms:consent:decline"):
        return

    guild = interaction.guild
    member = interaction.user if isinstance(interaction.user, discord.Member) else None
    if not guild or not member:
        await interaction.response.send_message("Guild/member missing.", ephemeral=True)
        return

    method = "dm_button" if isinstance(interaction.channel, discord.DMChannel) else "channel_button"

    if cid == "terms:consent:agree":
        await asyncio.to_thread(record_consent, guild.id, member.id, method=method)
        granted = await grant_sharps(member)
        msg = ("✅ Agreed. **Sharps** role granted. You can use Xedge now."
               if granted else
               "✅ Agreed, but admin must fix role: **Sharps** missing or bot role below Sharps.")
        await interaction.response.send_message(msg, ephemeral=True)
        log.info("consent.accepted guild=%s user=%s", guild.id, member.id)
    else:
        await remove_sharps(member)
        await interaction.response.send_message(
            "❌ Understood. Without agreement, **Sharps** won’t be granted. Run `/start` anytime.",
            ephemeral=True
        )
        log.info("consent.declined guild=%s user=%s", guild.id, member.id)

if __name__ == "__main__":
    bot.run(settings.DISCORD_TOKEN)
