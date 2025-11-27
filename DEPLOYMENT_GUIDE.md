# 🚀 AWS Ubuntu Deployment Guide

Complete guide to deploy Cybersanchaar on AWS Ubuntu instance with Nginx + Gunicorn.

## 📋 Prerequisites

- AWS EC2 instance with Ubuntu 20.04 or 22.04
- Domain name (optional, but recommended for SSL)
- SSH access to your instance

## 🔧 AWS Security Group Configuration

Configure your EC2 Security Group to allow:

| Type | Protocol | Port | Source |
|------|----------|------|--------|
| SSH | TCP | 22 | Your IP |
| HTTP | TCP | 80 | 0.0.0.0/0 |
| HTTPS | TCP | 443 | 0.0.0.0/0 |

## 📦 Step-by-Step Deployment

### 1️⃣ Connect to Your Instance

```bash
ssh -i your-key.pem ubuntu@your-instance-ip
```

### 2️⃣ Upload Your Code

**Option A: Using SCP (from your local machine)**
```bash
scp -i your-key.pem -r D:\cybersanchaar\cybersanchaar ubuntu@your-instance-ip:~/
```

**Option B: Using Git**
```bash
cd ~
git clone your-repository-url cybersanchaar
cd cybersanchaar
```

### 3️⃣ Run the Automated Deployment Script

```bash
cd ~/cybersanchaar
chmod +x deploy.sh

# Edit the script to set your domain name
nano deploy.sh
# Change: DOMAIN_NAME="yourdomain.com"

# Run the deployment
./deploy.sh
```

The script will automatically:
- ✅ Install system dependencies (Python, Nginx, Certbot)
- ✅ Install Gunicorn in virtual environment
- ✅ Set up systemd service
- ✅ Configure Nginx reverse proxy
- ✅ Configure firewall (UFW)
- ✅ Set up automated news updates (cron)

### 4️⃣ Manual Setup (Alternative to Script)

If you prefer manual setup:

#### Install Dependencies
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y nginx python3 python3-pip python3-venv
```

#### Set Up Virtual Environment
```bash
cd ~/cybersanchaar
python3 -m venv news
source news/bin/activate
pip install -r requirements.txt
pip install gunicorn
deactivate
```

#### Create Directories
```bash
mkdir -p ~/cybersanchaar/logs ~/cybersanchaar/data ~/cybersanchaar/cache
```

#### Copy and Enable Systemd Service
```bash
sudo cp cybersanchaar.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable cybersanchaar
sudo systemctl start cybersanchaar
sudo systemctl status cybersanchaar
```

#### Configure Nginx
```bash
# Copy Nginx configuration
sudo cp nginx_cybersanchaar.conf /etc/nginx/sites-available/cybersanchaar

# Update domain name
sudo sed -i 's/yourdomain.com/your-actual-domain.com/g' /etc/nginx/sites-available/cybersanchaar

# Enable the site
sudo ln -s /etc/nginx/sites-available/cybersanchaar /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default

# Test and restart Nginx
sudo nginx -t
sudo systemctl restart nginx
```

#### Set Up Cron for Automated Updates
```bash
crontab -e
# Add this line:
0 */6 * * * cd /home/ubuntu/cybersanchaar && /home/ubuntu/cybersanchaar/news/bin/python cyber_news_app.py --update >> /home/ubuntu/cybersanchaar/logs/cron.log 2>&1
```

### 5️⃣ SSL Certificate (Optional but Recommended)

**Prerequisites:**
- Domain DNS A record pointing to your server's IP
- Wait 5-15 minutes for DNS propagation

```bash
# Install Certbot if not already installed
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal is set up automatically
sudo certbot renew --dry-run
```

## 🔍 Verification

### Check Application Status
```bash
sudo systemctl status cybersanchaar
```

### View Application Logs
```bash
# Real-time logs
journalctl -u cybersanchaar -f

# Gunicorn logs
tail -f ~/cybersanchaar/logs/gunicorn-error.log
tail -f ~/cybersanchaar/logs/gunicorn-access.log
```

### View Nginx Logs
```bash
sudo tail -f /var/log/nginx/cybersanchaar-access.log
sudo tail -f /var/log/nginx/cybersanchaar-error.log
```

### Test the Application
```bash
# Test locally
curl http://localhost/api/sources

# Test from browser
http://your-domain.com
# or
http://your-server-ip
```

## 🛠️ Common Commands

### Application Management
```bash
# Restart application
sudo systemctl restart cybersanchaar

