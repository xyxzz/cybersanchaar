# Quick Deployment Reference

## 🚀 Fast Track Deployment (TL;DR)

### Prerequisites Check
- [ ] AWS EC2 instance running
- [ ] SSH access to instance
- [ ] Domain name purchased
- [ ] Repository cloned to `/home/ubuntu/cybersanchaar-master`
- [ ] Virtual environment created and requirements installed

### Quick Commands

```bash
# 1. SSH into your AWS instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# 2. Navigate to project directory
cd /home/ubuntu/cybersanchaar-master

# 3. Make deploy script executable and run it
chmod +x deploy.sh
./deploy.sh

# 4. Configure DNS (in your domain registrar)
# A Record: @ -> Your EC2 Public IP
# CNAME Record: www -> yourdomain.com

# 5. Wait 5-15 minutes for DNS propagation, then setup SSL
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

---

## Manual Deployment (Step by Step)

### 1. Install Dependencies
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install nginx python3 python3-pip python3-venv certbot python3-certbot-nginx -y
```

### 2. Setup Gunicorn
```bash
cd /home/ubuntu/cybersanchaar-master
source news/bin/activate
pip install gunicorn
```

### 3. Copy Service File
```bash
sudo cp cybersanchaar.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable cybersanchaar
sudo systemctl start cybersanchaar
```

### 4. Setup Nginx
```bash
# Edit nginx config and replace yourdomain.com with your actual domain
sudo nano nginx_cybersanchaar.conf

# Copy to Nginx sites
sudo cp nginx_cybersanchaar.conf /etc/nginx/sites-available/cybersanchaar
sudo ln -s /etc/nginx/sites-available/cybersanchaar /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 5. Configure AWS Security Group
Add inbound rules in AWS Console:
- HTTP (80) from 0.0.0.0/0
- HTTPS (443) from 0.0.0.0/0
- SSH (22) from Your IP

### 6. Configure DNS
In your domain registrar:
- **A Record**: `@` → Your EC2 Public IP
- **CNAME Record**: `www` → `yourdomain.com`

### 7. Setup SSL
```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

---

## Essential Commands

### Check Status
```bash
# Application status
sudo systemctl status cybersanchaar

# Nginx status
sudo systemctl status nginx

# View logs
journalctl -u cybersanchaar -f
sudo tail -f /var/log/nginx/cybersanchaar-error.log
```

### Restart Services
```bash
sudo systemctl restart cybersanchaar
sudo systemctl restart nginx
```

### Update Application
```bash
cd /home/ubuntu/cybersanchaar-master
git pull
source news/bin/activate
pip install -r requirements.txt
sudo systemctl restart cybersanchaar
```

### Update News Manually
```bash
cd /home/ubuntu/cybersanchaar-master
source news/bin/activate
python cyber_news_app.py --update
```

---

## File Locations

| Purpose | Path |
|---------|------|
| Application | `/home/ubuntu/cybersanchaar-master/` |
| Systemd Service | `/etc/systemd/system/cybersanchaar.service` |
| Nginx Config | `/etc/nginx/sites-available/cybersanchaar` |
| App Logs | `/home/ubuntu/cybersanchaar-master/logs/` |
| Nginx Logs | `/var/log/nginx/cybersanchaar-*.log` |
| SSL Certificates | `/etc/letsencrypt/live/yourdomain.com/` |

---

## Troubleshooting Quick Fixes

### 502 Bad Gateway
```bash
sudo systemctl restart cybersanchaar
sudo systemctl restart nginx
```

### Service Won't Start
```bash
journalctl -u cybersanchaar -n 50
sudo chown -R ubuntu:www-data /home/ubuntu/cybersanchaar-master
sudo systemctl restart cybersanchaar
```

### SSL Issues
```bash
sudo certbot renew
sudo certbot certificates
```

### Can't Access Website
1. Check AWS Security Group rules
2. Verify DNS: `nslookup yourdomain.com`
3. Check firewall: `sudo ufw status`
4. Check Nginx: `sudo nginx -t`

---

## Performance Tips

### Adjust Workers (based on CPU cores)
Edit `/etc/systemd/system/cybersanchaar.service`:
```ini
# Change --workers based on: (2 × CPU_cores) + 1
--workers 5 \  # for 2 CPU cores
```

### Monitor Resources
```bash
# CPU and Memory
htop

# Disk usage
df -h

# Application performance
sudo tail -f /home/ubuntu/cybersanchaar-master/logs/gunicorn-access.log
```

---

## Backup Commands

```bash
# Backup configuration
tar -czf cybersanchaar-backup-$(date +%Y%m%d).tar.gz \
  config.yaml \
  logs/ \
  cache/ \
  data/

# Restore from backup
tar -xzf cybersanchaar-backup-YYYYMMDD.tar.gz
```

---

## Security Checklist

- [ ] UFW firewall enabled
- [ ] SSH key-based authentication only
- [ ] SSL certificate installed and auto-renewal enabled
- [ ] Debug mode disabled in config.yaml
- [ ] Regular system updates scheduled
- [ ] Strong passwords/keys used
- [ ] Backup strategy in place

---

## Support & Resources

- **Full Guide**: See `deployment_guide.md`
- **Application README**: See `README.md`
- **Logs Location**: `/home/ubuntu/cybersanchaar-master/logs/`
- **Nginx Docs**: https://nginx.org/en/docs/
- **Let's Encrypt**: https://letsencrypt.org/docs/

---

**Need Help?** Check logs first:
```bash
journalctl -u cybersanchaar -n 100
sudo tail -100 /var/log/nginx/cybersanchaar-error.log
```


