import { useCallback, useRef } from 'react';
import type { PlotImage } from '../types';

interface UseTouchGesturesProps {
  viewMode: 'spec' | 'library';
  modalImage: PlotImage | null;
  goToPrevSpec: () => void;
  goToNextSpec: () => void;
  shuffleSpec: () => void;
  goToPrevLibrary: () => void;
  goToNextLibrary: () => void;
  shuffleLibrary: () => void;
}

export function useTouchGestures({
  viewMode,
  modalImage,
  goToPrevSpec,
  goToNextSpec,
  shuffleSpec,
  goToPrevLibrary,
  goToNextLibrary,
  shuffleLibrary,
}: UseTouchGesturesProps) {
  const touchStartX = useRef<number | null>(null);
  const lastTapTime = useRef<number>(0);

  const handleTouchStart = useCallback((e: React.TouchEvent) => {
    touchStartX.current = e.touches[0].clientX;
  }, []);

  const handleTouchEnd = useCallback((e: React.TouchEvent) => {
    if (touchStartX.current === null || modalImage) return;

    const touchEndX = e.changedTouches[0].clientX;
    const diff = touchEndX - touchStartX.current;
    const minSwipeDistance = 50;

    if (Math.abs(diff) > minSwipeDistance) {
      if (diff > 0) {
        // Swipe right = previous
        viewMode === 'spec' ? goToPrevSpec() : goToPrevLibrary();
      } else {
        // Swipe left = next
        viewMode === 'spec' ? goToNextSpec() : goToNextLibrary();
      }
    } else {
      // Check for double tap
      const now = Date.now();
      if (now - lastTapTime.current < 300) {
        viewMode === 'spec' ? shuffleSpec() : shuffleLibrary();
      }
      lastTapTime.current = now;
    }
    touchStartX.current = null;
  }, [modalImage, viewMode, goToPrevSpec, goToNextSpec, shuffleSpec, goToPrevLibrary, goToNextLibrary, shuffleLibrary]);

  return {
    handleTouchStart,
    handleTouchEnd,
  };
}
