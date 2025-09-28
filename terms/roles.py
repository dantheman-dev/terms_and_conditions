import discord
from terms.config import Settings
settings = Settings()

def find_sharps_role(guild: discord.Guild) -> discord.Role | None:
    role_id = settings.SHARPS_ROLE_ID
    if role_id is not None:
        role = guild.get_role(role_id)
        if role is not None:
            return role

    if settings.SHARPS_ROLE_NAME:
        return discord.utils.get(guild.roles, name=settings.SHARPS_ROLE_NAME)

    return None

async def grant_sharps(member: discord.Member) -> bool:
    role = find_sharps_role(member.guild)
    if not role: return False
    if role in member.roles: return True
    await member.add_roles(role, reason="Consent accepted")
    return True

async def remove_sharps(member: discord.Member) -> bool:
    role = find_sharps_role(member.guild)
    if not role: return False
    if role not in member.roles: return True
    await member.remove_roles(role, reason="Consent declined")
    return True
