/**
 * TypeScript types for the Cybersecurity News Application
 */

export interface NewsArticle {
  id: string;
  title: string;
  url: string;
  source: string;
  category: string;
  published_date: string;
  summary: string;
  keywords: string[];
  priority_score: number;
}

export interface NewsSource {
  name: string;
  category: string;
  enabled: boolean;
  url: string;
}

export interface NewsFilters {
  days: number;
  category: string;
  limit: number;
}

export interface Statistics {
  total_articles: number;
  sources_count: number;
  high_priority_count: number;
  categories: Record<string, number>;
  last_updated: string;
}

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
}

