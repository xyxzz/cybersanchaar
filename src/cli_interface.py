"""
Command Line Interface for the Cybersecurity News Application
"""

from datetime import datetime, timedelta
from typing import List, Optional
import textwrap
from dataclasses import asdict

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.text import Text
    from rich.syntax import Syntax
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("💡 Tip: Install 'rich' for enhanced CLI output: pip install rich")

from .config import Config
from .news_aggregator import NewsAggregator, NewsArticle


class CLIInterface:
    """Command line interface for displaying cybersecurity news"""
    
    def __init__(self, config: Config):
        self.config = config
        self.aggregator = NewsAggregator(config)
        
        if RICH_AVAILABLE:
            self.console = Console()
        else:
            self.console = None
    
    def display_news(self, categories: Optional[List[str]] = None, 
                    sources: Optional[List[str]] = None, 
                    days: int = 1):
        """Display news articles with filtering options"""
        
        # Load cached articles
        articles = self.aggregator.load_cached_articles(days_back=days)
        
        if not articles:
            self._print_message("📭 No cached news found. Run with --update to fetch latest news.", "warning")
            return
        
        # Apply filters
        filtered_articles = self._filter_articles(articles, categories, sources)
        
        if not filtered_articles:
            self._print_message("🔍 No articles found matching your criteria.", "info")
            return
        
        # Limit to max display articles
        display_articles = filtered_articles[:self.config.max_display_articles]
        
        # Display articles
        if RICH_AVAILABLE:
            self._display_rich(display_articles, days)
        else:
            self._display_plain(display_articles, days)
        
        # Show summary
        total_count = len(filtered_articles)
        displayed_count = len(display_articles)
        
        if displayed_count < total_count:
            self._print_message(
                f"📊 Showing {displayed_count} of {total_count} articles. "
                f"Use filters to narrow down results.",
                "info"
            )
    
    def _filter_articles(self, articles: List[NewsArticle], 
                        categories: Optional[List[str]] = None,
                        sources: Optional[List[str]] = None) -> List[NewsArticle]:
        """Filter articles based on criteria"""
        
        filtered = articles
        
        # Filter by categories
        if categories:
            categories_lower = [cat.lower() for cat in categories]
            filtered = [
                article for article in filtered 
                if article.category.lower() in categories_lower
            ]
        
        # Filter by sources
        if sources:
            sources_lower = [src.lower() for src in sources]
            filtered = [
                article for article in filtered 
                if any(src in article.source.lower() for src in sources_lower)
            ]
        
        return filtered
    
    def _display_rich(self, articles: List[NewsArticle], days: int):
        """Display articles using Rich formatting"""
        
        # Header
        if days == 1:
            title = f"📰 Today's Cybersecurity News ({len(articles)} articles)"
        else:
            title = f"📰 Cybersecurity News - Last {days} days ({len(articles)} articles)"
        
        self.console.print(Panel(title, style="bold blue"))
        
        # Articles
        for i, article in enumerate(articles, 1):
            self._display_article_rich(article, i)
            
            if i < len(articles):
                self.console.print("─" * 80, style="dim")
    
    def _display_article_rich(self, article: NewsArticle, index: int):
        """Display a single article using Rich formatting"""
        
        # Priority indicator
        priority_color = self._get_priority_color(article.priority_score)
        priority_indicator = "🔥" if article.priority_score > 20 else "📰"
        
        # Title with priority
        title_text = Text()
        title_text.append(f"{index}. ", style="dim")
        title_text.append(priority_indicator + " ")
        title_text.append(article.title, style=f"bold {priority_color}")
        
        self.console.print(title_text)
        
        # Source and date
        source_date = Text()
        source_date.append("📌 ", style="blue")
        source_date.append(article.source, style="blue")
        source_date.append(" • ", style="dim")
        source_date.append(article.published_date.strftime("%Y-%m-%d %H:%M"), style="dim")
        
        if article.category:
            source_date.append(" • ", style="dim")
            source_date.append(f"#{article.category}", style="green")
        
        self.console.print(source_date)
        
        # Summary
        if article.summary:
            summary = self._truncate_text(article.summary, 300)
            self.console.print(f"💬 {summary}", style="italic")
        
        # Keywords
        if article.keywords:
            keywords_text = Text("🏷️  Keywords: ", style="yellow")
            keywords_text.append(", ".join(article.keywords), style="yellow dim")
            self.console.print(keywords_text)
        
        # URL
        self.console.print(f"🔗 {article.url}", style="link " + article.url)
        
        # Priority score (if high)
        if article.priority_score > 15:
            self.console.print(f"⚡ Priority Score: {article.priority_score}", style="red bold")
    
    def _display_plain(self, articles: List[NewsArticle], days: int):
        """Display articles using plain text formatting"""
        
        # Header
        if days == 1:
            print("\n📰 TODAY'S CYBERSECURITY NEWS")
        else:
            print(f"\n📰 CYBERSECURITY NEWS - LAST {days} DAYS")
        
        print("=" * 60)
        print(f"Found {len(articles)} articles\n")
        
        # Articles
        for i, article in enumerate(articles, 1):
            self._display_article_plain(article, i)
            
            if i < len(articles):
                print("-" * 60)
    
    def _display_article_plain(self, article: NewsArticle, index: int):
        """Display a single article using plain text"""
        
        # Priority indicator
        priority_indicator = "🔥" if article.priority_score > 20 else "📰"
        
        # Title
        print(f"{index}. {priority_indicator} {article.title}")
        
        # Source and date
        date_str = article.published_date.strftime("%Y-%m-%d %H:%M")
        print(f"📌 {article.source} • {date_str} • #{article.category}")
        
        # Summary
        if article.summary:
            summary = self._truncate_text(article.summary, 300)
            wrapped_summary = textwrap.fill(summary, width=75, initial_indent="💬 ", subsequent_indent="   ")
            print(wrapped_summary)
        
        # Keywords
        if article.keywords:
            print(f"🏷️  Keywords: {', '.join(article.keywords)}")
        
        # URL
        print(f"🔗 {article.url}")
        
        # Priority score (if high)
        if article.priority_score > 15:
            print(f"⚡ Priority Score: {article.priority_score}")
        
        print()
    
    def _get_priority_color(self, score: int) -> str:
        """Get color based on priority score"""
        if score >= 25:
            return "red"
        elif score >= 15:
            return "yellow"
        elif score >= 10:
            return "blue"
        else:
            return "white"
    
    def _truncate_text(self, text: str, max_length: int) -> str:
        """Truncate text to specified length"""
        if len(text) <= max_length:
            return text
        
        return text[:max_length - 3] + "..."
    
    def _print_message(self, message: str, msg_type: str = "info"):
        """Print a formatted message"""
        
        icons = {
            "info": "ℹ️",
            "warning": "⚠️",
            "error": "❌",
            "success": "✅"
        }
        
        icon = icons.get(msg_type, "ℹ️")
        
        if RICH_AVAILABLE:
            style_map = {
                "info": "blue",
                "warning": "yellow",
                "error": "red",
                "success": "green"
            }
            style = style_map.get(msg_type, "blue")
            self.console.print(f"{icon} {message}", style=style)
        else:
            print(f"{icon} {message}")
    
    def show_sources(self):
        """Display configured news sources"""
        sources = self.config.get_all_sources()
        
        if RICH_AVAILABLE:
            table = Table(title="📡 Configured News Sources")
            table.add_column("Source", style="cyan", no_wrap=True)
            table.add_column("Category", style="magenta")
            table.add_column("Status", justify="center")
            table.add_column("URL", style="blue", overflow="fold")
            
            for source in sources:
                status = "✅ Enabled" if source.enabled else "❌ Disabled"
                status_style = "green" if source.enabled else "red"
                
                table.add_row(
                    source.name,
                    source.category,
                    Text(status, style=status_style),
                    source.url
                )
            
            self.console.print(table)
        else:
            print("\n📡 CONFIGURED NEWS SOURCES")
            print("=" * 60)
            
            for source in sources:
                status = "✅ Enabled" if source.enabled else "❌ Disabled"
                print(f"• {source.name}")
                print(f"  Category: {source.category}")
                print(f"  Status: {status}")
                print(f"  URL: {source.url}")
                print()
    
    def show_statistics(self):
        """Show news statistics"""
        articles = self.aggregator.load_cached_articles(days_back=7)
        
        if not articles:
            self._print_message("No cached articles found for statistics.", "warning")
            return
        
        # Calculate statistics
        total_articles = len(articles)
        sources_count = len(set(article.source for article in articles))
        categories = {}
        high_priority_count = 0
        
        for article in articles:
            # Count by category
            categories[article.category] = categories.get(article.category, 0) + 1
            
            # Count high priority
            if article.priority_score > 15:
                high_priority_count += 1
        
        # Display statistics
        if RICH_AVAILABLE:
            stats_table = Table(title="📊 News Statistics (Last 7 Days)")
            stats_table.add_column("Metric", style="cyan")
            stats_table.add_column("Value", justify="right", style="yellow")
            
            stats_table.add_row("Total Articles", str(total_articles))
            stats_table.add_row("Active Sources", str(sources_count))
            stats_table.add_row("High Priority Articles", str(high_priority_count))
            
            self.console.print(stats_table)
            
            # Category breakdown
            if categories:
                cat_table = Table(title="📂 Articles by Category")
                cat_table.add_column("Category", style="cyan")
                cat_table.add_column("Count", justify="right", style="yellow")
                
                for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
                    cat_table.add_row(category.title(), str(count))
                
                self.console.print(cat_table)
        else:
            print("\n📊 NEWS STATISTICS (LAST 7 DAYS)")
            print("=" * 40)
            print(f"Total Articles: {total_articles}")
            print(f"Active Sources: {sources_count}")
            print(f"High Priority Articles: {high_priority_count}")
            
            print("\n📂 ARTICLES BY CATEGORY")
            print("-" * 30)
            for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
                print(f"{category.title()}: {count}")
    
    def export_articles(self, format_type: str = "json", days: int = 1):
        """Export articles to file"""
        articles = self.aggregator.load_cached_articles(days_back=days)
        
        if not articles:
            self._print_message("No articles to export.", "warning")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format_type.lower() == "json":
            filename = f"cybernews_export_{timestamp}.json"
            self._export_json(articles, filename)
        elif format_type.lower() == "csv":
            filename = f"cybernews_export_{timestamp}.csv"
            self._export_csv(articles, filename)
        else:
            self._print_message(f"Unsupported export format: {format_type}", "error")
            return
        
        self._print_message(f"Articles exported to {filename}", "success")
    
    def _export_json(self, articles: List[NewsArticle], filename: str):
        """Export articles to JSON"""
        import json
        
        articles_data = []
        for article in articles:
            article_dict = asdict(article)
            article_dict['published_date'] = article.published_date.isoformat()
            articles_data.append(article_dict)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(articles_data, f, indent=2, ensure_ascii=False)
    
    def _export_csv(self, articles: List[NewsArticle], filename: str):
        """Export articles to CSV"""
        import csv
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow(['Title', 'Source', 'Category', 'Published Date', 'Priority Score', 'URL', 'Summary'])
            
            # Data
            for article in articles:
                writer.writerow([
                    article.title,
                    article.source,
                    article.category,
                    article.published_date.isoformat(),
                    article.priority_score,
                    article.url,
                    article.summary
                ])