# Stop application
sudo systemctl stop cybersanchaar

# Start application
sudo systemctl start cybersanchaar

# View status
sudo systemctl status cybersanchaar
```

### Nginx Management
```bash
# Restart Nginx
sudo systemctl restart nginx

# Test Nginx configuration
sudo nginx -t

# Reload Nginx (no downtime)
sudo systemctl reload nginx
```

### Manual News Update
```bash
cd ~/cybersanchaar
source news/bin/activate
python cyber_news_app.py --update
deactivate
```

### View News via CLI
```bash
cd ~/cybersanchaar
source news/bin/activate
python cyber_news_app.py --show --days 1
deactivate
```

## 🐛 Troubleshooting

### Application Won't Start
```bash
# Check logs
journalctl -u cybersanchaar -n 50

# Check if socket file exists
ls -la ~/cybersanchaar/cybersanchaar.sock

# Check if virtual environment works
source ~/cybersanchaar/news/bin/activate
python -c "from src.web_interface import create_app; print('OK')"
```

### Nginx 502 Bad Gateway
```bash
# Check if Gunicorn is running
sudo systemctl status cybersanchaar

# Check socket permissions
ls -la ~/cybersanchaar/cybersanchaar.sock

# Check Nginx error logs
sudo tail -f /var/log/nginx/cybersanchaar-error.log
```

### No Articles Showing
```bash
# Manually update news
cd ~/cybersanchaar
source news/bin/activate
python cyber_news_app.py --update
python cyber_news_app.py --show

# Check if data directory has files
ls -la ~/cybersanchaar/cache/
```

### Port Already in Use
```bash
# Find process using port 5000
sudo lsof -i :5000

# Kill the process (use PID from above)
sudo kill -9 <PID>
```

## 📊 Performance Optimization

### Increase Gunicorn Workers
Edit `cybersanchaar.service`:
```bash
sudo nano /etc/systemd/system/cybersanchaar.service

# Change --workers based on CPU cores (2-4 × CPU cores)
--workers 4

# Reload
sudo systemctl daemon-reload
sudo systemctl restart cybersanchaar
```

### Enable Nginx Caching
Add to `nginx_cybersanchaar.conf`:
```nginx
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m max_size=1g inactive=60m;

location /api/news {
    proxy_cache my_cache;
    proxy_cache_valid 200 5m;
    proxy_pass http://unix:/home/ubuntu/cybersanchaar/cybersanchaar.sock;
}
```

## 🔄 Updating the Application

```bash
cd ~/cybersanchaar

# Pull latest changes
git pull origin main

# Activate virtual environment
source news/bin/activate

# Update dependencies
pip install -r requirements.txt

# Deactivate
deactivate

# Restart application
sudo systemctl restart cybersanchaar
```

## 🔒 Security Best Practices

1. **Keep system updated:**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **Enable firewall:**
   ```bash
   sudo ufw allow 22/tcp
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw enable
   ```

3. **Use SSL certificate** (Let's Encrypt)

4. **Disable debug mode** in `config.yaml`:
   ```yaml
   web:
     debug: false
   ```

5. **Change Flask secret key** in `src/web_interface.py`:
   ```python
   app.config['SECRET_KEY'] = 'your-random-secret-key-here'
   ```

6. **Set up regular backups:**
   ```bash
   # Backup script
   tar -czf backup-$(date +%Y%m%d).tar.gz ~/cybersanchaar/cache ~/cybersanchaar/logs ~/cybersanchaar/config.yaml
   ```

## 📞 Support

### Check Application Health
```bash
# System resources
htop

# Disk usage
df -h

# Memory usage
free -h

# Application status
sudo systemctl status cybersanchaar nginx
```

### Useful API Endpoints
- `http://your-domain/` - Web interface
- `http://your-domain/api/news` - Get news articles
- `http://your-domain/api/sources` - List sources
- `http://your-domain/api/statistics` - Get statistics
- `http://your-domain/api/update` - Trigger news update

## 🎉 Success!

Once deployed, your application will be:
- ✅ Running 24/7 with auto-restart on failure
- ✅ Accessible via your domain (with SSL)
- ✅ Automatically updating news every 6 hours
- ✅ Logging all activity for debugging
- ✅ Protected by Nginx with security headers

**Visit:** `https://yourdomain.com`

---

**Happy Deploying! 🚀🔒**

