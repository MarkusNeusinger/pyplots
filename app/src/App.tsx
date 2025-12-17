import { useState, useEffect, useRef, useCallback, useMemo } from 'react';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import Link from '@mui/material/Link';
import Alert from '@mui/material/Alert';
import Card from '@mui/material/Card';
import CardMedia from '@mui/material/CardMedia';
import Grid from '@mui/material/Grid';
import Chip from '@mui/material/Chip';
import IconButton from '@mui/material/IconButton';
import Modal from '@mui/material/Modal';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import TextField from '@mui/material/TextField';
import InputAdornment from '@mui/material/InputAdornment';
import Tooltip from '@mui/material/Tooltip';
import SearchIcon from '@mui/icons-material/Search';
import ShuffleIcon from '@mui/icons-material/Shuffle';
import CloseIcon from '@mui/icons-material/Close';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import DownloadIcon from '@mui/icons-material/Download';
import CodeIcon from '@mui/icons-material/Code';
import ImageIcon from '@mui/icons-material/Image';
import SubjectIcon from '@mui/icons-material/Subject';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { oneLight } from 'react-syntax-highlighter/dist/esm/styles/prism';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const GITHUB_URL = 'https://github.com/MarkusNeusinger/pyplots'; // pyplots repo

interface PlotImage {
  library: string;
  url: string;
  thumb?: string;
  html?: string;
  code?: string;
}

