# Terms & Conditions Bot - Service Setup

This document explains how to set up the Terms & Conditions Discord bot to start automatically on boot and persist after system restarts.

## Quick Setup

1. **Install the service:**
   ```bash
   cd /mnt/hedger/terms_and_conditions
   ./manage.sh install
   ```

2. **Start the service:**
   ```bash
   ./manage.sh start
   ```

3. **Check status:**
   ```bash
   ./manage.sh status
   ```

## Service Management Commands

| Command | Description |
|---------|-------------|
| `./manage.sh install` | Install service and enable auto-start on boot |
| `./manage.sh start` | Start the bot service |
| `./manage.sh stop` | Stop the bot service |
| `./manage.sh restart` | Restart the bot service |
| `./manage.sh status` | Show service status |
| `./manage.sh logs` | Show live logs (Ctrl+C to exit) |
| `./manage.sh logs-tail` | Show last 50 log lines |
| `./manage.sh uninstall` | Remove service and disable auto-start |

## Ecosystem Management

For managing both Terms & Conditions and Xedge together:

```bash
# From anywhere on the system
/mnt/hedger/xedge-ecosystem.sh install-all   # Install both services
/mnt/hedger/xedge-ecosystem.sh start-all     # Start both services
/mnt/hedger/xedge-ecosystem.sh stop-all      # Stop both services
/mnt/hedger/xedge-ecosystem.sh status-all    # Check both services
```
## Service Details

- **Service Name:** `terms-and-conditions`
- **User:** `vega`
- **Working Directory:** `/mnt/hedger/terms_and_conditions`
- **Python Environment:** Uses the local `.venv` virtual environment
- **Auto-restart:** Yes (10-second delay on failure)
- **Logs:** Available via `journalctl` and the management script

## Boot Behavior

Once installed with `./manage.sh install`, the bot will:
- ✅ Start automatically when the system boots
- ✅ Restart automatically if it crashes
- ✅ Use the correct virtual environment
- ✅ Log all output to the system journal

## Troubleshooting

### Check if service is running:
```bash
./manage.sh status
```

### View recent logs:
```bash
./manage.sh logs-tail
```

### View live logs:
```bash
./manage.sh logs
```

### Manual restart:
```bash
./manage.sh restart
```

### Check systemd service directly:
```bash
sudo systemctl status terms-and-conditions
```

## Security Features

The service runs with restricted permissions:
- No new privileges allowed
- Private temporary directory
- Protected system directories
- Read-only access except to the project directory

## Integration with Xedge

The Terms & Conditions bot acts as a gatekeeper for the Xedge betting analysis tools. Users must consent to risk disclaimers before receiving the "Sharps" role that grants access to Xedge features.

**Startup Order:**
1. Terms & Conditions bot starts first (gatekeeper)
2. Xedge services start after (protected resources)

This ensures that role-based access control is active before any betting analysis tools become available.