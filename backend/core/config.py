"""
Configuration management for the Cybersecurity News Application
"""

import yaml
import os
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class NewsSource:
    """Data class for news source configuration"""
    name: str
    url: str
    category: str
    enabled: bool = True


class Config:
    """Configuration manager for the application"""
    
    def __init__(self, config_file: str = "../config.yaml"):
        self.config_file = config_file
        self.config_data = self._load_config()
        self._setup_directories()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        # Try to find config.yaml in the project root
        current_dir = Path(__file__).parent
        config_path = current_dir.parent.parent / "config.yaml"
        
        if not config_path.exists():
            # Fallback to relative path
            config_path = Path(self.config_file)
        
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        with open(config_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    
    def _setup_directories(self):
        """Create necessary directories if they don't exist"""
        directories = [
            self.cache_dir,
            self.data_dir,
            self.logs_dir
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
    
    @property
    def app_name(self) -> str:
        return self.config_data.get('app', {}).get('name', 'Cyber News App')
    
    @property
    def app_version(self) -> str:
        return self.config_data.get('app', {}).get('version', '1.0.0')
    
    @property
    def cache_dir(self) -> str:
        # Use absolute path relative to project root
        current_dir = Path(__file__).parent
        cache_path = current_dir.parent.parent / self.config_data.get('app', {}).get('cache_dir', './cache')
        return str(cache_path)
    
    @property
    def data_dir(self) -> str:
        # Use absolute path relative to project root
        current_dir = Path(__file__).parent
        data_path = current_dir.parent.parent / self.config_data.get('app', {}).get('data_dir', './data')
        return str(data_path)
    
    @property
    def logs_dir(self) -> str:
        # Use absolute path relative to project root
        current_dir = Path(__file__).parent
        logs_path = current_dir.parent.parent / 'logs'
        return str(logs_path)
    
    @property
    def log_level(self) -> str:
        return self.config_data.get('app', {}).get('log_level', 'INFO')
    
    def get_rss_sources(self) -> List[NewsSource]:
        """Get enabled RSS feed sources"""
        sources = []
        rss_feeds = self.config_data.get('news_sources', {}).get('rss_feeds', [])
        
        for feed_config in rss_feeds:
            if feed_config.get('enabled', True):
                sources.append(NewsSource(
                    name=feed_config['name'],
                    url=feed_config['url'],
                    category=feed_config['category'],
                    enabled=feed_config.get('enabled', True)
                ))
        
        return sources
    
    def get_official_sources(self) -> List[NewsSource]:
        """Get enabled official sources"""
        sources = []
        official_sources = self.config_data.get('news_sources', {}).get('official_sources', [])
        
        for source_config in official_sources:
            if source_config.get('enabled', True):
                sources.append(NewsSource(
                    name=source_config['name'],
                    url=source_config['url'],
                    category=source_config['category'],
                    enabled=source_config.get('enabled', True)
                ))
        
        return sources
    
    def get_all_sources(self) -> List[NewsSource]:
        """Get all enabled news sources"""
        return self.get_rss_sources() + self.get_official_sources()
    
    @property
    def priority_keywords(self) -> List[str]:
        """Get priority keywords for content filtering"""
        return self.config_data.get('content', {}).get('priority_keywords', [])
    
    @property
    def exclude_keywords(self) -> List[str]:
        """Get keywords to exclude from content"""
        return self.config_data.get('content', {}).get('exclude_keywords', [])
    
    @property
    def min_article_length(self) -> int:
        """Get minimum article length threshold"""
        return self.config_data.get('content', {}).get('min_article_length', 100)
    
    @property
    def max_articles_per_source(self) -> int:
        """Get maximum articles per source"""
        return self.config_data.get('content', {}).get('max_articles_per_source', 20)
    
    @property
    def cache_retention_days(self) -> int:
        """Get cache retention period in days"""
        return self.config_data.get('schedule', {}).get('cache_retention_days', 7)

