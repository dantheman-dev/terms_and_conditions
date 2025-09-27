from datetime import datetime, timezone
from terms.db import Session
from terms.models import UserConsent, ConsentDisplay
from terms.constants import DISCLAIMER_VERSION, DISCLAIMER_HASH

def has_active_consent(guild_id: int, user_id: int) -> bool:
    with Session() as s:
        return s.query(UserConsent).filter_by(
            guild_id=str(guild_id), discord_user_id=str(user_id), version=DISCLAIMER_VERSION
        ).first() is not None

def record_consent(guild_id: int, user_id: int, method: str) -> None:
    with Session() as s, s.begin():
        s.add(UserConsent(
            guild_id=str(guild_id),
            discord_user_id=str(user_id),
            version=DISCLAIMER_VERSION,
            disclaimer_hash=DISCLAIMER_HASH,
            method=method,
            consented_at=datetime.now(timezone.utc),
        ))

def record_display(guild_id: int, user_id: int, command: str) -> None:
    with Session() as s, s.begin():
        s.add(ConsentDisplay(
            guild_id=str(guild_id),
            discord_user_id=str(user_id),
            command=command,
            displayed_at=datetime.now(timezone.utc),
            disclaimer_hash=DISCLAIMER_HASH,
        ))
