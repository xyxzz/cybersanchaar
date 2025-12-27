#!/bin/bash

# Cybersanchaar Deployment Script for AWS + Nginx
# This script automates the deployment process

set -e  # Exit on any error

echo "🚀 Starting Cybersanchaar Deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration - UPDATE THESE!
DOMAIN_NAME="yourdomain.com"
APP_DIR="/home/ubuntu/cybersanchaar"
USER="ubuntu"

echo -e "${YELLOW}⚠️  Please make sure you've updated DOMAIN_NAME in this script!${NC}"
read -p "Press Enter to continue or Ctrl+C to cancel..."

# Step 1: Install system dependencies
echo -e "\n${GREEN}[1/9] Installing system dependencies...${NC}"
sudo apt update
sudo apt install -y nginx python3 python3-pip python3-venv certbot python3-certbot-nginx

# Step 2: Install Gunicorn in virtual environment
echo -e "\n${GREEN}[2/9] Installing Gunicorn...${NC}"
cd $APP_DIR
source news/bin/activate
pip install gunicorn
deactivate

# Step 3: Create logs directory if it doesn't exist
echo -e "\n${GREEN}[3/9] Setting up directories...${NC}"
mkdir -p $APP_DIR/logs
sudo chown -R $USER:www-data $APP_DIR

# Step 4: Copy and configure systemd service
echo -e "\n${GREEN}[4/9] Setting up systemd service...${NC}"
sudo cp $APP_DIR/cybersanchaar.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable cybersanchaar
sudo systemctl start cybersanchaar
sleep 2
sudo systemctl status cybersanchaar --no-pager

# Step 5: Configure Nginx
echo -e "\n${GREEN}[5/9] Configuring Nginx...${NC}"
sudo cp $APP_DIR/nginx_cybersanchaar.conf /etc/nginx/sites-available/cybersanchaar
sudo sed -i "s/yourdomain.com/$DOMAIN_NAME/g" /etc/nginx/sites-available/cybersanchaar
sudo ln -sf /etc/nginx/sites-available/cybersanchaar /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
sudo nginx -t

# Step 6: Restart Nginx
echo -e "\n${GREEN}[6/9] Restarting Nginx...${NC}"
sudo systemctl restart nginx
sudo systemctl enable nginx

# Step 7: Configure firewall
echo -e "\n${GREEN}[7/9] Configuring firewall...${NC}"
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
echo "y" | sudo ufw enable || true

# Step 8: Update config.yaml
echo -e "\n${GREEN}[8/9] Updating application configuration...${NC}"
cd $APP_DIR
sed -i 's/host: "127.0.0.1"/host: "0.0.0.0"/' config.yaml

# Step 9: Setup SSL (optional - requires DNS to be configured)
echo -e "\n${GREEN}[9/9] SSL Certificate Setup${NC}"
read -p "Do you want to set up SSL certificate now? (DNS must be configured first) [y/N]: " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    sudo certbot --nginx -d $DOMAIN_NAME -d www.$DOMAIN_NAME
fi

# Setup cron for news updates
echo -e "\n${GREEN}Setting up automated news updates...${NC}"
(crontab -l 2>/dev/null | grep -v "cybersanchaar"; echo "0 */6 * * * cd $APP_DIR && $APP_DIR/news/bin/python cyber_news_app.py --update >> $APP_DIR/logs/cron.log 2>&1") | crontab -

echo -e "\n${GREEN}✅ Deployment Complete!${NC}"
echo -e "\n${YELLOW}Next Steps:${NC}"
echo "1. Configure your domain's DNS A record to point to this server's IP"
echo "2. Wait 5-15 minutes for DNS propagation"
echo "3. Run: sudo certbot --nginx -d $DOMAIN_NAME -d www.$DOMAIN_NAME"
echo "4. Visit: http://$DOMAIN_NAME"
echo ""
echo -e "${YELLOW}Useful Commands:${NC}"
echo "  Check app status: sudo systemctl status cybersanchaar"
echo "  View app logs: journalctl -u cybersanchaar -f"
echo "  View nginx logs: sudo tail -f /var/log/nginx/cybersanchaar-error.log"
echo "  Restart app: sudo systemctl restart cybersanchaar"
echo "  Update news: cd $APP_DIR && source news/bin/activate && python cyber_news_app.py --update"
echo ""
echo -e "${GREEN}🎉 Happy Deploying!${NC}"

