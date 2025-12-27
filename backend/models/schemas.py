"""
Pydantic models for API request/response validation
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime


class NewsArticleSchema(BaseModel):
    """Schema for news article"""
    id: str = Field(..., alias="article_id", description="Unique article identifier")
    title: str = Field(..., description="Article title")
    url: str = Field(..., description="Article URL")
    source: str = Field(..., description="News source name")
    category: str = Field(..., description="Article category")
    published_date: datetime = Field(..., description="Publication date")
    summary: str = Field(default="", description="Article summary")
    keywords: List[str] = Field(default_factory=list, description="Priority keywords found")
    priority_score: int = Field(default=0, description="Priority score")
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "id": "abc123def456",
                "title": "Critical Zero-Day Vulnerability Discovered",
                "url": "https://example.com/article",
                "source": "The Hacker News",
                "category": "vulnerabilities",
                "published_date": "2024-01-15T10:30:00",
                "summary": "A critical zero-day vulnerability has been discovered...",
                "keywords": ["zero-day", "vulnerability"],
                "priority_score": 25
            }
        }


class NewsSourceSchema(BaseModel):
    """Schema for news source"""
    name: str = Field(..., description="Source name")
    category: str = Field(..., description="Source category")
    enabled: bool = Field(default=True, description="Whether source is enabled")
    url: str = Field(..., description="Source URL")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Krebs on Security",
                "category": "general",
                "enabled": True,
                "url": "https://krebsonsecurity.com/feed/"
            }
        }


class NewsResponse(BaseModel):
    """Response schema for news articles endpoint"""
    success: bool = Field(default=True, description="Request success status")
    articles: List[NewsArticleSchema] = Field(..., description="List of news articles")
    total_count: int = Field(..., description="Total number of articles")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "articles": [],
                "total_count": 0
            }
        }


class SourcesResponse(BaseModel):
    """Response schema for sources endpoint"""
    success: bool = Field(default=True, description="Request success status")
    sources: List[NewsSourceSchema] = Field(..., description="List of news sources")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "sources": []
            }
        }


class UpdateResponse(BaseModel):
    """Response schema for update endpoint"""
    success: bool = Field(default=True, description="Request success status")
    message: str = Field(..., description="Status message")
    article_count: int = Field(..., description="Number of articles fetched")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Successfully updated 42 articles",
                "article_count": 42
            }
        }


class StatisticsResponse(BaseModel):
    """Response schema for statistics endpoint"""
    success: bool = Field(default=True, description="Request success status")
    statistics: Dict = Field(..., description="Statistics data")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "statistics": {
                    "total_articles": 150,
                    "sources_count": 7,
                    "high_priority_count": 12,
                    "categories": {
                        "general": 50,
                        "threats": 30,
                        "vulnerabilities": 25
                    },
                    "last_updated": "2024-01-15T10:30:00"
                }
            }
        }


class ErrorResponse(BaseModel):
    """Response schema for errors"""
    success: bool = Field(default=False, description="Request success status")
    error: str = Field(..., description="Error message")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "error": "Failed to fetch news articles"
            }
        }


class NewsQueryParams(BaseModel):
    """Query parameters for news endpoint"""
    days: int = Field(default=1, ge=1, le=30, description="Number of days back to fetch")
    categories: Optional[List[str]] = Field(default=None, description="Filter by categories")
    sources: Optional[List[str]] = Field(default=None, description="Filter by sources")
    limit: int = Field(default=50, ge=1, le=200, description="Maximum number of articles")

