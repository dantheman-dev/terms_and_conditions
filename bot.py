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
    if guild is None:
        guild = bot.get_guild(settings.GUILD_ID)
        if guild:
            log.debug(
                "interaction.guild_resolved_from_cache id=%s guild=%s",
                interaction.id,
                guild.id,
            )
    if guild is None:
        try:
            guild = await bot.fetch_guild(settings.GUILD_ID)
        except discord.HTTPException as exc:
            log.warning(
                "interaction.guild_fetch_failed id=%s guild=%s exc=%s",
                interaction.id,
                settings.GUILD_ID,
                exc,
            )
        else:
            log.info(
                "interaction.guild_resolved_via_fetch id=%s guild=%s",
                interaction.id,
                guild.id,
            )

    member = interaction.user if isinstance(interaction.user, discord.Member) else None
    if member is None and guild is not None:
        member = guild.get_member(interaction.user.id)
        if member:
            log.debug(
                "interaction.member_resolved_from_cache id=%s guild=%s member=%s",
                interaction.id,
                guild.id,
                member.id,
            )
    if member is None and guild is not None:
        try:
            member = await guild.fetch_member(interaction.user.id)
        except discord.HTTPException as exc:
            log.warning(
                "interaction.member_fetch_failed id=%s guild=%s user=%s exc=%s",
                interaction.id,
                guild.id if guild else "?",
                interaction.user.id,
                exc,
            )
        else:
            log.info(
                "interaction.member_resolved_via_fetch id=%s guild=%s member=%s",
                interaction.id,
                guild.id,
                member.id,
            )

    if not guild or not member:
        await interaction.response.send_message("Guild/member missing.", ephemeral=True)
        log.error(
            "interaction.guild_or_member_missing id=%s guild=%s user=%s",
            interaction.id,
            getattr(guild, "id", None),
            interaction.user.id,
        )
        return

    method = "dm_button" if isinstance(interaction.channel, discord.DMChannel) else "channel_button"
    if method == "dm_button":
        log.info(
            "interaction.dm_button_resolved id=%s guild=%s member=%s",
            interaction.id,
            guild.id,
            member.id,
        )

    if cid == "terms:consent:agree":
        await interaction.response.defer(ephemeral=True)
        created = False
        granted = False
        followup_message: str | None = None

        try:
            created = await asyncio.to_thread(record_consent, guild.id, member.id, method=method)
        except Exception:
            log.exception(
                "consent.record_failed guild=%s user=%s", guild.id, member.id
            )
            followup_message = (
                "⚠️ We couldn't record your agreement due to an internal error. Please try again."
            )

        if followup_message is None:
            try:
                granted = await grant_sharps(member)
            except Exception:
                log.exception(
                    "consent.role_grant_failed guild=%s user=%s", guild.id, member.id
                )
                followup_message = (
                    "⚠️ Agreed, but there was an error applying **Sharps**. Please contact an admin."
                )

        if followup_message is None:
            followup_message = (
                "✅ Agreed. **Sharps** role granted. You can use Xedge now."
                if granted
                else "✅ Agreed, but admin must fix role: **Sharps** missing or bot role below Sharps."
            )

        await interaction.followup.send(followup_message, ephemeral=True)
        log.info(
            "consent.accepted guild=%s user=%s consent_recorded=%s",
            guild.id,
            member.id,
            created,
        )
    else:
        await interaction.response.defer(ephemeral=True)
        followup_message = (
            "❌ Understood. Without agreement, **Sharps** won’t be granted. Run `/start` anytime."
        )
        try:
            await remove_sharps(member)
        except Exception:
            log.exception(
                "consent.role_remove_failed guild=%s user=%s", guild.id, member.id
            )
            followup_message = (
                "⚠️ We couldn't remove **Sharps** due to an internal error. Please contact an admin."
            )

        await interaction.followup.send(followup_message, ephemeral=True)
        log.info("consent.declined guild=%s user=%s", guild.id, member.id)

if __name__ == "__main__":
    bot.run(settings.DISCORD_TOKEN)
