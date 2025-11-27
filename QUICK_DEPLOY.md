# ⚡ Quick Deploy Cheat Sheet

## 🚀 One-Command Deployment

```bash
# 1. SSH into your AWS Ubuntu instance
ssh -i your-key.pem ubuntu@your-instance-ip

# 2. Upload code (from your local machine)
scp -i your-key.pem -r D:\cybersanchaar\cybersanchaar ubuntu@your-instance-ip:~/

# 3. Run deployment script (on the server)
cd ~/cybersanchaar
chmod +x deploy.sh
nano deploy.sh  # Update DOMAIN_NAME
./deploy.sh
```

## 📋 Pre-Deployment Checklist

- [ ] AWS Security Group allows ports: 22, 80, 443
- [ ] Domain DNS A record points to server IP (if using domain)
- [ ] Updated `DOMAIN_NAME` in `deploy.sh`
- [ ] Config.yaml has `host: "0.0.0.0"`

## 🔧 Essential Commands

### Check Status
```bash
sudo systemctl status cybersanchaar  # App status
sudo systemctl status nginx          # Nginx status
curl http://localhost/api/sources    # Test locally
```

### View Logs
```bash
journalctl -u cybersanchaar -f                      # App logs (live)
tail -f ~/cybersanchaar/logs/gunicorn-error.log     # Gunicorn errors
sudo tail -f /var/log/nginx/cybersanchaar-error.log # Nginx errors
```

### Restart Services
```bash
sudo systemctl restart cybersanchaar  # Restart app
sudo systemctl restart nginx          # Restart Nginx
```

### Update News Manually
```bash
cd ~/cybersanchaar
source news/bin/activate
python cyber_news_app.py --update
python cyber_news_app.py --show
```

## 🐛 Quick Fixes

### 502 Bad Gateway?
```bash
sudo systemctl restart cybersanchaar
sudo systemctl status cybersanchaar
```

### No Articles?
```bash
cd ~/cybersanchaar
source news/bin/activate
python cyber_news_app.py --update
```

### Can't Access from Browser?
```bash
# Check AWS Security Group (ports 80, 443)
# Check firewall
sudo ufw status
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

## 🔐 SSL Setup (After DNS Propagation)

```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

## 📱 Access Your App

- Web Interface: `http://your-domain.com` or `http://your-ip`
- API Docs: `http://your-domain.com/api/news`
- Update News: `http://your-domain.com/api/update`

## ✅ Verify Everything Works

```bash
# 1. App is running
sudo systemctl is-active cybersanchaar

# 2. Nginx is running
sudo systemctl is-active nginx

# 3. Socket exists
ls -la ~/cybersanchaar/cybersanchaar.sock

# 4. API works
curl http://localhost/api/sources | jq

# 5. Cron is set
crontab -l | grep cybersanchaar
```

## 🆘 Emergency Commands

```bash
# Complete restart
sudo systemctl restart cybersanchaar nginx

# View recent errors
journalctl -u cybersanchaar -n 50 --no-pager

# Check what's using port 80
sudo lsof -i :80

# Restart everything from scratch
sudo systemctl stop cybersanchaar
sudo systemctl start cybersanchaar
sudo systemctl restart nginx
```

---

**That's it! You're deployed! 🎉**

