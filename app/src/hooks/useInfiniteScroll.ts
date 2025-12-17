import { useEffect, useRef, useCallback } from 'react';
import type { PlotImage } from '../types';
import { BATCH_SIZE } from '../constants';

interface UseInfiniteScrollProps {
  allImages: PlotImage[];
  displayedImages: PlotImage[];
  hasMore: boolean;
  setDisplayedImages: React.Dispatch<React.SetStateAction<PlotImage[]>>;
  setHasMore: (hasMore: boolean) => void;
}

export function useInfiniteScroll({
  allImages,
  displayedImages,
  hasMore,
  setDisplayedImages,
  setHasMore,
}: UseInfiniteScrollProps) {
  const loadMoreRef = useRef<HTMLDivElement>(null);

  // Load more images
  const loadMore = useCallback(() => {
    if (!hasMore) return;

    const currentLength = displayedImages.length;
    const nextBatch = allImages.slice(currentLength, currentLength + BATCH_SIZE);

    setDisplayedImages(prev => [...prev, ...nextBatch]);
    setHasMore(currentLength + BATCH_SIZE < allImages.length);
  }, [allImages, displayedImages.length, hasMore, setDisplayedImages, setHasMore]);

  // Intersection Observer to trigger loadMore - with look-ahead (preload before reaching the end)
  useEffect(() => {
    if (!hasMore) return;

    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting) {
          loadMore();
        }
      },
      {
        threshold: 0.1,
        rootMargin: '1200px 0px' // Trigger 1200px before visible (preload ~4 rows ahead)
      }
    );

    if (loadMoreRef.current) {
      observer.observe(loadMoreRef.current);
    }

    return () => observer.disconnect();
  }, [hasMore, loadMore]);

  return {
    loadMoreRef,
    loadMore,
  };
}
