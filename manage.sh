#!/bin/bash

# Terms and Conditions Bot Service Management Script
# This script helps manage the Discord bot service

PROJECT_DIR="/mnt/hedger/terms_and_conditions"
SERVICE_NAME="terms-and-conditions"
SERVICE_FILE="${SERVICE_NAME}.service"

cd "$PROJECT_DIR" || exit 1

case "$1" in
    install)
        echo "Installing Terms and Conditions bot service..."
        
        # Copy service file to systemd directory
        sudo cp "$SERVICE_FILE" "/etc/systemd/system/"
        
        # Reload systemd daemon
        sudo systemctl daemon-reload
        
        # Enable the service to start on boot
        sudo systemctl enable "$SERVICE_NAME"
        
        echo "Service installed and enabled for auto-start on boot"
        echo "Use './manage.sh start' to start the service now"
        ;;
    
    start)
        echo "Starting Terms and Conditions bot..."
        sudo systemctl start "$SERVICE_NAME"
        echo "Bot started"
        ;;
    
    stop)
        echo "Stopping Terms and Conditions bot..."
        sudo systemctl stop "$SERVICE_NAME"
        echo "Bot stopped"
        ;;
    
    restart)
        echo "Restarting Terms and Conditions bot..."
        sudo systemctl restart "$SERVICE_NAME"
        echo "Bot restarted"
        ;;
    
    status)
        echo "Terms and Conditions bot status:"
        sudo systemctl status "$SERVICE_NAME"
        ;;
    
    logs)
        echo "Terms and Conditions bot logs:"
        sudo journalctl -u "$SERVICE_NAME" -f
        ;;
    
    logs-tail)
        echo "Last 50 lines of Terms and Conditions bot logs:"
        sudo journalctl -u "$SERVICE_NAME" -n 50
        ;;
    
    uninstall)
        echo "Uninstalling Terms and Conditions bot service..."
        sudo systemctl stop "$SERVICE_NAME" 2>/dev/null
        sudo systemctl disable "$SERVICE_NAME" 2>/dev/null
        sudo rm -f "/etc/systemd/system/$SERVICE_FILE"
        sudo systemctl daemon-reload
        echo "Service uninstalled"
        ;;
    
    *)
        echo "Usage: $0 {install|start|stop|restart|status|logs|logs-tail|uninstall}"
        echo ""
        echo "Commands:"
        echo "  install    - Install service and enable auto-start on boot"
        echo "  start      - Start the bot service"
        echo "  stop       - Stop the bot service"
        echo "  restart    - Restart the bot service"
        echo "  status     - Show service status"
        echo "  logs       - Show live logs"
        echo "  logs-tail  - Show last 50 log lines"
        echo "  uninstall  - Remove service and disable auto-start"
        exit 1
        ;;
esac