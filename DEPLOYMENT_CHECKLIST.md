# 📋 Deployment Checklist

Use this checklist to track your deployment progress.

## Pre-Deployment Setup

- [ ] AWS EC2 instance is running and accessible
- [ ] SSH access configured with key pair
- [ ] Domain name purchased and accessible
- [ ] Repository cloned to server
- [ ] Python 3 installed
- [ ] Virtual environment created (`python3 -m venv news`)
- [ ] Requirements installed (`pip install -r requirements.txt`)

## System Configuration

- [ ] System packages updated (`sudo apt update && sudo apt upgrade`)
- [ ] Nginx installed (`sudo apt install nginx`)
- [ ] Certbot installed (`sudo apt install certbot python3-certbot-nginx`)
- [ ] Gunicorn installed in venv (`pip install gunicorn`)

## Application Setup

- [ ] `wsgi.py` file exists in project root
- [ ] `config.yaml` updated (host: "0.0.0.0")
- [ ] Logs directory exists (`mkdir -p logs`)
- [ ] File permissions set (`sudo chown -R ubuntu:www-data /path/to/app`)

## Systemd Service

- [ ] `cybersanchaar.service` file created
- [ ] Service file paths updated for your environment
- [ ] Service copied to `/etc/systemd/system/`
- [ ] Service enabled (`sudo systemctl enable cybersanchaar`)
- [ ] Service started (`sudo systemctl start cybersanchaar`)
- [ ] Service running without errors (`sudo systemctl status cybersanchaar`)

## Nginx Configuration

- [ ] `nginx_cybersanchaar.conf` created
- [ ] Domain name updated in Nginx config
- [ ] Socket path verified in Nginx config
- [ ] Config copied to `/etc/nginx/sites-available/`
- [ ] Symlink created in `/etc/nginx/sites-enabled/`
- [ ] Default site disabled (if needed)
- [ ] Nginx config tested (`sudo nginx -t`)
- [ ] Nginx restarted (`sudo systemctl restart nginx`)

## AWS Security Configuration

- [ ] Security Group configured with inbound rules:
  - [ ] HTTP (Port 80) from 0.0.0.0/0
  - [ ] HTTPS (Port 443) from 0.0.0.0/0
  - [ ] SSH (Port 22) from your IP only
- [ ] Instance has a public IP address
- [ ] Public IP is not changing (Elastic IP recommended)

## DNS Configuration

- [ ] A Record created: `@` → EC2 Public IP
- [ ] CNAME Record created: `www` → your domain
- [ ] DNS propagation completed (5-15 minutes)
- [ ] Domain resolves correctly (`nslookup yourdomain.com`)

## SSL Certificate

- [ ] Certbot run for your domain
- [ ] Certificate installed successfully
- [ ] Auto-renewal configured
- [ ] Auto-renewal tested (`sudo certbot renew --dry-run`)
- [ ] HTTP redirects to HTTPS

## Testing & Verification

- [ ] Application accessible via HTTP
- [ ] Application accessible via HTTPS
- [ ] API endpoints working (`/api/news`, `/api/sources`)
- [ ] No 502/503 errors
- [ ] Logs show no errors
- [ ] News updates working (`python cyber_news_app.py --update`)

## Optional Features

- [ ] Cron job for automatic news updates
- [ ] UFW firewall configured and enabled
- [ ] Log rotation configured
- [ ] Monitoring setup (optional)
- [ ] Backup strategy implemented

## Post-Deployment

- [ ] Admin email configured for SSL renewal notifications
- [ ] Application password/secrets secured
- [ ] SSH key-based authentication enforced
- [ ] Regular update schedule planned
- [ ] Backup schedule established
- [ ] Documentation updated with your specific details

## Testing Commands to Run

```bash
# 1. Check service status
sudo systemctl status cybersanchaar
sudo systemctl status nginx

# 2. Check if socket exists
ls -la /home/ubuntu/cybersanchaar-master/cybersanchaar.sock

# 3. Test from localhost
curl http://localhost

# 4. Test from domain
curl http://yourdomain.com
curl https://yourdomain.com

# 5. Test API endpoints
curl https://yourdomain.com/api/sources
curl https://yourdomain.com/api/news?days=1

# 6. Check DNS
nslookup yourdomain.com
dig yourdomain.com

# 7. Check SSL
sudo certbot certificates

# 8. View logs
journalctl -u cybersanchaar -n 50
sudo tail -50 /var/log/nginx/cybersanchaar-error.log
```

## Common Issues to Check

If something isn't working, verify:

1. **Service Issues**
   - [ ] Gunicorn is running
   - [ ] No port conflicts
   - [ ] Virtual environment is activated in service
   - [ ] Python path is correct

2. **Nginx Issues**
   - [ ] Nginx syntax is valid
   - [ ] Socket path matches service config
   - [ ] File permissions are correct
   - [ ] Port 80/443 are not blocked

3. **Network Issues**
   - [ ] AWS Security Group allows traffic
   - [ ] UFW allows traffic (if enabled)
   - [ ] DNS points to correct IP
   - [ ] No firewall blocking requests

4. **SSL Issues**
   - [ ] Domain is accessible before running certbot
   - [ ] Ports 80 and 443 are open
   - [ ] Certificate is not expired

## Success Criteria

Your deployment is successful when:

✅ Website loads at https://yourdomain.com  
✅ API returns data at /api/news  
✅ SSL certificate shows valid and secure  
✅ Services auto-start on reboot  
✅ News updates are fetching correctly  
✅ No errors in logs  

---

## Need Help?

If you're stuck on any step:

1. Check the detailed guide: `deployment_guide.md`
2. See quick reference: `QUICK_DEPLOY_REFERENCE.md`
3. Review application logs: `tail -f logs/gunicorn-error.log`
4. Check system logs: `journalctl -u cybersanchaar -f`

---

**Remember**: Most issues are due to:
- Incorrect file paths in configs
- Wrong file permissions
- Firewall/security group blocking traffic
- DNS not propagated yet

Take your time with each step and verify it works before moving to the next! 🚀


