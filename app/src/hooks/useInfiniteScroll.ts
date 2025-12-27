import { useEffect, useRef, useCallback } from 'react';
import type { PlotImage } from '../types';
import { BATCH_SIZE } from '../constants';

interface UseInfiniteScrollProps {
  allImages: PlotImage[];
  displayedImages: PlotImage[];
  hasMore: boolean;
  setDisplayedImages: React.Dispatch<React.SetStateAction<PlotImage[]>>;
  setHasMore: React.Dispatch<React.SetStateAction<boolean>>;
}

export function useInfiniteScroll({
  allImages,
  displayedImages,
  hasMore,
  setDisplayedImages,
  setHasMore,
}: UseInfiniteScrollProps) {
  const loadMoreRef = useRef<HTMLDivElement>(null);

  // Use refs to avoid stale closures in scroll handler
  const stateRef = useRef({ allImages, displayedImages, hasMore });
  stateRef.current = { allImages, displayedImages, hasMore };

  // Load more images
  const loadMore = useCallback(() => {
    const { allImages: all, displayedImages: displayed, hasMore: more } = stateRef.current;
    if (!more) return;

    const currentLength = displayed.length;
    const remaining = all.length - currentLength;
    if (remaining <= 0) return;

    const itemsToLoad = Math.min(BATCH_SIZE, remaining);
    const nextBatch = all.slice(currentLength, currentLength + itemsToLoad);

    setDisplayedImages(prev => [...prev, ...nextBatch]);
    setHasMore(currentLength + itemsToLoad < all.length);
  }, [setDisplayedImages, setHasMore]);

  // Check if we need to load more based on scroll position
  const checkAndLoad = useCallback(() => {
    const { hasMore: more } = stateRef.current;
    if (!more) return;

    const scrollBottom = window.scrollY + window.innerHeight;
    const docHeight = document.documentElement.scrollHeight;

    // If within 2500px of bottom, load more
    if (scrollBottom + 2500 > docHeight) {
      loadMore();
    }
  }, [loadMore]);

  // Intersection Observer for normal scrolling
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
        rootMargin: '2400px 0px'
      }
    );

    if (loadMoreRef.current) {
      observer.observe(loadMoreRef.current);
    }

    return () => observer.disconnect();
  }, [hasMore, loadMore]);

  // Scroll event for fast scrolling - uses ref to always have fresh state
  useEffect(() => {
    let ticking = false;

    const handleScroll = () => {
      if (!ticking) {
        requestAnimationFrame(() => {
          checkAndLoad();
          ticking = false;
        });
        ticking = true;
      }
    };

    window.addEventListener('scroll', handleScroll, { passive: true });

    // Also check on resize and initial mount
    checkAndLoad();

    return () => window.removeEventListener('scroll', handleScroll);
  }, [checkAndLoad]);

  // Re-check after images are added (in case we need more)
  useEffect(() => {
    // Small delay to let DOM update
    const timer = setTimeout(checkAndLoad, 50);
    return () => clearTimeout(timer);
  }, [displayedImages.length, checkAndLoad]);

  return {
    loadMoreRef,
    loadMore,
  };
}
