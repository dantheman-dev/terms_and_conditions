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

## Production Deployment (Auto-start on boot)

### Install as systemd service:
```bash
./manage.sh install    # Install and enable auto-start
./manage.sh start      # Start the service
./manage.sh status     # Check status
./manage.sh logs       # View live logs
```

### Ecosystem management (with Xedge):
```bash
/mnt/hedger/xedge-ecosystem.sh install-all   # Install both services
/mnt/hedger/xedge-ecosystem.sh start-all     # Start both services
/mnt/hedger/xedge-ecosystem.sh status-all    # Check both services
```

See [SERVICE_SETUP.md](SERVICE_SETUP.md) for detailed service management instructions.

## Verification notes

- DM button consent flow: trigger `/start` in a DM or click the consent button from a DM card. Confirm the bot logs `interaction.dm_button_resolved` and that the consent response is delivered via DM.
