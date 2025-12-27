'use client';

/**
 * Statistics component for displaying news statistics
 */

import React from 'react';
import { NewsArticle } from '@/lib/types';

interface StatisticsProps {
  articles: NewsArticle[];
}

export default function Statistics({ articles }: StatisticsProps) {
  if (articles.length === 0) {
    return null;
  }

  const highPriorityCount = articles.filter(a => a.priority_score > 20).length;
  const mediumPriorityCount = articles.filter(a => a.priority_score > 10 && a.priority_score <= 20).length;
  const sources = new Set(articles.map(a => a.source)).size;

  return (
    <div className="bg-gray-50 rounded-xl p-6 mb-6 grid grid-cols-2 md:grid-cols-4 gap-4">
      <div className="text-center">
        <div className="text-3xl font-bold text-purple-600">{articles.length}</div>
        <div className="text-sm text-gray-600 mt-1">Total Articles</div>
      </div>
      
      <div className="text-center">
        <div className="text-3xl font-bold text-purple-600">{highPriorityCount}</div>
        <div className="text-sm text-gray-600 mt-1">High Priority</div>
      </div>
      
      <div className="text-center">
        <div className="text-3xl font-bold text-purple-600">{mediumPriorityCount}</div>
        <div className="text-sm text-gray-600 mt-1">Medium Priority</div>
      </div>
      
      <div className="text-center">
        <div className="text-3xl font-bold text-purple-600">{sources}</div>
        <div className="text-sm text-gray-600 mt-1">Sources</div>
      </div>
    </div>
  );
}

