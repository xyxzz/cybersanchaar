# 🔒 Cybersecurity News Application

A modern full-stack cybersecurity news aggregator built with **Next.js (React)** and **FastAPI**. Fetches, processes, and displays daily cybersecurity news from multiple trusted sources with intelligent prioritization.

## ✨ Features

- **Modern Stack**: Next.js 14 with TypeScript and Tailwind CSS for the frontend, FastAPI for the backend
- **Multi-Source Aggregation**: Fetch news from 7+ trusted cybersecurity sources
- **Smart Prioritization**: Automatically prioritizes articles based on keywords like "zero-day", "ransomware", "data breach"
- **Duplicate Detection**: Intelligent deduplication to avoid showing the same story multiple times
- **Real-time Filtering**: Filter by date range, categories, and article limit
- **Beautiful UI**: Responsive design with gradient backgrounds and smooth animations
- **Export Functionality**: Export articles to JSON format
- **API Documentation**: Automatic OpenAPI/Swagger documentation

## 📁 Project Structure

```
Cyber News/
├── frontend/                 # Next.js application
│   ├── app/                 # Next.js app router
│   │   ├── layout.tsx       # Root layout
│   │   ├── page.tsx         # Main page
│   │   └── globals.css      # Global styles
│   ├── components/          # React components
│   │   ├── NewsArticle.tsx
│   │   ├── FilterControls.tsx
│   │   └── Statistics.tsx
│   ├── contexts/            # React contexts
│   │   └── NewsContext.tsx
│   ├── lib/                 # Utilities
│   │   ├── api.ts           # API client
│   │   └── types.ts         # TypeScript types
│   ├── package.json
│   └── next.config.ts
├── backend/                 # FastAPI application
│   ├── api/                 # API routes
│   │   └── news.py
│   ├── core/                # Core logic
│   │   ├── config.py
│   │   └── news_aggregator.py
│   ├── models/              # Pydantic models
│   │   └── schemas.py
│   ├── main.py              # FastAPI entry point
│   └── requirements.txt
├── cache/                   # Cached articles
├── logs/                    # Application logs
├── config.yaml              # Configuration file
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+**
- **Node.js 18+**
- **npm or yarn**

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the FastAPI server
uvicorn main:app --reload --port 8000
```

The backend will be available at `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

### 2. Frontend Setup

```bash
# Navigate to frontend directory (in a new terminal)
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

### 3. Initial Data Fetch

Once both servers are running:
1. Open `http://localhost:3000` in your browser
2. Click the **"🔄 Update News"** button to fetch the latest articles
3. Click **"📰 Load News"** to display the articles

## 🖥️ Usage

### Web Interface

The web interface provides an intuitive way to browse cybersecurity news:

1. **Filter Controls**:
   - **Days Back**: Choose how many days of news to display (1-7 days)
   - **Category**: Filter by specific categories (general, threats, vulnerabilities, etc.)
   - **Limit**: Set maximum number of articles to display (15-100)

2. **Actions**:
   - **Load News**: Fetch and display articles based on current filters
   - **Update News**: Trigger a fresh fetch from all news sources
   - **Export**: Download articles as JSON file

3. **Article Display**:
   - Articles are color-coded by priority (high/medium/low)
   - Shows source, publication date, category, and keywords
   - Click article titles to open in new tab

### API Endpoints

#### GET `/api/news`
Retrieve news articles with optional filtering.

**Query Parameters**:
- `days` (int): Number of days back (1-30, default: 1)
- `categories` (list): Filter by categories
- `sources` (list): Filter by sources
- `limit` (int): Maximum articles (1-200, default: 50)

**Example**:
```bash
curl "http://localhost:8000/api/news?days=3&limit=25"
```

#### POST `/api/update`
Trigger a news update from all configured sources.

**Example**:
```bash
curl -X POST "http://localhost:8000/api/update"
```

#### GET `/api/sources`
Get all configured news sources.

**Example**:
```bash
curl "http://localhost:8000/api/sources"
```

#### GET `/api/statistics`
Get statistics about cached articles.

**Example**:
```bash
curl "http://localhost:8000/api/statistics"
```

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
  max_articles_per_source: 20
```

### Cache Settings

```yaml
schedule:
  cache_retention_days: 7
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
- **CVE Recent Entries** - Latest vulnerability disclosures (disabled by default)

## 🛠️ Development

### Backend Development

```bash
cd backend

# Run with auto-reload
uvicorn main:app --reload --port 8000

# Run tests (if available)
pytest

# Check logs
tail -f ../logs/fastapi.log
```

### Frontend Development

```bash
cd frontend

# Development server with hot reload
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Lint code
npm run lint
```

## 📦 Production Deployment

### Backend (FastAPI)

```bash
cd backend

# Install production dependencies
pip install -r requirements.txt

# Run with Gunicorn (recommended for production)
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000
```

### Frontend (Next.js)

```bash
cd frontend

# Build the application
npm run build

# Start production server
npm start
```

Or deploy to platforms like:
- **Vercel** (recommended for Next.js)
- **Netlify**
- **AWS Amplify**
- **Docker**

## 🔧 Environment Variables

Create `.env.local` in the frontend directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

For production, update to your production API URL.

## 🐛 Troubleshooting

### Backend Issues

**No articles fetched:**
- Check internet connection
- Verify RSS feeds are accessible
- Check logs in `logs/` directory
- Ensure config.yaml is properly configured

**Import errors:**
- Make sure you're in the backend directory
- Activate virtual environment
- Reinstall dependencies: `pip install -r requirements.txt`

### Frontend Issues

**API connection errors:**
- Ensure backend is running on port 8000
- Check Next.js proxy configuration in `next.config.ts`
- Verify CORS settings in backend

**Build errors:**
- Delete `.next` folder and `node_modules`
- Run `npm install` again
- Check for TypeScript errors: `npm run lint`

### Common Issues

**Port already in use:**
```bash
# Backend (change port)
uvicorn main:app --reload --port 8001

# Frontend (change port)
PORT=3001 npm run dev
```

**Cache issues:**
- Clear cache directory: `rm -rf cache/*`
- Restart both servers

## 📝 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These provide interactive API documentation with the ability to test endpoints directly.

## 🎨 Customization

### Styling

The application uses Tailwind CSS. Customize colors and styles in:
- `frontend/tailwind.config.ts` - Tailwind configuration
- `frontend/app/globals.css` - Global styles
- Component files - Component-specific styles

### Adding New Sources

1. Edit `config.yaml`
2. Add new RSS feed under `news_sources.rss_feeds`
3. Restart the backend
4. Trigger an update from the UI

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, fork the repository, and create pull requests.

## 📞 Support

For questions or issues:
1. Check the logs directory for error details
2. Ensure all dependencies are properly installed
3. Verify configuration in `config.yaml`
4. Check API documentation at `/docs`

---

**Stay informed, stay secure! 🔒**