function App() {
  const [specs, setSpecs] = useState<string[]>([]);
  const [selectedSpec, setSelectedSpec] = useState<string>('');
  const [images, setImages] = useState<PlotImage[]>([]);
  const [loading, setLoading] = useState(true);
  const [specsLoaded, setSpecsLoaded] = useState(false);
  const [error, setError] = useState<string>('');
  const [isShuffling, setIsShuffling] = useState(false);
  const [modalImage, setModalImage] = useState<PlotImage | null>(null);
  const [menuAnchor, setMenuAnchor] = useState<HTMLElement | null>(null);
  const [searchFilter, setSearchFilter] = useState('');
  const [highlightedIndex, setHighlightedIndex] = useState(0);
  const [specDescription, setSpecDescription] = useState<string>('');
  const [descriptionOpen, setDescriptionOpen] = useState(false);
  const [showCode, setShowCode] = useState(false);
  const [blinkCodeButton, setBlinkCodeButton] = useState(false);
  const [isTransitioning, setIsTransitioning] = useState(false);
  const shuffleButtonRef = useRef<HTMLButtonElement>(null);
  const searchInputRef = useRef<HTMLInputElement>(null);
  const menuItemRefs = useRef<(HTMLLIElement | null)[]>([]);
  const touchStartX = useRef<number | null>(null);
  const lastTapTime = useRef<number>(0);

  // Fisher-Yates shuffle algorithm
  const shuffleArray = <T,>(array: T[]): T[] => {
    const shuffled = [...array];
    for (let i = shuffled.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    return shuffled;
  };

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
  }, [specs, selectedSpec]);

  // Navigate to previous spec (alphabetically) - with fade transition
  const goToPrevSpec = useCallback(() => {
    if (sortedSpecs.length <= 1 || isTransitioning) return;
    setIsTransitioning(true);
    setTimeout(() => {
      const currentIndex = sortedSpecs.indexOf(selectedSpec);
      const prevIndex = currentIndex <= 0 ? sortedSpecs.length - 1 : currentIndex - 1;
      setSelectedSpec(sortedSpecs[prevIndex]);
    }, 150);
  }, [sortedSpecs, selectedSpec, isTransitioning]);

  // Navigate to next spec (alphabetically) - with fade transition
  const goToNextSpec = useCallback(() => {
    if (sortedSpecs.length <= 1 || isTransitioning) return;
    setIsTransitioning(true);
    setTimeout(() => {
      const currentIndex = sortedSpecs.indexOf(selectedSpec);
      const nextIndex = currentIndex >= sortedSpecs.length - 1 ? 0 : currentIndex + 1;
      setSelectedSpec(sortedSpecs[nextIndex]);
    }, 150);
  }, [sortedSpecs, selectedSpec, isTransitioning]);

  // Touch handlers for swipe and double-tap
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
        goToPrevSpec(); // Swipe right = previous
      } else {
        goToNextSpec(); // Swipe left = next
      }
    } else {
      // Check for double tap
      const now = Date.now();
      if (now - lastTapTime.current < 300) {
        shuffleSpec();
      }
      lastTapTime.current = now;
    }
    touchStartX.current = null;
  }, [modalImage, goToPrevSpec, goToNextSpec, shuffleSpec]);

  // Copy code to clipboard
  const copyCodeToClipboard = useCallback(() => {
    if (modalImage?.code) {
      navigator.clipboard.writeText(modalImage.code);
    }
  }, [modalImage]);

  // Download image via backend proxy
  const downloadImage = useCallback(() => {
    if (modalImage?.library && selectedSpec) {
      const link = document.createElement('a');
      link.href = `${API_URL}/download/${selectedSpec}/${modalImage.library}`;
      link.download = `${selectedSpec}-${modalImage.library}.png`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  }, [modalImage, selectedSpec]);

  // Handle card click - open modal and trigger code button animation
  const handleCardClick = useCallback((img: PlotImage) => {
    setModalImage(img);
    setShowCode(false);
    setBlinkCodeButton(true);
    setTimeout(() => setBlinkCodeButton(false), 1000);
  }, []);

  // Memoize syntax-highlighted code to avoid expensive re-renders
  const highlightedCode = useMemo(() => {
    if (!modalImage?.code) return null;
    return (
      <SyntaxHighlighter
        language="python"
        style={oneLight}
        customStyle={{
          margin: 0,
          fontSize: '0.85rem',
          fontFamily: '"JetBrains Mono", monospace',
          background: 'transparent',
        }}
      >
        {modalImage.code}
      </SyntaxHighlighter>
    );
  }, [modalImage?.code]);

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      const isTyping = document.activeElement?.tagName === 'INPUT' || document.activeElement?.tagName === 'TEXTAREA';

      if (e.code === 'Space' && !modalImage && !menuAnchor && !isTyping) {
        e.preventDefault();
        shuffleSpec();
      }
      if (e.code === 'ArrowLeft' && !modalImage && !menuAnchor && !isTyping) {
        e.preventDefault();
        goToPrevSpec();
      }
      if (e.code === 'ArrowRight' && !modalImage && !menuAnchor && !isTyping) {
        e.preventDefault();
        goToNextSpec();
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
  }, [modalImage, menuAnchor, shuffleSpec, goToPrevSpec, goToNextSpec]);

  // Load specs on mount
  useEffect(() => {
    const fetchSpecs = async () => {
      try {
        const response = await fetch(`${API_URL}/specs`);
        if (!response.ok) throw new Error('Failed to fetch specs');
        const data = await response.json();
        // API returns array of {id, title, ...} objects - extract IDs
        const specIds = Array.isArray(data) ? data.map((s: { id: string }) => s.id) : data.specs || [];
        setSpecs(specIds);

        // Check URL for spec parameter
        const urlParams = new URLSearchParams(window.location.search);
        const specFromUrl = urlParams.get('spec');

        if (specFromUrl && specIds.includes(specFromUrl)) {
          setSelectedSpec(specFromUrl);
        } else if (specIds.length > 0) {
          // Select random spec
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

  // Update URL when spec changes
  useEffect(() => {
    if (selectedSpec && specsLoaded) {
      const url = new URL(window.location.href);
      url.searchParams.set('spec', selectedSpec);
      window.history.replaceState({}, '', url.toString());
      setDescriptionOpen(false); // Close description tooltip when spec changes
    }
  }, [selectedSpec, specsLoaded]);

  // Load images when spec changes
  useEffect(() => {
    if (!selectedSpec) {
      if (specsLoaded) {
        setLoading(false);
      }
      return;
    }

    const fetchImages = async () => {
      setLoading(true);
      try {
        // Fetch images and spec details in parallel
        const [imagesRes, specRes] = await Promise.all([
          fetch(`${API_URL}/specs/${selectedSpec}/images`),
          fetch(`${API_URL}/specs/${selectedSpec}`),
        ]);

        if (!imagesRes.ok) throw new Error('Failed to fetch images');
        const imagesData = await imagesRes.json();

        // Get description and code from spec details
        let description = '';
        const codeByLibrary: Record<string, string> = {};
        if (specRes.ok) {
          const specData = await specRes.json();
          description = specData.description || '';
          for (const impl of specData.implementations || []) {
            if (impl.code) {
              codeByLibrary[impl.library_id] = impl.code;
            }
          }
        }
        setSpecDescription(description);

        // Merge code into images
        const imagesWithCode = (imagesData.images as PlotImage[]).map((img) => ({
          ...img,
          code: codeByLibrary[img.library] || undefined,
        }));
        const shuffled = shuffleArray<PlotImage>(imagesWithCode);
        setImages(shuffled);
      } catch (err) {
        setError(`Error loading images: ${err}`);
      } finally {
        setLoading(false);
        // End fade transition after images load
        setTimeout(() => setIsTransitioning(false), 50);
      }
    };

    fetchImages();
  }, [selectedSpec, specsLoaded]);

  return (
    <Box
      onTouchStart={handleTouchStart}
      onTouchEnd={handleTouchEnd}
      sx={{
        minHeight: '100vh',
        bgcolor: '#fafafa',
        py: 5,
      }}
    >
      <Container maxWidth={false} sx={{ px: { xs: 4, sm: 8, lg: 12 } }}>
        {/* Header */}
        <Box sx={{ textAlign: 'center', mb: 6 }}>
          <Link
            href="https://pyplots.ai"
            target="_blank"
            rel="noopener noreferrer"
            underline="none"
          >
            <Typography
              variant="h2"
              component="h1"
              sx={{
                fontWeight: 700,
                fontFamily: '"JetBrains Mono", monospace',
                mb: 3,
                letterSpacing: '-0.02em',
              }}
            >
              <Box component="span" sx={{ color: '#3776AB' }}>py</Box>
              <Box component="span" sx={{ color: '#FFD43B' }}>plots</Box>
              <Box component="span" sx={{ color: '#1f2937' }}>.ai</Box>
            </Typography>
          </Link>
          <Typography
            variant="body1"
            sx={{
              maxWidth: 560,
              mx: 'auto',
              lineHeight: 1.8,
              fontFamily: '"JetBrains Mono", monospace',
              color: '#6b7280',
              fontSize: '1rem',
            }}
          >
            library-agnostic, ai-powered python plotting examples. automatically generated, tested, and maintained.
          </Typography>
        </Box>

        {/* Error Display */}
        {error && (
          <Alert severity="error" sx={{ mb: 4, maxWidth: 500, mx: 'auto' }}>
            {error}
          </Alert>
        )}

        {/* Spec Title with Shuffle - visible even during loading */}
        {selectedSpec && (
          <Box
            sx={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              gap: 1.5,
              mb: 5,
            }}
          >
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              {/* Invisible spacer for visual balance */}
              <Box sx={{ width: 28, visibility: 'hidden' }} />
              <Chip
                data-spec-chip
                label={selectedSpec}
                variant="outlined"
                onClick={(e) => setMenuAnchor(e.currentTarget)}
                onKeyDown={(e) => {
                  // Prevent space from triggering click (space is for shuffle)
                  if (e.code === 'Space') {
                    e.preventDefault();
                  }
                }}
                sx={{
                  fontSize: '0.95rem',
                  fontWeight: 600,
                  fontFamily: '"JetBrains Mono", monospace',
                  color: '#3776AB',
                  borderColor: '#3776AB',
                  bgcolor: '#f9fafb',
                  py: 2,
                  px: 0.5,
                  cursor: 'pointer',
                  '&:hover': {
                    bgcolor: '#e8f4fc',
                  },
                }}
              />
              <Tooltip
                title={specDescription}
                arrow
                placement="bottom"
                open={descriptionOpen}
                disableFocusListener
                disableHoverListener
                disableTouchListener
                slotProps={{
                  tooltip: {
                    sx: {
                      maxWidth: { xs: '80vw', sm: 400 },
                      fontFamily: '"JetBrains Mono", monospace',
                      fontSize: '0.8rem',
                    },
                  },
                }}
              >
                <IconButton
                  size="small"
                  onClick={() => setDescriptionOpen(!descriptionOpen)}
                  sx={{
                    ml: 0.5,
                    color: descriptionOpen ? '#3776AB' : '#9ca3af',
                    '&:hover': {
                      color: '#3776AB',
                      bgcolor: 'transparent',
                    },
                  }}
                >
                  <SubjectIcon sx={{ fontSize: 18 }} />
                </IconButton>
              </Tooltip>
            </Box>
            <Menu
              anchorEl={menuAnchor}
              open={Boolean(menuAnchor)}
              onClose={() => {
                setMenuAnchor(null);
                setSearchFilter('');
              }}
              anchorOrigin={{
                vertical: 'bottom',
                horizontal: 'center',
              }}
              transformOrigin={{
                vertical: 'top',
                horizontal: 'center',
              }}
              autoFocus={false}
              disableAutoFocus
              disableEnforceFocus
              TransitionProps={{
                onEntered: () => {
                  // Don't auto-focus on touch devices to avoid keyboard popup
                  const isTouchDevice = window.matchMedia('(hover: none)').matches;
                  if (!isTouchDevice) {
                    searchInputRef.current?.focus();
                  }
                },
              }}
              PaperProps={{
                sx: {
                  mt: 1,
                  maxHeight: 350,
                  minWidth: 220,
                  fontFamily: '"JetBrains Mono", monospace',
                },
              }}
            >
              <Box sx={{ px: 1.5, py: 1, position: 'sticky', top: 0, bgcolor: '#fff', zIndex: 1 }}>
                <TextField
                  size="small"
                  placeholder="search..."
                  value={searchFilter}
                  onChange={(e) => {
                    setSearchFilter(e.target.value);
                    setHighlightedIndex(0);
                  }}
                  onKeyDown={(e) => {
                    const filtered = sortedSpecs.filter((s) => s.toLowerCase().includes(searchFilter.toLowerCase()));

                    if (e.key === 'Escape') {
                      setMenuAnchor(null);
                      setSearchFilter('');
                      setHighlightedIndex(0);
                      return;
                    }
                    if (e.key === 'ArrowDown') {
                      e.preventDefault();
                      const newIndex = filtered.length > 0 ? (highlightedIndex + 1) % filtered.length : 0;
                      setHighlightedIndex(newIndex);
                      menuItemRefs.current[newIndex]?.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
                      return;
                    }
                    if (e.key === 'ArrowUp') {
                      e.preventDefault();
                      const newIndex = filtered.length > 0 ? (highlightedIndex - 1 + filtered.length) % filtered.length : 0;
                      setHighlightedIndex(newIndex);
                      menuItemRefs.current[newIndex]?.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
                      return;
                    }
                    // Stop propagation for all other keys (including letters) to prevent Menu from handling them
                    e.stopPropagation();
                    if (e.key === 'Enter') {
                      if (filtered.length > 0 && highlightedIndex < filtered.length) {
                        setSelectedSpec(filtered[highlightedIndex]);
                        setMenuAnchor(null);
                        setSearchFilter('');
                        setHighlightedIndex(0);
                      }
                    }
                  }}
                  inputRef={searchInputRef}
                  fullWidth
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position="start">
                        <SearchIcon sx={{ fontSize: 18, color: '#9ca3af' }} />
                      </InputAdornment>
                    ),
                    sx: {
                      fontSize: '0.85rem',
                      fontFamily: '"JetBrains Mono", monospace',
                    },
                  }}
                />
              </Box>
              {sortedSpecs
                .filter((spec) => spec.toLowerCase().includes(searchFilter.toLowerCase()))
                .map((spec, index) => (
                  <MenuItem
                    key={spec}
                    ref={(el) => { menuItemRefs.current[index] = el; }}
                    onClick={() => {
                      setSelectedSpec(spec);
                      setMenuAnchor(null);
                      setSearchFilter('');
                      setHighlightedIndex(0);
                    }}
                    onMouseEnter={() => setHighlightedIndex(index)}
                    sx={{
                      fontSize: '0.85rem',
                      fontFamily: '"JetBrains Mono", monospace',
                      bgcolor: index === highlightedIndex ? '#e8f4fc' : 'transparent',
                      '&:hover': {
                        bgcolor: '#e8f4fc',
                      },
                    }}
                  >
                    {spec}
                  </MenuItem>
                ))}
            </Menu>

            <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
              <Tooltip title="Previous (← / Swipe right)" arrow placement="bottom">
                <IconButton
                  onClick={goToPrevSpec}
                  size="small"
                  aria-label="Previous spec"
                  sx={{
                    color: '#9ca3af',
                    '&:hover': {
                      color: '#3776AB',
                      bgcolor: '#e8f4fc',
                    },
                  }}
                >
                  <ChevronLeftIcon />
                </IconButton>
              </Tooltip>
              <Tooltip title="Random (Space / Double-tap)" arrow placement="bottom">
                <IconButton
                  ref={shuffleButtonRef}
                  onClick={shuffleSpec}
                  size="small"
                  aria-label="Shuffle to a different random spec"
                  sx={{
                    color: '#3776AB',
                    transition: 'transform 0.5s ease',
                    transform: isShuffling ? 'rotate(180deg)' : 'rotate(0deg)',
                    '&:hover': {
                      color: '#2c5d8a',
                      bgcolor: '#e8f4fc',
                    },
                  }}
                >
                  <ShuffleIcon />
                </IconButton>
              </Tooltip>
              <Tooltip title="Next (→ / Swipe left)" arrow placement="bottom">
                <IconButton
                  onClick={goToNextSpec}
                  size="small"
                  aria-label="Next spec"
                  sx={{
                    color: '#9ca3af',
                    '&:hover': {
                      color: '#3776AB',
                      bgcolor: '#e8f4fc',
                    },
                  }}
                >
                  <ChevronRightIcon />
                </IconButton>
              </Tooltip>
            </Box>
          </Box>
        )}

        {/* Content */}
        <Box>
          {/* Loading State - only show on initial load, not during navigation */}
          {loading && !isTransitioning && images.length === 0 && (
            <Box
              sx={{
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                my: 8,
                opacity: 0,
                animation: 'fadeInDelayed 1.5s ease-out 0.3s forwards',
                '@keyframes fadeInDelayed': {
                  '0%': { opacity: 0 },
                  '100%': { opacity: 1 },
                },
              }}
            >
              <Box
                sx={{
                  position: 'relative',
                  width: 100,
                  height: 16,
                  '&::before': {
                    content: '""',
                    position: 'absolute',
                    width: 16,
                    height: 16,
                    borderRadius: '50%',
                    background: '#3776AB',
                    boxShadow: '32px 0 #3776AB',
                    left: 0,
                    top: 0,
                    animation: 'ballMoveX 2s linear infinite',
                  },
                  '&::after': {
                    content: '""',
                    position: 'absolute',
                    width: 16,
                    height: 16,
                    borderRadius: '50%',
                    background: '#3776AB',
                    left: 0,
                    top: 0,
                    transform: 'translateX(64px) scale(1)',
                    zIndex: 2,
                    animation: 'trfLoader 2s linear infinite',
                  },
                  '@keyframes trfLoader': {
                    '0%, 5%': {
                      transform: 'translateX(64px) scale(1)',
                      background: '#3776AB',
                    },
                    '10%': {
                      transform: 'translateX(64px) scale(1)',
                      background: '#FFD43B',
                    },
                    '40%': {
                      transform: 'translateX(32px) scale(1.5)',
                      background: '#FFD43B',
                    },
                    '90%, 95%': {
                      transform: 'translateX(0px) scale(1)',
                      background: '#FFD43B',
                    },
                    '100%': {
                      transform: 'translateX(0px) scale(1)',
                      background: '#3776AB',
                    },
                  },
                  '@keyframes ballMoveX': {
                    '0%, 10%': { transform: 'translateX(0)' },
                    '90%, 100%': { transform: 'translateX(32px)' },
                  },
                }}
              />
            </Box>
          )}

          {/* Images - show even during loading if we have images (for smooth transitions) */}
          {selectedSpec && (images.length > 0 || !loading) && (
            <Box>
            {images.length === 0 ? (
              <Alert
                severity="info"
                sx={{
                  maxWidth: 400,
                  mx: 'auto',
                  bgcolor: '#f9fafb',
                  border: '1px solid #e5e7eb',
                  '& .MuiAlert-icon': { color: '#9ca3af' },
                }}
              >
                No images found for this spec.
              </Alert>
            ) : (
              <Grid container spacing={3} justifyContent="center" sx={{
                  maxWidth: 1800,
                  mx: 'auto',
                  minHeight: '60vh',
                  opacity: isTransitioning ? 0 : 1,
                  transition: 'opacity 0.15s ease-in-out',
                }}>
                {images.map((img, index) => (
                  <Grid size={{ xs: 12, sm: 6, lg: 4 }} key={img.library} sx={{ maxWidth: 600 }}>
                    <Box
                      sx={{
                        animation: 'fadeIn 0.6s ease-out',
                        animationDelay: `${index * 0.1}s`,
                        animationFillMode: 'backwards',
                        '@keyframes fadeIn': {
                          from: { opacity: 0, transform: 'translateY(20px)' },
                          to: { opacity: 1, transform: 'translateY(0)' },
                        },
                      }}
                    >
                      <Card
                        elevation={0}
                        onClick={() => handleCardClick(img)}
                        onKeyDown={(e) => {
                          if (e.key === 'Enter' || e.key === ' ') {
                            e.preventDefault();
                            handleCardClick(img);
                          }
                        }}
                        tabIndex={0}
                        role="button"
                        aria-label={`View ${img.library} plot in fullscreen`}
                        sx={{
                          borderRadius: 3,
                          overflow: 'hidden',
                          border: '2px solid rgba(55, 118, 171, 0.2)',
                          boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
                          transition: 'all 0.3s ease',
                          cursor: 'pointer',
                          '&:hover': {
                            border: '2px solid rgba(55, 118, 171, 0.4)',
                            boxShadow: '0 8px 30px rgba(0,0,0,0.15)',
                            transform: 'scale(1.03)',
                          },
                        }}
                      >
                        <CardMedia
                          component="img"
                          image={img.thumb || img.url}
                          alt={`${selectedSpec} - ${img.library}`}
                          sx={{
                            width: '100%',
                            aspectRatio: '16 / 10',
                            objectFit: 'contain',
                            bgcolor: '#fff',
                          }}
                          onError={(e) => {
                            const target = e.target as HTMLImageElement;
                            target.style.display = 'none';
                          }}
                        />
                      </Card>
                      {/* Library label below card */}
                      <Typography
                        sx={{
                          mt: 1.5,
                          textAlign: 'center',
                          fontSize: '0.8rem',
                          fontWeight: 600,
                          fontFamily: '"JetBrains Mono", monospace',
                          color: '#9ca3af',
                          textTransform: 'lowercase',
                        }}
                      >
                        {img.library}
                      </Typography>
                    </Box>
                  </Grid>
                ))}
              </Grid>
            )}
            </Box>
          )}
        </Box>

        {/* No specs available */}
        {!loading && specsLoaded && specs.length === 0 && (
          <Alert severity="warning" sx={{ maxWidth: 400, mx: 'auto' }}>
            No specs found.
          </Alert>
        )}

        {/* Footer */}
        <Box sx={{ textAlign: 'center', mt: 8, pt: 5, borderTop: '1px solid #f3f4f6' }}>
          <Box
            sx={{
              display: 'flex',
              justifyContent: 'center',
              alignItems: 'center',
              gap: 1,
              fontSize: '0.8rem',
              fontFamily: '"JetBrains Mono", monospace',
              color: '#9ca3af',
            }}
          >
            <Link
              href="https://www.linkedin.com/in/markus-neusinger/"
              target="_blank"
              rel="noopener noreferrer"
              sx={{
                color: '#9ca3af',
                textDecoration: 'none',
                '&:hover': { color: '#6b7280' },
              }}
            >
              markus neusinger
            </Link>
            <span>·</span>
            <Link
              href={GITHUB_URL}
              target="_blank"
              rel="noopener noreferrer"
              sx={{
                color: '#9ca3af',
                textDecoration: 'none',
                '&:hover': { color: '#6b7280' },
              }}
            >
              github
            </Link>
          </Box>
        </Box>
      </Container>

      {/* Fullscreen Modal */}
      <Modal
        open={!!modalImage}
        onClose={() => {
          setModalImage(null);
          setShowCode(false);
        }}
        aria-labelledby="plot-modal-title"
        disableRestoreFocus
        sx={{
          display: 'flex',
          alignItems: { xs: 'flex-start', sm: 'center' },
          justifyContent: 'center',
          pt: { xs: 5, sm: 0 },
          '@media (orientation: landscape)': {
            alignItems: 'center',
            pt: 0,
          },
        }}
      >
        <Box
          sx={{
            position: 'relative',
            maxWidth: '90vw',
            maxHeight: { xs: '92vh', sm: '90vh' },
            outline: 'none',
          }}
          role="dialog"
        >
          {/* Modal Header - Close only */}
          <Box sx={{ position: 'absolute', top: { xs: -36, sm: -40 }, right: 0, zIndex: 10 }}>
            <IconButton
              onClick={() => {
                setModalImage(null);
                setShowCode(false);
              }}
              aria-label="Close"
              sx={{
                color: '#fff',
                '&:hover': { bgcolor: 'rgba(255,255,255,0.1)' },
              }}
            >
              <CloseIcon />
            </IconButton>
          </Box>

          {/* Modal Content */}
          {modalImage && (
            <Box sx={{ position: 'relative' }}>
              {/* Code View - only rendered when needed */}
              {showCode && (
                <Box
                  sx={{
                    position: 'relative',
                    bgcolor: '#fafafa',
                    borderRadius: '8px',
                    width: 'min(90vw, calc(85vh * 16 / 9))',
                    height: 'min(85vh, calc(90vw * 9 / 16))',
                    overflow: 'hidden',
                    boxShadow: 'none',
                    '@media (orientation: portrait)': {
                      height: '85vh',
                    },
                  }}
                >
                  {/* Button bar */}
                  <Box
                    sx={{
                      position: 'absolute',
                      top: 6,
                      right: 16,
                      display: 'flex',
                      gap: 0.5,
                      zIndex: 1,
                    }}
                  >
                    <Box
                      onClick={() => setShowCode(false)}
                      sx={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: 0.5,
                        px: 1,
                        py: 0.5,
                        borderRadius: 1,
                        cursor: 'pointer',
                        color: '#6b7280',
                        bgcolor: 'rgba(255,255,255,0.9)',
                        fontSize: '0.85rem',
                        fontFamily: '"JetBrains Mono", monospace',
                        '&:hover': { color: '#3776AB', bgcolor: '#fff' },
                      }}
                    >
                      <ImageIcon sx={{ fontSize: 20 }} />
                      plot
                    </Box>
                    <Box
                      onClick={copyCodeToClipboard}
                      sx={{
                        display: 'flex',
                        alignItems: 'center',
                        px: 1,
                        py: 0.5,
                        borderRadius: 1,
                        cursor: 'pointer',
                        color: '#6b7280',
                        bgcolor: 'rgba(255,255,255,0.9)',
                        '&:hover': { color: '#1f2937', bgcolor: '#fff' },
                      }}
                    >
                      <ContentCopyIcon sx={{ fontSize: 20 }} />
                    </Box>
                  </Box>
                  <Box
                    sx={{
                      height: '100%',
                      overflow: 'auto',
                      p: 3,
                    }}
                  >
                    {highlightedCode}
                  </Box>
                </Box>
              )}
              {/* PNG image - always rendered, hidden when code is shown */}
              <Box
                sx={{
                  position: 'relative',
                  display: showCode ? 'none' : 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  bgcolor: '#fff',
                  borderRadius: '8px',
                  width: 'min(90vw, calc(85vh * 16 / 9))',
                  height: 'min(85vh, calc(90vw * 9 / 16))',
                  overflow: 'hidden',
                  boxShadow: 'none',
                }}
              >
                {/* Button bar */}
                <Box
                  sx={{
                    position: 'absolute',
                    top: 6,
                    right: 16,
                    display: 'flex',
                    gap: 0.5,
                    zIndex: 1,
                  }}
                >
                  {modalImage?.code && (
                    <Box
                      onClick={() => setShowCode(true)}
                      sx={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: 0.5,
                        px: 1,
                        py: 0.5,
                        borderRadius: 1,
                        cursor: 'pointer',
                        color: '#6b7280',
                        bgcolor: 'rgba(255,255,255,0.9)',
                        fontSize: '0.85rem',
                        fontFamily: '"JetBrains Mono", monospace',
                        '&:hover': { color: '#3776AB', bgcolor: '#fff' },
                        ...(blinkCodeButton && {
                          animation: 'bounce 0.6s ease-in-out',
                          '@keyframes bounce': {
                            '0%, 100%': { transform: 'translateY(0)' },
                            '25%': { transform: 'translateY(-4px)' },
                            '50%': { transform: 'translateY(0)' },
                            '75%': { transform: 'translateY(-2px)' },
                          },
                        }),
                      }}
                    >
                      <CodeIcon sx={{ fontSize: 20 }} />
                      code
                    </Box>
                  )}
                  <Box
                    onClick={downloadImage}
                    sx={{
                      display: 'flex',
                      alignItems: 'center',
                      px: 1,
                      py: 0.5,
                      borderRadius: 1,
                      cursor: 'pointer',
                      color: '#6b7280',
                      bgcolor: 'rgba(255,255,255,0.9)',
                      '&:hover': { color: '#1f2937', bgcolor: '#fff' },
                      ...(blinkCodeButton && {
                        animation: 'bounce 0.6s ease-in-out',
                        '@keyframes bounce': {
                          '0%, 100%': { transform: 'translateY(0)' },
                          '25%': { transform: 'translateY(-4px)' },
                          '50%': { transform: 'translateY(0)' },
                          '75%': { transform: 'translateY(-2px)' },
                        },
                      }),
                    }}
                  >
                    <DownloadIcon sx={{ fontSize: 20 }} />
                  </Box>
                </Box>
                <img
                  src={modalImage.url}
                  alt={`${selectedSpec} - ${modalImage.library}`}
                  style={{
                    maxWidth: '100%',
                    maxHeight: '100%',
                    objectFit: 'contain',
                    borderRadius: '8px',
                  }}
                />
              </Box>
              <Typography
                id="plot-modal-title"
                sx={{
                  textAlign: 'center',
                  mt: 2,
                  color: '#fff',
                  fontWeight: 600,
                  fontFamily: '"JetBrains Mono", monospace',
                  fontSize: '1rem',
                }}
              >
                {modalImage.library}
              </Typography>
            </Box>
          )}
        </Box>
      </Modal>
    </Box>
  );
}

export default App;
