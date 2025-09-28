import discord

from terms.config import Settings

settings = Settings()
_SHARPS_ROLE_CACHE: dict[int, int] = {}

def find_sharps_role(guild: discord.Guild) -> discord.Role | None:
    role_id = settings.SHARPS_ROLE_ID
    if role_id is not None:
        role = guild.get_role(role_id)
        if role is not None:
            return role

    cached_role_id = _SHARPS_ROLE_CACHE.get(guild.id)
    if cached_role_id is not None:
        cached_role = guild.get_role(cached_role_id)
        if cached_role is not None:
            return cached_role
        _SHARPS_ROLE_CACHE.pop(guild.id, None)

    if settings.SHARPS_ROLE_NAME:
        role = discord.utils.get(guild.roles, name=settings.SHARPS_ROLE_NAME)
        if role is not None:
            _SHARPS_ROLE_CACHE[guild.id] = role.id
        return role

    return None

async def grant_sharps(member: discord.Member) -> bool:
    role = find_sharps_role(member.guild)
    if not role:
        return False
    if role in member.roles:
        return True
    await member.add_roles(role, reason="Consent accepted")
    return True

async def remove_sharps(member: discord.Member) -> bool:
    role = find_sharps_role(member.guild)
    if not role:
        return False
    if role not in member.roles:
        return True
    await member.remove_roles(role, reason="Consent declined")
    return True
