'use client';

/**
 * FilterControls component for filtering news articles
 */

import React from 'react';
import { useNews } from '@/contexts/NewsContext';

export default function FilterControls() {
  const { filters, setFilters, loadNews, updateNews, exportArticles, loading } = useNews();

  const handleLoadNews = async () => {
    await loadNews();
  };

  const handleUpdateNews = async () => {
    try {
      await updateNews();
      alert('✅ News updated successfully!');
    } catch (error) {
      alert('❌ Failed to update news. Please try again.');
    }
  };

  return (
    <div className="bg-white/95 backdrop-blur-sm rounded-2xl p-6 mb-6 shadow-lg">
      <div className="flex flex-wrap gap-4 mb-4">
        <div className="flex flex-col gap-2">
          <label htmlFor="daysSelect" className="text-sm font-semibold text-gray-700">
            Days Back
          </label>
          <select
            id="daysSelect"
            value={filters.days}
            onChange={(e) => setFilters({ days: parseInt(e.target.value) })}
            className="px-4 py-2 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-purple-500 focus:ring-2 focus:ring-purple-200 transition-all"
          >
            <option value="1">Today</option>
            <option value="2">Last 2 days</option>
            <option value="3">Last 3 days</option>
            <option value="7">Last week</option>
          </select>
        </div>

        <div className="flex flex-col gap-2">
          <label htmlFor="categorySelect" className="text-sm font-semibold text-gray-700">
            Category
          </label>
          <select
            id="categorySelect"
            value={filters.category}
            onChange={(e) => setFilters({ category: e.target.value })}
            className="px-4 py-2 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-purple-500 focus:ring-2 focus:ring-purple-200 transition-all"
          >
            <option value="">All Categories</option>
            <option value="general">General</option>
            <option value="threats">Threats</option>
            <option value="vulnerabilities">Vulnerabilities</option>
            <option value="alerts">Alerts</option>
            <option value="industry">Industry</option>
            <option value="research">Research</option>
            <option value="technical">Technical</option>
          </select>
        </div>

        <div className="flex flex-col gap-2">
          <label htmlFor="limitSelect" className="text-sm font-semibold text-gray-700">
            Limit
          </label>
          <select
            id="limitSelect"
            value={filters.limit}
            onChange={(e) => setFilters({ limit: parseInt(e.target.value) })}
            className="px-4 py-2 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-purple-500 focus:ring-2 focus:ring-purple-200 transition-all"
          >
            <option value="15">15 articles</option>
            <option value="25">25 articles</option>
            <option value="50">50 articles</option>
            <option value="100">100 articles</option>
          </select>
        </div>
      </div>

      <div className="flex flex-wrap gap-3">
        <button
          onClick={handleLoadNews}
          disabled={loading}
          className="px-6 py-2 bg-gradient-to-r from-purple-600 to-purple-800 text-white rounded-lg font-semibold hover:scale-105 transition-transform disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100 shadow-md"
        >
          {loading ? '⏳ Loading...' : '📰 Load News'}
        </button>

        <button
          onClick={handleUpdateNews}
          disabled={loading}
          className="px-6 py-2 bg-gradient-to-r from-green-500 to-green-700 text-white rounded-lg font-semibold hover:scale-105 transition-transform disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100 shadow-md"
        >
          {loading ? '⏳ Updating...' : '🔄 Update News'}
        </button>

        <button
          onClick={exportArticles}
          disabled={loading}
          className="px-6 py-2 bg-gradient-to-r from-pink-500 to-rose-600 text-white rounded-lg font-semibold hover:scale-105 transition-transform disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100 shadow-md"
        >
          📁 Export
        </button>
      </div>
    </div>
  );
}

