'use client';

/**
 * Main page for the Cybersecurity News Application
 */

import { useEffect } from 'react';
import { useNews } from '@/contexts/NewsContext';
import NewsArticle from '@/components/NewsArticle';
import FilterControls from '@/components/FilterControls';
import Statistics from '@/components/Statistics';

export default function Home() {
  const { articles, loading, error, loadNews } = useNews();

  // Auto-load news on mount
  useEffect(() => {
    loadNews();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []); // Only run once on mount

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-600 via-purple-700 to-purple-900">
      <div className="container mx-auto px-4 py-8 max-w-6xl">
        {/* Header */}
        <header className="text-center mb-8 text-white">
          <h1 className="text-5xl font-bold mb-3 drop-shadow-lg">
            🔒 Cyber Security News
          </h1>
          <p className="text-xl opacity-90">
            Stay informed with the latest cybersecurity threats and news
          </p>
        </header>

        {/* Filter Controls */}
        <FilterControls />

        {/* Loading State */}
        {loading && (
          <div className="text-center py-16 text-white">
            <div className="inline-block w-12 h-12 border-4 border-white border-t-transparent rounded-full animate-spin mb-4"></div>
            <div className="text-xl">Loading news articles...</div>
          </div>
        )}

        {/* Error State */}
        {error && !loading && (
          <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-6 rounded-lg mb-6">
            <h3 className="font-bold text-lg mb-2">❌ Error loading news</h3>
            <p>{error}</p>
            <p className="mt-2 text-sm">Try updating the news first or check if the server is running.</p>
          </div>
        )}

        {/* News Container */}
        {!loading && !error && (
          <div className="bg-white/95 backdrop-blur-sm rounded-2xl p-6 shadow-xl">
            {articles.length === 0 ? (
              <div className="text-center py-16 text-gray-500">
                <h3 className="text-2xl font-semibold mb-3">📭 No articles loaded</h3>
                <p>Click "Load News" to fetch the latest cybersecurity news</p>
              </div>
            ) : (
              <>
                {/* Statistics */}
                <Statistics articles={articles} />

                {/* Articles List */}
                <div>
                  {articles.map((article) => (
                    <NewsArticle key={article.id} article={article} />
                  ))}
                </div>
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
