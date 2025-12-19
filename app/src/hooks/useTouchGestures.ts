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
  onTrackEvent?: (name: string, props?: Record<string, string | undefined>) => void;
  selectedSpec?: string;
  selectedLibrary?: string;
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
  onTrackEvent,
  selectedSpec,
  selectedLibrary,
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
        if (viewMode === 'spec') {
          onTrackEvent?.('navigate_prev', { mode: 'spec', spec: selectedSpec, input_method: 'touch' });
          goToPrevSpec();
        } else {
          onTrackEvent?.('navigate_prev', { mode: 'library', library: selectedLibrary, input_method: 'touch' });
          goToPrevLibrary();
        }
      } else {
        // Swipe left = next
        if (viewMode === 'spec') {
          onTrackEvent?.('navigate_next', { mode: 'spec', spec: selectedSpec, input_method: 'touch' });
          goToNextSpec();
        } else {
          onTrackEvent?.('navigate_next', { mode: 'library', library: selectedLibrary, input_method: 'touch' });
          goToNextLibrary();
        }
      }
    } else {
      // Check for double tap
      const now = Date.now();
      if (now - lastTapTime.current < 300) {
        if (viewMode === 'spec') {
          onTrackEvent?.('navigate_shuffle', { mode: 'spec', spec: selectedSpec, input_method: 'touch' });
          shuffleSpec();
        } else {
          onTrackEvent?.('navigate_shuffle', { mode: 'library', library: selectedLibrary, input_method: 'touch' });
          shuffleLibrary();
        }
      }
      lastTapTime.current = now;
    }
    touchStartX.current = null;
  }, [modalImage, viewMode, goToPrevSpec, goToNextSpec, shuffleSpec, goToPrevLibrary, goToNextLibrary, shuffleLibrary, onTrackEvent, selectedSpec, selectedLibrary]);

  return {
    handleTouchStart,
    handleTouchEnd,
  };
}
