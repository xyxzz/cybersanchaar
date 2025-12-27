/**
 * API client functions for communicating with the FastAPI backend
 */

import { NewsArticle, NewsSource, Statistics, NewsFilters } from './types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || '';

/**
 * Fetch news articles with optional filters
 */
export async function fetchNews(filters: Partial<NewsFilters> = {}): Promise<NewsArticle[]> {
  const params = new URLSearchParams();
  
  if (filters.days) params.append('days', filters.days.toString());
  if (filters.category) params.append('categories', filters.category);
  if (filters.limit) params.append('limit', filters.limit.toString());
  
  const url = `${API_BASE_URL}/api/news?${params.toString()}`;
  
  const response = await fetch(url);
  
  if (!response.ok) {
    throw new Error(`Failed to fetch news: ${response.statusText}`);
  }
  
  const data = await response.json();
  
  if (!data.success) {
    throw new Error(data.error || 'Failed to fetch news');
  }
  
  return data.articles;
}

/**
 * Trigger a news update from all sources
 */
export async function updateNews(): Promise<{ message: string; article_count: number }> {
  const response = await fetch(`${API_BASE_URL}/api/update`, {
    method: 'POST',
  });
  
  if (!response.ok) {
    throw new Error(`Failed to update news: ${response.statusText}`);
  }
  
  const data = await response.json();
  
  if (!data.success) {
    throw new Error(data.error || 'Failed to update news');
  }
  
  return {
    message: data.message,
    article_count: data.article_count,
  };
}

/**
 * Fetch configured news sources
 */
export async function fetchSources(): Promise<NewsSource[]> {
  const response = await fetch(`${API_BASE_URL}/api/sources`);
  
  if (!response.ok) {
    throw new Error(`Failed to fetch sources: ${response.statusText}`);
  }
  
  const data = await response.json();
  
  if (!data.success) {
    throw new Error(data.error || 'Failed to fetch sources');
  }
  
  return data.sources;
}

/**
 * Fetch news statistics
 */
export async function fetchStatistics(): Promise<Statistics> {
  const response = await fetch(`${API_BASE_URL}/api/statistics`);
  
  if (!response.ok) {
    throw new Error(`Failed to fetch statistics: ${response.statusText}`);
  }
  
  const data = await response.json();
  
  if (!data.success) {
    throw new Error(data.error || 'Failed to fetch statistics');
  }
  
  return data.statistics;
}

/**
 * Export articles to JSON
 */
export function exportArticlesToJSON(articles: NewsArticle[]): void {
  const dataStr = JSON.stringify(articles, null, 2);
  const dataBlob = new Blob([dataStr], { type: 'application/json' });
  const url = URL.createObjectURL(dataBlob);
  
  const link = document.createElement('a');
  link.href = url;
  link.download = `cybernews_export_${new Date().toISOString().split('T')[0]}.json`;
  link.click();
  
  URL.revokeObjectURL(url);
}

