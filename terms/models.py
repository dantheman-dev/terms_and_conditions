from datetime import datetime

from sqlalchemy import DateTime, Integer, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class UserConsent(Base):
    __tablename__ = "user_consents"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    guild_id: Mapped[str] = mapped_column(String, index=True)
    discord_user_id: Mapped[str] = mapped_column(String, index=True)
    version: Mapped[str] = mapped_column(String)
    disclaimer_hash: Mapped[str] = mapped_column(String)
    method: Mapped[str] = mapped_column(String)  # dm_button | channel_button | slash_start
    consented_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    __table_args__ = (UniqueConstraint("guild_id", "discord_user_id", "version", name="uq_consent_user_version"),)

class ConsentDisplay(Base):
    __tablename__ = "consent_displays"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    guild_id: Mapped[str] = mapped_column(String, index=True)
    discord_user_id: Mapped[str] = mapped_column(String, index=True)
    command: Mapped[str] = mapped_column(String)  # e.g., "start"
    displayed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    disclaimer_hash: Mapped[str] = mapped_column(String)
