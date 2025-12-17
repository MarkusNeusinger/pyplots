import { useState, useCallback, useMemo } from 'react';
import { LIBRARIES } from '../constants';

interface UseNavigationProps {
  specs: string[];
  selectedSpec: string;
  selectedLibrary: string;
  setSelectedSpec: (spec: string) => void;
  setSelectedLibrary: (library: string) => void;
}

export function useNavigation({
  specs,
  selectedSpec,
  selectedLibrary,
  setSelectedSpec,
  setSelectedLibrary,
}: UseNavigationProps) {
  const [isShuffling, setIsShuffling] = useState(false);
  const [isTransitioning, setIsTransitioning] = useState(false);

  // Sorted specs for navigation
  const sortedSpecs = useMemo(() => [...specs].sort(), [specs]);

  // Shuffle to a different random spec
  const shuffleSpec = useCallback(() => {
    if (specs.length <= 1) return;
    setIsShuffling(true);
    setTimeout(() => setIsShuffling(false), 300);
    const otherSpecs = specs.filter((s) => s !== selectedSpec);
    const randomIndex = Math.floor(Math.random() * otherSpecs.length);
    setSelectedSpec(otherSpecs[randomIndex]);
  }, [specs, selectedSpec, setSelectedSpec]);

  // Navigate to previous spec (alphabetically) - with fade transition
  const goToPrevSpec = useCallback(() => {
    if (sortedSpecs.length <= 1 || isTransitioning) return;
    setIsTransitioning(true);
    setTimeout(() => {
      const currentIndex = sortedSpecs.indexOf(selectedSpec);
      const prevIndex = currentIndex <= 0 ? sortedSpecs.length - 1 : currentIndex - 1;
      setSelectedSpec(sortedSpecs[prevIndex]);
    }, 150);
  }, [sortedSpecs, selectedSpec, isTransitioning, setSelectedSpec]);

  // Navigate to next spec (alphabetically) - with fade transition
  const goToNextSpec = useCallback(() => {
    if (sortedSpecs.length <= 1 || isTransitioning) return;
    setIsTransitioning(true);
    setTimeout(() => {
      const currentIndex = sortedSpecs.indexOf(selectedSpec);
      const nextIndex = currentIndex >= sortedSpecs.length - 1 ? 0 : currentIndex + 1;
      setSelectedSpec(sortedSpecs[nextIndex]);
    }, 150);
  }, [sortedSpecs, selectedSpec, isTransitioning, setSelectedSpec]);

  // Shuffle to a different random library
  const shuffleLibrary = useCallback(() => {
    if (LIBRARIES.length <= 1) return;
    setIsShuffling(true);
    setTimeout(() => setIsShuffling(false), 300);
    const otherLibraries = LIBRARIES.filter((l) => l !== selectedLibrary);
    const randomIndex = Math.floor(Math.random() * otherLibraries.length);
    setSelectedLibrary(otherLibraries[randomIndex]);
  }, [selectedLibrary, setSelectedLibrary]);

  // Navigate to previous library (alphabetically) - with fade transition
  const goToPrevLibrary = useCallback(() => {
    if (LIBRARIES.length <= 1 || isTransitioning) return;
    setIsTransitioning(true);
    setTimeout(() => {
      const currentIndex = LIBRARIES.indexOf(selectedLibrary);
      const prevIndex = currentIndex <= 0 ? LIBRARIES.length - 1 : currentIndex - 1;
      setSelectedLibrary(LIBRARIES[prevIndex]);
    }, 150);
  }, [selectedLibrary, isTransitioning, setSelectedLibrary]);

  // Navigate to next library (alphabetically) - with fade transition
  const goToNextLibrary = useCallback(() => {
    if (LIBRARIES.length <= 1 || isTransitioning) return;
    setIsTransitioning(true);
    setTimeout(() => {
      const currentIndex = LIBRARIES.indexOf(selectedLibrary);
      const nextIndex = currentIndex >= LIBRARIES.length - 1 ? 0 : currentIndex + 1;
      setSelectedLibrary(LIBRARIES[nextIndex]);
    }, 150);
  }, [selectedLibrary, isTransitioning, setSelectedLibrary]);

  // Reset transition state (called after images load)
  const resetTransition = useCallback(() => {
    setTimeout(() => setIsTransitioning(false), 50);
  }, []);

  return {
    sortedSpecs,
    isShuffling,
    isTransitioning,
    shuffleSpec,
    goToPrevSpec,
    goToNextSpec,
    shuffleLibrary,
    goToPrevLibrary,
    goToNextLibrary,
    resetTransition,
  };
}
