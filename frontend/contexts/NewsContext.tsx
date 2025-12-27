'use client';

/**
 * News Context for global state management
 */

import React, { createContext, useContext, useState, useCallback, ReactNode } from 'react';
import { NewsArticle, NewsFilters } from '@/lib/types';
import { fetchNews, updateNews as apiUpdateNews, exportArticlesToJSON } from '@/lib/api';

interface NewsContextType {
  articles: NewsArticle[];
  loading: boolean;
  error: string | null;
  filters: NewsFilters;
  setFilters: (filters: Partial<NewsFilters>) => void;
  loadNews: () => Promise<void>;
  updateNews: () => Promise<void>;
  exportArticles: () => void;
}

const NewsContext = createContext<NewsContextType | undefined>(undefined);

export function NewsProvider({ children }: { children: ReactNode }) {
  const [articles, setArticles] = useState<NewsArticle[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFiltersState] = useState<NewsFilters>({
    days: 1,
    category: '',
    limit: 50,
  });

  const setFilters = useCallback((newFilters: Partial<NewsFilters>) => {
    setFiltersState(prev => ({ ...prev, ...newFilters }));
  }, []);

  const loadNews = useCallback(async () => {
    setLoading(true);
    setError(null);
    
    try {
      const data = await fetchNews(filters);
      setArticles(data);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to load news';
      setError(errorMessage);
      console.error('Error loading news:', err);
    } finally {
      setLoading(false);
    }
  }, [filters]);

  const updateNews = useCallback(async () => {
    setLoading(true);
    setError(null);
    
    try {
      await apiUpdateNews();
      // After updating, reload the news
      await loadNews();
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to update news';
      setError(errorMessage);
      console.error('Error updating news:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [loadNews]);

  const exportArticles = useCallback(() => {
    if (articles.length === 0) {
      alert('No articles to export. Load news first.');
      return;
    }
    exportArticlesToJSON(articles);
  }, [articles]);

  return (
    <NewsContext.Provider
      value={{
        articles,
        loading,
        error,
        filters,
        setFilters,
        loadNews,
        updateNews,
        exportArticles,
      }}
    >
      {children}
    </NewsContext.Provider>
  );
}

export function useNews() {
  const context = useContext(NewsContext);
  if (context === undefined) {
    throw new Error('useNews must be used within a NewsProvider');
  }
  return context;
}

