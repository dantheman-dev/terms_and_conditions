"""Application configuration helpers."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Final

from dotenv import load_dotenv


class Settings:
    """Lightweight settings loader for the Discord bot.

    The original project used :mod:`pydantic_settings`, but the production
    service failed to start because that optional dependency was missing.
    Instead of relying on that package, we eagerly load the ``.env`` file once
    and expose strongly-typed attributes.  This keeps configuration simple and
    avoids runtime import errors while remaining easy to understand and extend.
    """

    _ENV_FILE: Final[str] = ".env"
    _ENV_LOADED: bool = False

    def __init__(self) -> None:
        self._ensure_env_loaded()

        self.DISCORD_TOKEN: str = self._require("DISCORD_TOKEN")
        self.GUILD_ID: int = self._require_int("GUILD_ID")
        self.SHARPS_ROLE_NAME: str = os.getenv("SHARPS_ROLE_NAME", "Sharps")
        self.DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./consent.db")
        self.LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    @classmethod
    def _ensure_env_loaded(cls) -> None:
        if cls._ENV_LOADED:
            return

        env_path = Path(__file__).resolve().parent.parent / cls._ENV_FILE
        load_dotenv(env_path)
        cls._ENV_LOADED = True

    @staticmethod
    def _require(key: str) -> str:
        value = os.getenv(key)
        if value:
            return value
        raise RuntimeError(f"Missing required configuration value: {key}")

    @classmethod
    def _require_int(cls, key: str) -> int:
        raw = cls._require(key)
        try:
            return int(raw)
        except ValueError as exc:  # pragma: no cover - defensive programming
            raise RuntimeError(f"Expected integer value for {key!r}") from exc


__all__ = ["Settings"]

