# 🔒 Cybersecurity News Application

A comprehensive cybersecurity news aggregator that fetches, processes, and displays daily cybersecurity news from multiple trusted sources. Built with Python, featuring both CLI and web interfaces.

## ✨ Features

- **Multi-Source Aggregation**: Fetch news from 7+ trusted cybersecurity sources including Krebs on Security, The Hacker News, Dark Reading, and more
- **Smart Prioritization**: Automatically prioritizes articles based on keywords like "zero-day", "ransomware", "data breach"
- **Duplicate Detection**: Intelligent deduplication to avoid showing the same story multiple times
- **Multiple Interfaces**: 
  - Beautiful command-line interface with Rich formatting
  - Modern web interface with responsive design
  - RESTful API for integration
- **Scheduled Updates**: Automatic news fetching at configurable times
- **Export Functionality**: Export articles to JSON or CSV formats
- **Caching System**: Local caching to reduce API calls and improve performance
- **Content Filtering**: Filter by categories, sources, keywords, and date ranges

## 📁 Project Structure

```
Cyber News/
├── cyber_news_app.py          # Main application entry point
├── config.yaml                # Configuration file
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── src/                       # Source code modules
│   ├── __init__.py
│   ├── config.py              # Configuration management
│   ├── news_aggregator.py     # News fetching and processing
│   ├── cli_interface.py       # Command-line interface
│   ├── web_interface.py       # Web interface (Flask)
│   └── scheduler.py           # Scheduling and daemon functionality
├── templates/                 # Web interface templates
│   └── index.html
├── data/                      # Data storage
├── cache/                     # Cached articles
└── logs/                      # Application logs
```

## 🚀 Quick Start

### 1. Setup Virtual Environment

```bash
# Create virtual environment (recommended)
python3 -m venv news

# Activate virtual environment
source news/bin/activate  # On Linux/Mac
# OR
news\Scripts\activate.bat  # On Windows

# Install Python dependencies
pip install -r requirements.txt

# For enhanced CLI output (optional but recommended)
pip install rich

# For web interface (optional)
pip install flask flask-cors

# For scheduling (optional)
pip install schedule
```

**Note**: Always activate the virtual environment before running commands:
```bash
source news/bin/activate  # Run this first
python cyber_news_app.py --help
```

### 2. Update News Sources

```bash
# Fetch latest news from all sources
python cyber_news_app.py --update
```

### 3. View News

```bash
# Show today's news (default)
python cyber_news_app.py

# Show last 3 days of news
python cyber_news_app.py --show --days 3

# Filter by category
python cyber_news_app.py --show --categories threats vulnerabilities

# Filter by source
python cyber_news_app.py --show --sources "Krebs" "Dark Reading"
```

## 🖥️ Command Line Usage

### Basic Commands

```bash
# Show help
python cyber_news_app.py --help

# Update news from all sources
python cyber_news_app.py --update

# Show today's news
python cyber_news_app.py --show

# Show last week's news
python cyber_news_app.py --show --days 7
```

### Filtering Options

```bash
# Filter by categories
python cyber_news_app.py --show --categories general threats

# Filter by specific sources
python cyber_news_app.py --show --sources "Krebs on Security" "SANS"

# Combine filters
python cyber_news_app.py --show --days 3 --categories vulnerabilities --sources "Threatpost"
```

### Utility Commands

```bash
# List all configured sources
python cyber_news_app.py --sources-list

# Show statistics
python cyber_news_app.py --stats

# Export articles to JSON
python cyber_news_app.py --export json --days 7

# Export articles to CSV
python cyber_news_app.py --export csv --days 3
```

### Scheduling

```bash
# Run as daemon with automatic updates
python cyber_news_app.py --daemon

# Check scheduler status
python cyber_news_app.py --schedule-status
```

## 🌐 Web Interface

Start the web interface for a modern, interactive experience:

```bash
# Start web server (default: http://127.0.0.1:5000)
python cyber_news_app.py --web
```

The web interface provides:
- Real-time article loading
- Interactive filtering
- Export functionality
- Statistics dashboard
- Responsive design for mobile devices

### Web API Endpoints

- `GET /api/news` - Get news articles with optional filters
- `GET /api/sources` - Get configured news sources
- `GET /api/update` - Trigger news update
- `GET /api/statistics` - Get news statistics

## ⚙️ Configuration

Edit `config.yaml` to customize the application:

### News Sources

```yaml
news_sources:
  rss_feeds:
    - name: "Custom Source"
      url: "https://example.com/rss"
      category: "custom"
      enabled: true
```

### Content Filtering

```yaml
content:
  priority_keywords:
    - "zero-day"
    - "ransomware"
    - "data breach"
  exclude_keywords:
    - "advertisement"
  min_article_length: 100
```

### Scheduling

```yaml
schedule:
  fetch_times:
    - "06:00"  # Morning update
    - "12:00"  # Noon update
    - "18:00"  # Evening update
  cache_retention_days: 7
```

### Web Interface

```yaml
web:
  host: "127.0.0.1"
  port: 5000
  debug: false
```

## 📊 News Sources

The application fetches news from these trusted sources:

### RSS Feeds
- **Krebs on Security** - Brian Krebs' cybersecurity blog
- **The Hacker News** - Latest cybersecurity news and vulnerabilities
- **Dark Reading** - Cybersecurity news and analysis
- **Threatpost** - Threat intelligence and security news
- **SecurityWeek** - Information security news
- **BleepingComputer** - Computer security and technology news
- **SANS Internet Storm Center** - Global security monitoring

### Official Sources
- **US-CERT Alerts** - Official cybersecurity alerts
- **CVE Recent Entries** - Latest vulnerability disclosures

## 🔧 Advanced Usage

### Running as a Service

Create a systemd service file for automatic startup:

```ini
[Unit]
Description=Cybersecurity News Daemon
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/cyber-news
ExecStart=/usr/bin/python3 cyber_news_app.py --daemon
Restart=always

[Install]
WantedBy=multi-user.target
```

### Custom Scripts

Create wrapper scripts for common tasks:

```bash
#!/bin/bash
# daily_update.sh
cd "/path/to/cyber-news"
python3 cyber_news_app.py --update
python3 cyber_news_app.py --show --days 1
```

### Integration Examples

Use the API for integration with other tools:

```python
import requests

# Get latest news
response = requests.get('http://localhost:5000/api/news?days=1')
articles = response.json()['articles']

# Trigger update
requests.get('http://localhost:5000/api/update')
```

## 🛠️ Development

### Adding New Sources

1. Add source configuration to `config.yaml`
2. Modify `news_aggregator.py` if special handling is needed
3. Test with `--update` and verify articles are fetched

### Extending Functionality

The modular design makes it easy to extend:
- Add new output formats in `cli_interface.py`
- Implement additional filtering in `news_aggregator.py`
- Create new web endpoints in `web_interface.py`

## 📝 License

This project is open source and available under the MIT License.

## 🐛 Troubleshooting

### Common Issues

**No articles fetched:**
- Check internet connection
- Verify RSS feeds are accessible
- Check logs in `logs/` directory

**Web interface not starting:**
- Install Flask: `pip install flask flask-cors`
- Check if port 5000 is available
- Review web configuration in `config.yaml`

**Scheduling not working:**
- Install schedule: `pip install schedule`
- Check daemon logs
- Verify cron permissions if running as service

### Debug Mode

Enable debug logging by setting `log_level: "DEBUG"` in `config.yaml`.

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## 📞 Support

For questions or issues, please check the logs directory for error details and ensure all dependencies are properly installed.

---

**Stay informed, stay secure! 🔒**