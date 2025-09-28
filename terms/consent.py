from datetime import datetime, timezone
from sqlalchemy import select

from terms.db import Session
from terms.models import UserConsent
from terms.constants import DISCLAIMER_VERSION, DISCLAIMER_HASH

def record_consent(guild_id: int, user_id: int, method: str) -> bool:
    """Persist a consent decision, returning True if a new row was created."""

    with Session() as session:
        existing = session.execute(
            select(UserConsent).where(
                UserConsent.guild_id == guild_id,
                UserConsent.discord_user_id == user_id,
                UserConsent.version == DISCLAIMER_VERSION,
            )
        ).scalar_one_or_none()

        if existing is not None:
            updated = False
            if existing.disclaimer_hash != DISCLAIMER_HASH:
                existing.disclaimer_hash = DISCLAIMER_HASH
                updated = True
            if existing.method != method:
                existing.method = method
                updated = True
            if updated:
                existing.consented_at = datetime.now(timezone.utc)
                session.commit()
            return False

        consent = UserConsent(
            guild_id=guild_id,
            discord_user_id=user_id,
            version=DISCLAIMER_VERSION,
            disclaimer_hash=DISCLAIMER_HASH,
            method=method,
            consented_at=datetime.now(timezone.utc),
        )
        session.add(consent)
        session.commit()

    return True
