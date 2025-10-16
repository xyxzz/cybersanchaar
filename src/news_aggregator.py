"""
News aggregation module for fetching cybersecurity news from multiple sources
"""

import asyncio
import aiohttp
import feedparser
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional
from urllib.parse import urljoin
from dataclasses import dataclass, asdict
import hashlib
import re

from .config import Config, NewsSource


@dataclass
class NewsArticle:
    """Data class for news articles"""
    title: str
    url: str
    source: str
    category: str
    published_date: datetime
    summary: str = ""
    content: str = ""
    keywords: List[str] = None
    priority_score: int = 0
    article_id: str = ""
    
    def __post_init__(self):
        """Generate article ID and initialize keywords"""
        if not self.article_id:
            # Generate unique ID based on title and URL
            content_hash = hashlib.md5(f"{self.title}{self.url}".encode()).hexdigest()
            self.article_id = content_hash[:12]
        
        if self.keywords is None:
            self.keywords = []


class NewsAggregator:
    """Main news aggregation class"""
    
    def __init__(self, config: Config):
        self.config = config
        self.session: Optional[aiohttp.ClientSession] = None
        self.articles: List[NewsArticle] = []
        
        # Setup logging
        logging.basicConfig(
            level=getattr(logging, config.log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f"{config.logs_dir}/news_aggregator.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={'User-Agent': 'CyberNewsApp/1.0 (https://github.com/cybernews)'}
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def fetch_rss_feed(self, source: NewsSource) -> List[NewsArticle]:
        """Fetch articles from an RSS feed"""
        articles = []
        
        try:
            self.logger.info(f"Fetching RSS feed: {source.name}")
            
            if not self.session:
                raise RuntimeError("Session not initialized. Use async context manager.")
            
            async with self.session.get(source.url) as response:
                if response.status == 200:
                    content = await response.text()
                    feed = feedparser.parse(content)
                    
                    for entry in feed.entries[:self.config.max_articles_per_source]:
                        # Parse publication date
                        pub_date = self._parse_date(entry)
                        
                        # Skip articles older than cache retention period
                        if self._is_article_too_old(pub_date):
                            continue
                        
                        # Extract content
                        summary = getattr(entry, 'summary', '')
                        content = getattr(entry, 'content', [{}])
                        if content and isinstance(content, list):
                            content_text = content[0].get('value', summary)
                        else:
                            content_text = summary
                        
                        # Create article
                        article = NewsArticle(
                            title=entry.title,
                            url=entry.link,
                            source=source.name,
                            category=source.category,
                            published_date=pub_date,
                            summary=self._clean_text(summary),
                            content=self._clean_text(content_text)
                        )
                        
                        # Calculate priority score and extract keywords
                        article = self._process_article(article)
                        
                        if self._is_article_relevant(article):
                            articles.append(article)
                
                else:
                    self.logger.warning(f"Failed to fetch {source.name}: HTTP {response.status}")
                    
        except Exception as e:
            self.logger.error(f"Error fetching RSS feed {source.name}: {str(e)}")
        
        return articles
    
    def _parse_date(self, entry) -> datetime:
        """Parse publication date from RSS entry"""
        # Try different date fields
        date_fields = ['published_parsed', 'updated_parsed']
        
        for field in date_fields:
            if hasattr(entry, field) and getattr(entry, field):
                time_struct = getattr(entry, field)
                return datetime(*time_struct[:6])
        
        # Fallback to current time
        return datetime.now()
    
    def _is_article_too_old(self, pub_date: datetime) -> bool:
        """Check if article is too old based on cache retention"""
        cutoff_date = datetime.now() - timedelta(days=self.config.cache_retention_days)
        return pub_date < cutoff_date
    
    def _clean_text(self, text: str) -> str:
        """Clean and sanitize text content"""
        if not text:
            return ""
        
        # Remove HTML tags
        clean_text = re.sub(r'<[^>]+>', '', text)
        
        # Remove extra whitespace
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        
        return clean_text
    
    def _process_article(self, article: NewsArticle) -> NewsArticle:
        """Process article to calculate priority score and extract keywords"""
        text_content = f"{article.title} {article.summary} {article.content}".lower()
        
        # Calculate priority score based on keywords
        priority_score = 0
        found_keywords = []
        
        for keyword in self.config.priority_keywords:
            if keyword.lower() in text_content:
                priority_score += 10
                found_keywords.append(keyword)
        
        # Additional scoring based on source category
        category_scores = {
            'alerts': 20,
            'vulnerabilities': 15,
            'threats': 12,
            'general': 5,
            'industry': 3
        }
        priority_score += category_scores.get(article.category, 0)
        
        article.priority_score = priority_score
        article.keywords = found_keywords
        
        return article
    
    def _is_article_relevant(self, article: NewsArticle) -> bool:
        """Check if article is relevant based on content filtering rules"""
        # Check minimum length
        if len(article.content) < self.config.min_article_length:
            return False
        
        # Check for excluded keywords
        text_content = f"{article.title} {article.summary}".lower()
        for exclude_word in self.config.exclude_keywords:
            if exclude_word.lower() in text_content:
                return False
        
        return True
    
    async def update_news(self) -> List[NewsArticle]:
        """Fetch news from all configured sources"""
        self.logger.info("Starting news update process")
        
        async with self:  # Use context manager
            all_articles = []
            
            # Fetch from all sources concurrently
            tasks = []
            for source in self.config.get_all_sources():
                tasks.append(self.fetch_rss_feed(source))
            
            # Wait for all tasks to complete
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Collect articles and handle exceptions
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    source_name = self.config.get_all_sources()[i].name
                    self.logger.error(f"Failed to fetch from {source_name}: {result}")
                else:
                    all_articles.extend(result)
            
            # Remove duplicates and sort by priority
            unique_articles = self._deduplicate_articles(all_articles)
            sorted_articles = sorted(unique_articles, key=lambda x: x.priority_score, reverse=True)
            
            self.articles = sorted_articles
            
            # Cache the results
            await self._cache_articles(sorted_articles)
            
            self.logger.info(f"Successfully fetched {len(sorted_articles)} articles")
            return sorted_articles
    
    def _deduplicate_articles(self, articles: List[NewsArticle]) -> List[NewsArticle]:
        """Remove duplicate articles based on similarity"""
        seen_titles = set()
        unique_articles = []
        
        for article in articles:
            # Simple deduplication based on title similarity
            title_words = set(article.title.lower().split())
            
            is_duplicate = False
            for seen_title in seen_titles:
                seen_words = set(seen_title.split())
                
                # Check for significant overlap
                overlap = len(title_words.intersection(seen_words))
                if overlap > max(3, len(title_words) * 0.7):
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                seen_titles.add(article.title.lower())
                unique_articles.append(article)
        
        return unique_articles
    
    async def _cache_articles(self, articles: List[NewsArticle]):
        """Cache articles to local storage"""
        try:
            cache_file = Path(self.config.cache_dir) / f"articles_{datetime.now().strftime('%Y%m%d')}.json"
            
            # Convert articles to JSON-serializable format
            articles_data = []
            for article in articles:
                article_dict = asdict(article)
                article_dict['published_date'] = article.published_date.isoformat()
                articles_data.append(article_dict)
            
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(articles_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Cached {len(articles)} articles to {cache_file}")
            
        except Exception as e:
            self.logger.error(f"Failed to cache articles: {str(e)}")
    
    def load_cached_articles(self, days_back: int = 1) -> List[NewsArticle]:
        """Load articles from cache"""
        all_articles = []
        
        for i in range(days_back):
            date = datetime.now() - timedelta(days=i)
            cache_file = Path(self.config.cache_dir) / f"articles_{date.strftime('%Y%m%d')}.json"
            
            if cache_file.exists():
                try:
                    with open(cache_file, 'r', encoding='utf-8') as f:
                        articles_data = json.load(f)
                    
                    for article_dict in articles_data:
                        # Convert back to NewsArticle object
                        article_dict['published_date'] = datetime.fromisoformat(article_dict['published_date'])
                        article = NewsArticle(**article_dict)
                        all_articles.append(article)
                
                except Exception as e:
                    self.logger.error(f"Failed to load cached articles from {cache_file}: {str(e)}")
        
        # Sort by priority and date
        all_articles.sort(key=lambda x: (x.priority_score, x.published_date), reverse=True)
        return all_articles