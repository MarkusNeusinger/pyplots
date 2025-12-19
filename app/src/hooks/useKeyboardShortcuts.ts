import { useEffect } from 'react';
import type { PlotImage } from '../types';

interface UseKeyboardShortcutsProps {
  viewMode: 'spec' | 'library';
  modalImage: PlotImage | null;
  menuAnchor: HTMLElement | null;
  setModalImage: (image: PlotImage | null) => void;
  setMenuAnchor: (anchor: HTMLElement | null) => void;
  setSearchFilter: (filter: string) => void;
  shuffleSpec: () => void;
  goToPrevSpec: () => void;
  goToNextSpec: () => void;
  shuffleLibrary: () => void;
  goToPrevLibrary: () => void;
  goToNextLibrary: () => void;
  onTrackEvent?: (name: string, props?: Record<string, string | undefined>) => void;
  selectedSpec?: string;
  selectedLibrary?: string;
}

export function useKeyboardShortcuts({
  viewMode,
  modalImage,
  menuAnchor,
  setModalImage,
  setMenuAnchor,
  setSearchFilter,
  shuffleSpec,
  goToPrevSpec,
  goToNextSpec,
  shuffleLibrary,
  goToPrevLibrary,
  goToNextLibrary,
  onTrackEvent,
  selectedSpec,
  selectedLibrary,
}: UseKeyboardShortcutsProps) {
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      const isTyping = document.activeElement?.tagName === 'INPUT' || document.activeElement?.tagName === 'TEXTAREA';

      // Navigation shortcuts work in both spec and library mode
      if (e.code === 'Space' && !modalImage && !menuAnchor && !isTyping) {
        e.preventDefault();
        if (viewMode === 'spec') {
          onTrackEvent?.('navigate_shuffle', { mode: 'spec', spec: selectedSpec, input_method: 'keyboard' });
          shuffleSpec();
        } else {
          onTrackEvent?.('navigate_shuffle', { mode: 'library', library: selectedLibrary, input_method: 'keyboard' });
          shuffleLibrary();
        }
      }
      if (e.code === 'ArrowLeft' && !modalImage && !menuAnchor && !isTyping) {
        e.preventDefault();
        if (viewMode === 'spec') {
          onTrackEvent?.('navigate_prev', { mode: 'spec', spec: selectedSpec, input_method: 'keyboard' });
          goToPrevSpec();
        } else {
          onTrackEvent?.('navigate_prev', { mode: 'library', library: selectedLibrary, input_method: 'keyboard' });
          goToPrevLibrary();
        }
      }
      if (e.code === 'ArrowRight' && !modalImage && !menuAnchor && !isTyping) {
        e.preventDefault();
        if (viewMode === 'spec') {
          onTrackEvent?.('navigate_next', { mode: 'spec', spec: selectedSpec, input_method: 'keyboard' });
          goToNextSpec();
        } else {
          onTrackEvent?.('navigate_next', { mode: 'library', library: selectedLibrary, input_method: 'keyboard' });
          goToNextLibrary();
        }
      }
      if (e.code === 'Enter' && !modalImage && !menuAnchor && !isTyping) {
        e.preventDefault();
        const chip = document.querySelector('[data-spec-chip]') as HTMLElement;
        if (chip) setMenuAnchor(chip);
      }
      if (e.code === 'Escape') {
        if (modalImage) {
          setModalImage(null);
          return; // Close only one element at a time
        }
        if (menuAnchor) {
          setMenuAnchor(null);
          setSearchFilter('');
        }
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [modalImage, menuAnchor, viewMode, shuffleSpec, goToPrevSpec, goToNextSpec, shuffleLibrary, goToPrevLibrary, goToNextLibrary, setModalImage, setMenuAnchor, setSearchFilter, onTrackEvent, selectedSpec, selectedLibrary]);
}
