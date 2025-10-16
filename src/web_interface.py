"""
Web interface for the Cybersecurity News Application
Optional Flask-based web UI for better user experience
"""

from datetime import datetime
from typing import List, Optional
import json

try:
    from flask import Flask, render_template, jsonify, request, send_from_directory
    from flask_cors import CORS
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    print("💡 Web interface requires Flask. Install with: pip install flask flask-cors")

from .config import Config
from .news_aggregator import NewsAggregator, NewsArticle


def create_app(config: Config) -> Optional[Flask]:
    """Create and configure Flask application"""
    
    if not FLASK_AVAILABLE:
        return None
    
    # Set template folder path relative to the main app directory
    app = Flask(__name__, template_folder='../templates')
    CORS(app)
    
    # Configuration
    app.config['SECRET_KEY'] = 'cybernews-secret-key'
    app.config['DEBUG'] = config.config_data.get('web', {}).get('debug', False)
    
    aggregator = NewsAggregator(config)
    
    @app.route('/')
    def index():
        """Main page"""
        return render_template('index.html')
    
    @app.route('/api/news')
    def get_news():
        """API endpoint to get news articles"""
        try:
            # Get query parameters
            days = int(request.args.get('days', 1))
            categories = request.args.getlist('categories')
            sources = request.args.getlist('sources')
            limit = int(request.args.get('limit', 50))
            
            # Load articles
            articles = aggregator.load_cached_articles(days_back=days)
            
            # Apply filters
            if categories:
                articles = [a for a in articles if a.category in categories]
            
            if sources:
                articles = [a for a in articles if any(s in a.source for s in sources)]
            
            # Limit results
            articles = articles[:limit]
            
            # Convert to JSON-serializable format
            articles_data = []
            for article in articles:
                articles_data.append({
                    'id': article.article_id,
                    'title': article.title,
                    'url': article.url,
                    'source': article.source,
                    'category': article.category,
                    'published_date': article.published_date.isoformat(),
                    'summary': article.summary,
                    'keywords': article.keywords,
                    'priority_score': article.priority_score
                })
            
            return jsonify({
                'success': True,
                'articles': articles_data,
                'total_count': len(articles_data)
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/sources')
    def get_sources():
        """API endpoint to get configured sources"""
        try:
            sources = config.get_all_sources()
            sources_data = []
            
            for source in sources:
                sources_data.append({
                    'name': source.name,
                    'category': source.category,
                    'enabled': source.enabled,
                    'url': source.url
                })
            
            return jsonify({
                'success': True,
                'sources': sources_data
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/update')
    def update_news():
        """API endpoint to trigger news update"""
        try:
            import asyncio
            
            # Run the async update function
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            articles = loop.run_until_complete(aggregator.update_news())
            loop.close()
            
            return jsonify({
                'success': True,
                'message': f'Successfully updated {len(articles)} articles',
                'article_count': len(articles)
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/statistics')
    def get_statistics():
        """API endpoint to get news statistics"""
        try:
            articles = aggregator.load_cached_articles(days_back=7)
            
            # Calculate statistics
            total_articles = len(articles)
            sources_count = len(set(article.source for article in articles))
            categories = {}
            high_priority_count = 0
            
            for article in articles:
                categories[article.category] = categories.get(article.category, 0) + 1
                if article.priority_score > 15:
                    high_priority_count += 1
            
            return jsonify({
                'success': True,
                'statistics': {
                    'total_articles': total_articles,
                    'sources_count': sources_count,
                    'high_priority_count': high_priority_count,
                    'categories': categories,
                    'last_updated': datetime.now().isoformat()
                }
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    return app


def start_web_server():
    """Start the web server"""
    if not FLASK_AVAILABLE:
        print("❌ Flask is not installed. Install it with: pip install flask flask-cors")
        return
    
    config = Config()
    app = create_app(config)
    
    if app:
        print(f"🌐 Starting web server at http://{config.web_host}:{config.web_port}")
        print("Press Ctrl+C to stop the server")
        
        app.run(
            host=config.web_host,
            port=config.web_port,
            debug=config.config_data.get('web', {}).get('debug', False)
        )
    else:
        print("❌ Failed to create Flask application")