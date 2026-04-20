import { useEffect, useState } from 'react';
import { API_URL } from '../constants';

export interface FeaturedImpl {
  spec_id: string;
  spec_title: string;
  library_id: string;
  language: string;
  quality_score: number;
  preview_url: string | null;
}

/**
 * Fetches a handful of high-quality implementations to feature on the landing
 * page as spec examples. Backed by `/insights/dashboard` (server-cached), we
 * just read its `top_implementations` slice.
 */
export function useFeaturedSpecs(count: number = 4): FeaturedImpl[] | null {
  const [featured, setFeatured] = useState<FeaturedImpl[] | null>(null);

  useEffect(() => {
    let cancelled = false;
    fetch(`${API_URL}/insights/dashboard`)
      .then(r => (r.ok ? r.json() : null))
      .then((data: { top_implementations?: FeaturedImpl[] } | null) => {
        if (cancelled || !data?.top_implementations) return;
        setFeatured(data.top_implementations.slice(0, count));
      })
      .catch(() => {});
    return () => {
      cancelled = true;
    };
  }, [count]);

  return featured;
}
