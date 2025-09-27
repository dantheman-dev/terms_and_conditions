# terms_and_conditions — Consent-Gating Bot for Xedge

Grants/removes the **Sharps** role after explicit user consent and records a signed consent row
(user, guild, disclaimer version+hash, timestamp, method). Single slash command: **/start**.

- DM consent card on join; fallback: `/start` shows an ephemeral consent card.
- **I Agree** → writes `user_consents` and grants Sharps.
- **Decline** → removes Sharps and denies.
- Bump `DISCLAIMER_VERSION` to force re-consent.

## Quick start
1. Create Discord app → Add Bot → enable **Server Members Intent**.
2. OAuth scopes: `bot`, `applications.commands`; permissions: **Manage Roles**, **Send Messages**, **View Channels**.
3. Invite the bot; move its role **above** `Sharps`.
4. Fill `.env` with token + guild id.
5. `python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
6. `python bot.py` to run in foreground.

## Systemd
See service section in the guide.
