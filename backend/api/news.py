"""
FastAPI endpoints for news operations
"""

from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
import asyncio
from datetime import datetime

from core.config import Config
from core.news_aggregator import NewsAggregator
from models.schemas import (
    NewsResponse,
    NewsArticleSchema,
    SourcesResponse,
    NewsSourceSchema,
    UpdateResponse,
    StatisticsResponse,
    ErrorResponse
)

router = APIRouter(prefix="/api", tags=["news"])

# Initialize config and aggregator
config = Config()
aggregator = NewsAggregator(config)


@router.get(
    "/news",
    response_model=NewsResponse,
    responses={500: {"model": ErrorResponse}},
    summary="Get news articles",
    description="Retrieve news articles with optional filtering by days, categories, sources, and limit"
)
async def get_news(
    days: int = Query(default=1, ge=1, le=30, description="Number of days back to fetch"),
    categories: Optional[List[str]] = Query(default=None, description="Filter by categories"),
    sources: Optional[List[str]] = Query(default=None, description="Filter by sources"),
    limit: int = Query(default=50, ge=1, le=200, description="Maximum number of articles")
):
    """Get news articles with filtering options"""
    try:
        # Load articles from cache
        articles = aggregator.load_cached_articles(days_back=days)
        
        # Apply category filter
        if categories:
            articles = [a for a in articles if a.category in categories]
        
        # Apply source filter
        if sources:
            articles = [a for a in articles if any(s in a.source for s in sources)]
        
        # Limit results
        articles = articles[:limit]
        
        # Convert to schema format
        articles_data = []
        for article in articles:
            articles_data.append(NewsArticleSchema(
                article_id=article.article_id,
                title=article.title,
                url=article.url,
                source=article.source,
                category=article.category,
                published_date=article.published_date,
                summary=article.summary,
                keywords=article.keywords,
                priority_score=article.priority_score
            ))
        
        return NewsResponse(
            success=True,
            articles=articles_data,
            total_count=len(articles_data)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/sources",
    response_model=SourcesResponse,
    responses={500: {"model": ErrorResponse}},
    summary="Get news sources",
    description="Retrieve all configured news sources"
)
async def get_sources():
    """Get configured news sources"""
    try:
        sources = config.get_all_sources()
        sources_data = []
        
        for source in sources:
            sources_data.append(NewsSourceSchema(
                name=source.name,
                category=source.category,
                enabled=source.enabled,
                url=source.url
            ))
        
        return SourcesResponse(
            success=True,
            sources=sources_data
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/update",
    response_model=UpdateResponse,
    responses={500: {"model": ErrorResponse}},
    summary="Update news",
    description="Trigger a news update from all configured sources"
)
async def update_news():
    """Trigger news update from all sources"""
    try:
        # Run the async update function
        articles = await aggregator.update_news()
        
        return UpdateResponse(
            success=True,
            message=f"Successfully updated {len(articles)} articles",
            article_count=len(articles)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/statistics",
    response_model=StatisticsResponse,
    responses={500: {"model": ErrorResponse}},
    summary="Get statistics",
    description="Retrieve statistics about cached news articles"
)
async def get_statistics():
    """Get news statistics"""
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
        
        return StatisticsResponse(
            success=True,
            statistics={
                'total_articles': total_articles,
                'sources_count': sources_count,
                'high_priority_count': high_priority_count,
                'categories': categories,
                'last_updated': datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

