from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from terms.db import Session
from terms.models import UserConsent, ConsentDisplay
from terms.constants import DISCLAIMER_VERSION, DISCLAIMER_HASH

def has_active_consent(guild_id: int, user_id: int, *, session=None) -> bool:
    """Return True if the user already consented to the current disclaimer."""

    stmt = (
        select(UserConsent.id)
        .filter_by(guild_id=str(guild_id), discord_user_id=str(user_id), version=DISCLAIMER_VERSION)
        .limit(1)
    )

    owns_session = session is None
    if owns_session:
        session = Session()

    try:
        return session.execute(stmt).scalar_one_or_none() is not None
    finally:
        if owns_session:
            session.close()

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
        if has_active_consent(guild_id, user_id, session=session):
            return False

        session.add(consent)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            return False

    return True

def record_display(guild_id: int, user_id: int, command: str) -> None:
    with Session() as s, s.begin():
        s.add(ConsentDisplay(
            guild_id=str(guild_id),
            discord_user_id=str(user_id),
            command=command,
            displayed_at=datetime.now(timezone.utc),
            disclaimer_hash=DISCLAIMER_HASH,
        ))
