# 🔒 Cybersecurity News App - Usage Examples

## Getting Started

```bash
# Always activate the virtual environment first
source news/bin/activate

# Get help
python cyber_news_app.py --help
```

## Daily Usage

### 1. Morning News Routine
```bash
# Update and view today's top cybersecurity news
python cyber_news_app.py --update
python cyber_news_app.py
```

### 2. Focused Research
```bash
# Look for specific threats
python cyber_news_app.py --show --categories threats vulnerabilities --days 3

# Focus on specific sources
python cyber_news_app.py --show --sources "Krebs" "SANS" --days 2

# High-priority alerts only (shows articles with score > 15)
python cyber_news_app.py --show --days 1 | grep "Priority Score"
```

### 3. Weekly Analysis
```bash
# View statistics for the week
python cyber_news_app.py --stats

# Export week's data for analysis
python cyber_news_app.py --export json --days 7
python cyber_news_app.py --export csv --days 7
```

## Advanced Usage

### 1. Web Interface
```bash
# Start the web server
python cyber_news_app.py --web

# Then visit: http://localhost:5000
# Features:
# - Interactive filtering
# - Real-time updates
# - Export functionality
# - Mobile-responsive design
```

### 2. Automated Updates
```bash
# Run as daemon with scheduled updates (6 AM, 12 PM, 6 PM)
python cyber_news_app.py --daemon

# Check scheduler status
python cyber_news_app.py --schedule-status
```

### 3. API Integration
```bash
# Use curl to interact with the API when web server is running
curl "http://localhost:5000/api/news?days=1&categories=threats"
curl "http://localhost:5000/api/sources"
curl "http://localhost:5000/api/update"
curl "http://localhost:5000/api/statistics"
```

## Real Examples from Today's Run

### Sample Output
```
📰 Today's Cybersecurity News (15 articles)

1. 🔥 FreePBX Servers Targeted by Zero-Day Flaw, Emergency Patch Now Available
📌 The Hacker News • 2025-08-29 09:44 • #general
💬 The Sangoma FreePBX Security Team has issued an advisory warning...
🏷️  Keywords: zero-day, vulnerability, exploit
⚡ Priority Score: 35

2. 🔥 Storm-0501 Exploits Entra ID to Exfiltrate and Delete Azure Data
📌 The Hacker News • 2025-08-27 19:04 • #general
💬 The financially motivated threat actor known as Storm-0501...
🏷️  Keywords: ransomware, exploit, malware
⚡ Priority Score: 35
```

### Filtering Examples
```bash
# Show only vulnerability news
python cyber_news_app.py --show --categories vulnerabilities

# Show only high-priority threats from last 3 days
python cyber_news_app.py --show --days 3 | grep -A 10 "Priority Score: [2-9][0-9]"

# Show news from specific trusted sources
python cyber_news_app.py --show --sources "Krebs on Security" "SANS"
```

## Automation Ideas

### 1. Daily Email Summary
```bash
#!/bin/bash
# daily_summary.sh
source news/bin/activate
python cyber_news_app.py --update > /dev/null 2>&1
python cyber_news_app.py --show --days 1 | mail -s "Daily Cyber News" your-email@domain.com
```

### 2. Slack Integration
```bash
#!/bin/bash
# slack_notify.sh - Post high-priority news to Slack
source news/bin/activate
HIGH_PRIORITY=$(python cyber_news_app.py --show --days 1 | grep -A 5 "Priority Score: [2-9][0-9]")
if [ ! -z "$HIGH_PRIORITY" ]; then
    curl -X POST -H 'Content-type: application/json' \
    --data "{\"text\":\"🚨 High Priority Cyber News:\n$HIGH_PRIORITY\"}" \
    YOUR_SLACK_WEBHOOK_URL
fi
```

### 3. Continuous Monitoring
```bash
#!/bin/bash
# monitor.sh - Check for zero-day mentions every hour
while true; do
    source news/bin/activate
    python cyber_news_app.py --update > /dev/null 2>&1
    ZERO_DAYS=$(python cyber_news_app.py --show --days 1 | grep -i "zero-day")
    if [ ! -z "$ZERO_DAYS" ]; then
        echo "🚨 ZERO-DAY ALERT: $ZERO_DAYS" | wall
    fi
    sleep 3600  # Wait 1 hour
done
```

## Customization Tips

### 1. Add Custom Sources
Edit `config.yaml`:
```yaml
news_sources:
  rss_feeds:
    - name: "Your Custom Source"
      url: "https://yourcustomsource.com/rss"
      category: "custom"
      enabled: true
```

### 2. Adjust Priority Keywords
```yaml
content:
  priority_keywords:
    - "your-company-name"
    - "specific-threat"
    - "industry-specific-term"
```

### 3. Custom Scheduling
```yaml
schedule:
  fetch_times:
    - "05:00"  # Early morning
    - "09:00"  # Start of work
    - "13:00"  # Lunch time
    - "17:00"  # End of work
```

## Performance Tips

1. **Cache Management**: Articles are cached for 7 days by default
2. **Source Limiting**: Disable heavy sources in config if needed
3. **Export Regularly**: Use `--export` to backup important news
4. **Monitor Logs**: Check `logs/` directory for any issues

## Troubleshooting

### Common Commands
```bash
# Clear cache and update
rm -rf cache/*
python cyber_news_app.py --update

# Check what sources are actually working
python cyber_news_app.py --sources-list

# View raw logs
tail -f logs/news_aggregator.log

# Test configuration
python -c "from src.config import Config; c=Config(); print(f'Found {len(c.get_all_sources())} sources')"
```

This application gives you **enterprise-level cybersecurity news aggregation for free**! 🎉