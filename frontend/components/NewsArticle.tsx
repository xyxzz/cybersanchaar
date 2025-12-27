'use client';

/**
 * NewsArticle component for displaying individual news articles
 */

import React from 'react';
import { NewsArticle as NewsArticleType } from '@/lib/types';

interface NewsArticleProps {
  article: NewsArticleType;
}

export default function NewsArticle({ article }: NewsArticleProps) {
  const publishedDate = new Date(article.published_date);
  const formattedDate = publishedDate.toLocaleDateString() + ' ' + 
                       publishedDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

  // Determine priority class
  const priorityClass = article.priority_score > 20 
    ? 'high-priority' 
    : article.priority_score > 10 
    ? 'medium-priority' 
    : '';

  // Priority badge
  const priorityBadge = article.priority_score > 20 
    ? { text: `🔥 ${article.priority_score}`, class: 'bg-red-500' }
    : article.priority_score > 10 
    ? { text: `⚡ ${article.priority_score}`, class: 'bg-amber-500' }
    : { text: article.priority_score.toString(), class: 'bg-gray-400' };

  return (
    <div className={`article ${priorityClass} bg-white rounded-xl p-6 mb-5 border transition-all duration-300 hover:-translate-y-1 hover:shadow-xl ${
      article.priority_score > 20 
        ? 'border-l-4 border-l-red-500 bg-gradient-to-r from-red-50/50 to-transparent' 
        : article.priority_score > 10 
        ? 'border-l-4 border-l-amber-500 bg-gradient-to-r from-amber-50/50 to-transparent'
        : 'border-gray-200'
    }`}>
      <div className="flex justify-between items-start gap-4 mb-3">
        <h3 className="text-xl font-semibold text-gray-800 leading-snug flex-1">
          <a 
            href={article.url} 
            target="_blank" 
            rel="noopener noreferrer"
            className="hover:text-purple-600 transition-colors"
          >
            {article.title}
          </a>
        </h3>
        <span className={`${priorityBadge.class} text-white px-3 py-1 rounded-full text-sm font-semibold whitespace-nowrap`}>
          {priorityBadge.text}
        </span>
      </div>

      <div className="flex flex-wrap gap-4 text-sm text-gray-600 mb-3">
        <span className="flex items-center gap-1">
          <span>📌</span>
          <span className="font-medium">{article.source}</span>
        </span>
        <span className="flex items-center gap-1">
          <span>📅</span>
          <span>{formattedDate}</span>
        </span>
        <span className="flex items-center gap-1">
          <span>#</span>
          <span className="text-green-600 font-medium">{article.category}</span>
        </span>
      </div>

      {article.summary && (
        <p className="text-gray-700 leading-relaxed mb-3">
          {article.summary}
        </p>
      )}

      {article.keywords && article.keywords.length > 0 && (
        <div className="flex flex-wrap gap-2">
          {article.keywords.map((keyword, index) => (
            <span 
              key={index}
              className="bg-purple-600 text-white px-3 py-1 rounded-full text-xs font-medium"
            >
              {keyword}
            </span>
          ))}
        </div>
      )}
    </div>
  );
}

