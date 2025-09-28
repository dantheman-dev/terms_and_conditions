from datetime import datetime, timezone
from sqlalchemy.exc import IntegrityError

from terms.db import Session
from terms.models import UserConsent
from terms.constants import DISCLAIMER_VERSION, DISCLAIMER_HASH

def record_consent(guild_id: int, user_id: int, method: str) -> bool:
    """Persist a consent decision, returning True if a new row was created."""

    consent = UserConsent(
        guild_id=str(guild_id),
        discord_user_id=str(user_id),
        version=DISCLAIMER_VERSION,
        disclaimer_hash=DISCLAIMER_HASH,
        method=method,
        consented_at=datetime.now(timezone.utc),
    )

    with Session() as session:
        session.add(consent)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            return False

    return True
