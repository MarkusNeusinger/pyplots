import { useState, useEffect, useCallback } from 'react';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import Alert from '@mui/material/Alert';

import type { PlotImage, LibraryInfo, SpecInfo } from './types';
import { API_URL, LIBRARIES, BATCH_SIZE } from './constants';
import { useNavigation, useTouchGestures, useKeyboardShortcuts, useInfiniteScroll } from './hooks';
import { Header, Footer, NavigationBar, SelectionMenu, ImagesGrid, FullscreenModal } from './components';

// Fisher-Yates shuffle algorithm
const shuffleArray = <T,>(array: T[]): T[] => {
  const shuffled = [...array];
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  return shuffled;
};

function App() {
  // Core state
  const [specs, setSpecs] = useState<string[]>([]);
  const [selectedSpec, setSelectedSpec] = useState<string>('');
  const [selectedLibrary, setSelectedLibrary] = useState<string>('');
  const [viewMode, setViewMode] = useState<'spec' | 'library'>('spec');
  const [specsLoaded, setSpecsLoaded] = useState(false);

  // Data state
  const [specsData, setSpecsData] = useState<SpecInfo[]>([]);
  const [librariesData, setLibrariesData] = useState<LibraryInfo[]>([]);
  const [allImages, setAllImages] = useState<PlotImage[]>([]);
  const [displayedImages, setDisplayedImages] = useState<PlotImage[]>([]);
  const [hasMore, setHasMore] = useState(false);

  // UI state
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');
  const [modalImage, setModalImage] = useState<PlotImage | null>(null);
  const [menuAnchor, setMenuAnchor] = useState<HTMLElement | null>(null);
  const [descriptionOpen, setDescriptionOpen] = useState(false);
  const [isRolling, setIsRolling] = useState(false);
  const [openImageTooltip, setOpenImageTooltip] = useState<string | null>(null);

  // Description state
  const [specDescription, setSpecDescription] = useState<string>('');
  const [libraryDescription, setLibraryDescription] = useState<string>('');
  const [libraryDocsUrl, setLibraryDocsUrl] = useState<string>('');

  // Custom hooks
  const navigation = useNavigation({
    specs,
    selectedSpec,
    selectedLibrary,
    setSelectedSpec,
    setSelectedLibrary,
  });

  const { handleTouchStart, handleTouchEnd } = useTouchGestures({
    viewMode,
    modalImage,
    ...navigation,
  });

  useKeyboardShortcuts({
    viewMode,
    modalImage,
    menuAnchor,
    setModalImage,
    setMenuAnchor,
    setSearchFilter: () => {}, // No-op: SelectionMenu manages its own internal searchFilter state
    ...navigation,
  });

  const { loadMoreRef } = useInfiniteScroll({
    allImages,
    displayedImages,
    hasMore,
    setDisplayedImages,
    setHasMore,
  });

  // Toggle between spec and library view with roll animation
  const toggleViewMode = useCallback(() => {
    setIsRolling(true);
    setDescriptionOpen(false);
    setAllImages([]);
    setDisplayedImages([]);
    setHasMore(false);
    setLoading(true);
    setTimeout(() => {
      setViewMode((prev) => {
        if (prev === 'spec') {
          const randomLib = LIBRARIES[Math.floor(Math.random() * LIBRARIES.length)];
          setSelectedLibrary(randomLib);
          return 'library';
        } else {
          if (specs.length > 0) {
            const randomSpec = specs[Math.floor(Math.random() * specs.length)];
            setSelectedSpec(randomSpec);
          }
          return 'spec';
        }
      });
      setIsRolling(false);
    }, 300);
  }, [specs]);

  // Handle card click - open modal
  const handleCardClick = useCallback((img: PlotImage) => {
    setModalImage(img);
  }, []);

  // Close description when clicking anywhere
  const handleContainerClick = useCallback((e: React.MouseEvent) => {
    const target = e.target as HTMLElement;
    if (target.closest('[data-description-btn]')) return;
    if (descriptionOpen) setDescriptionOpen(false);
    if (openImageTooltip) setOpenImageTooltip(null);
  }, [descriptionOpen, openImageTooltip]);

  // Load specs on mount
  useEffect(() => {
    const fetchSpecs = async () => {
      try {
        const response = await fetch(`${API_URL}/specs`);
        if (!response.ok) throw new Error('Failed to fetch specs');
        const data = await response.json();
        const specsArray = Array.isArray(data) ? data : data.specs || [];
        const specIds = specsArray.map((s: SpecInfo) => s.id);
        setSpecs(specIds);
        setSpecsData(specsArray);

        const urlParams = new URLSearchParams(window.location.search);
        const specFromUrl = urlParams.get('spec');
        const libraryFromUrl = urlParams.get('library');

        if (libraryFromUrl && LIBRARIES.includes(libraryFromUrl)) {
          setViewMode('library');
          setSelectedLibrary(libraryFromUrl);
        } else if (specFromUrl && specIds.includes(specFromUrl)) {
          setSelectedSpec(specFromUrl);
        } else if (specIds.length > 0) {
          const randomIndex = Math.floor(Math.random() * specIds.length);
          setSelectedSpec(specIds[randomIndex]);
        }
      } catch (err) {
        setError(`Error loading specs: ${err}`);
      } finally {
        setSpecsLoaded(true);
      }
    };
    fetchSpecs();
  }, []);

  // Load libraries data on mount
  useEffect(() => {
    const fetchLibraries = async () => {
      try {
        const response = await fetch(`${API_URL}/libraries`);
        if (!response.ok) throw new Error('Failed to fetch libraries');
        const data = await response.json();
        setLibrariesData(data.libraries || []);
      } catch (err) {
        console.error('Error loading libraries:', err);
      }
    };
    fetchLibraries();
  }, []);

  // Update library description when selected library changes
  useEffect(() => {
    if (viewMode === 'library' && selectedLibrary && librariesData.length > 0) {
      const lib = librariesData.find((l) => l.id === selectedLibrary);
      if (lib) {
        setLibraryDescription(lib.description || '');
        setLibraryDocsUrl(lib.documentation_url || '');
      }
      setDescriptionOpen(false);
    }
  }, [selectedLibrary, librariesData, viewMode]);

  // Update URL and document title when spec/library changes
  useEffect(() => {
    const url = new URL(window.location.href);
    if (viewMode === 'spec' && selectedSpec && specsLoaded) {
      url.searchParams.delete('library');
      url.searchParams.set('spec', selectedSpec);
      window.history.replaceState({}, '', url.toString());
      document.title = `${selectedSpec} | pyplots.ai`;
      setDescriptionOpen(false);
      if (typeof window.plausible === 'function') {
        window.plausible('pageview', { u: url.toString() });
      }
    } else if (viewMode === 'library' && selectedLibrary) {
      url.searchParams.delete('spec');
      url.searchParams.set('library', selectedLibrary);
      window.history.replaceState({}, '', url.toString());
      document.title = `${selectedLibrary} plots | pyplots.ai`;
      if (typeof window.plausible === 'function') {
        window.plausible('pageview', { u: url.toString() });
      }
    }
  }, [selectedSpec, selectedLibrary, specsLoaded, viewMode]);

  // Load images when spec changes (spec view mode)
  useEffect(() => {
    setOpenImageTooltip(null);

    if (viewMode !== 'spec' || !selectedSpec) {
      if (specsLoaded && viewMode === 'spec') setLoading(false);
      return;
    }

    const fetchImages = async () => {
      setLoading(true);
      try {
        const [imagesRes, specRes] = await Promise.all([
          fetch(`${API_URL}/specs/${selectedSpec}/images`),
          fetch(`${API_URL}/specs/${selectedSpec}`),
        ]);

        if (!imagesRes.ok) throw new Error('Failed to fetch images');
        const imagesData = await imagesRes.json();

        let description = '';
        const codeByLibrary: Record<string, string> = {};
        if (specRes.ok) {
          const specData = await specRes.json();
          description = specData.description || '';
          for (const impl of specData.implementations || []) {
            if (impl.code) codeByLibrary[impl.library_id] = impl.code;
          }
        }
        setSpecDescription(description);

        const imagesWithCode = (imagesData.images as PlotImage[]).map((img) => ({
          ...img,
          code: codeByLibrary[img.library] || undefined,
        }));
        const shuffled = shuffleArray<PlotImage>(imagesWithCode);
        setAllImages(shuffled);
        setDisplayedImages(shuffled.slice(0, BATCH_SIZE));
        setHasMore(shuffled.length > BATCH_SIZE);
      } catch (err) {
        setError(`Error loading images: ${err}`);
      } finally {
        setLoading(false);
        navigation.resetTransition();
      }
    };
    fetchImages();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedSpec, specsLoaded, viewMode]);

  // Load images when library changes (library view mode)
  useEffect(() => {
    setOpenImageTooltip(null);

    if (viewMode !== 'library' || !selectedLibrary) return;

    const fetchLibraryImages = async () => {
      setLoading(true);
      try {
        const res = await fetch(`${API_URL}/libraries/${selectedLibrary}/images`);
        if (!res.ok) throw new Error('Failed to fetch library images');
        const data = await res.json();
        const shuffled = shuffleArray<PlotImage>(data.images || []);
        setAllImages(shuffled);
        setDisplayedImages(shuffled.slice(0, BATCH_SIZE));
        setHasMore(shuffled.length > BATCH_SIZE);
      } catch (err) {
        setError(`Error loading library images: ${err}`);
      } finally {
        setLoading(false);
        navigation.resetTransition();
      }
    };
    fetchLibraryImages();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedLibrary, viewMode]);

  return (
    <Box
      onTouchStart={handleTouchStart}
      onTouchEnd={handleTouchEnd}
      onClick={handleContainerClick}
      sx={{ minHeight: '100vh', bgcolor: '#fafafa', py: 5 }}
    >
      <Container maxWidth={false} sx={{ px: { xs: 4, sm: 8, lg: 12 } }}>
        <Header />

        {error && (
          <Alert severity="error" sx={{ mb: 4, maxWidth: 500, mx: 'auto' }}>
            {error}
          </Alert>
        )}

        {(selectedSpec || viewMode === 'library') && (
          <>
            <NavigationBar
              viewMode={viewMode}
              selectedSpec={selectedSpec}
              selectedLibrary={selectedLibrary}
              specDescription={specDescription}
              libraryDescription={libraryDescription}
              libraryDocsUrl={libraryDocsUrl}
              descriptionOpen={descriptionOpen}
              isRolling={isRolling}
              isShuffling={navigation.isShuffling}
              onToggleViewMode={toggleViewMode}
              onMenuOpen={setMenuAnchor}
              onDescriptionToggle={() => setDescriptionOpen(!descriptionOpen)}
              shuffleSpec={navigation.shuffleSpec}
              goToPrevSpec={navigation.goToPrevSpec}
              goToNextSpec={navigation.goToNextSpec}
              shuffleLibrary={navigation.shuffleLibrary}
              goToPrevLibrary={navigation.goToPrevLibrary}
              goToNextLibrary={navigation.goToNextLibrary}
            />

            <SelectionMenu
              anchorEl={menuAnchor}
              open={Boolean(menuAnchor)}
              onClose={() => setMenuAnchor(null)}
              viewMode={viewMode}
              sortedSpecs={navigation.sortedSpecs}
              selectedSpec={selectedSpec}
              selectedLibrary={selectedLibrary}
              onSelectSpec={setSelectedSpec}
              onSelectLibrary={setSelectedLibrary}
            />
          </>
        )}

        <ImagesGrid
          images={displayedImages}
          viewMode={viewMode}
          selectedSpec={selectedSpec}
          selectedLibrary={selectedLibrary}
          loading={loading}
          hasMore={hasMore}
          isTransitioning={navigation.isTransitioning}
          librariesData={librariesData}
          specsData={specsData}
          openTooltip={openImageTooltip}
          loadMoreRef={loadMoreRef}
          onTooltipToggle={setOpenImageTooltip}
          onCardClick={handleCardClick}
        />

        {!loading && specsLoaded && specs.length === 0 && (
          <Alert severity="warning" sx={{ maxWidth: 400, mx: 'auto' }}>
            No specs found.
          </Alert>
        )}

        <Footer />
      </Container>

      <FullscreenModal
        image={modalImage}
        selectedSpec={selectedSpec}
        onClose={() => setModalImage(null)}
      />
    </Box>
  );
}

export default App;
