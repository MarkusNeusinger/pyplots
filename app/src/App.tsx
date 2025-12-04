import { useState, useEffect, useRef, useCallback } from 'react';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import Link from '@mui/material/Link';
import Alert from '@mui/material/Alert';
import CircularProgress from '@mui/material/CircularProgress';
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
import SearchIcon from '@mui/icons-material/Search';
import ShuffleIcon from '@mui/icons-material/Shuffle';
import CloseIcon from '@mui/icons-material/Close';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const GITHUB_URL = 'https://github.com/MarkusNeusinger/pyplots'; // pyplots repo

interface PlotImage {
  library: string;
  url: string;
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
  const shuffleButtonRef = useRef<HTMLButtonElement>(null);
  const searchInputRef = useRef<HTMLInputElement>(null);
  const menuItemRefs = useRef<(HTMLLIElement | null)[]>([]);

  // Fisher-Yates shuffle algorithm
  const shuffleArray = <T,>(array: T[]): T[] => {
    const shuffled = [...array];
    for (let i = shuffled.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    return shuffled;
  };

  // Shuffle to a different random spec
  const shuffleSpec = useCallback(() => {
    if (specs.length <= 1) return;
    setIsShuffling(true);
    setTimeout(() => setIsShuffling(false), 300);
    const otherSpecs = specs.filter((s) => s !== selectedSpec);
    const randomIndex = Math.floor(Math.random() * otherSpecs.length);
    setSelectedSpec(otherSpecs[randomIndex]);
  }, [specs, selectedSpec]);

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      const isTyping = document.activeElement?.tagName === 'INPUT' || document.activeElement?.tagName === 'TEXTAREA';

      if (e.code === 'Space' && !modalImage && !menuAnchor && !isTyping) {
        e.preventDefault();
        shuffleSpec();
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
  }, [modalImage, menuAnchor, shuffleSpec]);

  // Load specs on mount
  useEffect(() => {
    const fetchSpecs = async () => {
      try {
        const response = await fetch(`${API_URL}/specs`);
        if (!response.ok) throw new Error('Failed to fetch specs');
        const data = await response.json();
        setSpecs(data.specs);

        // Check URL for spec parameter
        const urlParams = new URLSearchParams(window.location.search);
        const specFromUrl = urlParams.get('spec');

        if (specFromUrl && data.specs.includes(specFromUrl)) {
          setSelectedSpec(specFromUrl);
        } else if (data.specs.length > 0) {
          // Select random spec
          const randomIndex = Math.floor(Math.random() * data.specs.length);
          setSelectedSpec(data.specs[randomIndex]);
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
    }
  }, [selectedSpec, specsLoaded]);

  // Load images when spec changes
  useEffect(() => {
    if (!selectedSpec) {
      setLoading(false);
      return;
    }

    const fetchImages = async () => {
      setLoading(true);
      try {
        const response = await fetch(`${API_URL}/specs/${selectedSpec}/images`);
        if (!response.ok) throw new Error('Failed to fetch images');
        const data = await response.json();
        const shuffled = shuffleArray<PlotImage>(data.images as PlotImage[]);
        setImages(shuffled);
      } catch (err) {
        setError(`Error loading images: ${err}`);
      } finally {
        setLoading(false);
      }
    };

    fetchImages();
  }, [selectedSpec]);

  return (
    <Box
      sx={{
        minHeight: '100vh',
        bgcolor: '#fff',
        py: 5,
      }}
    >
      <Container maxWidth="lg">
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
            <Chip
              data-spec-chip
              label={selectedSpec}
              variant="outlined"
              onClick={(e) => setMenuAnchor(e.currentTarget)}
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
                onEntered: () => searchInputRef.current?.focus(),
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
                    const filtered = specs.filter((s) => s.toLowerCase().includes(searchFilter.toLowerCase()));

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
              {specs
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
              <ShuffleIcon fontSize="small" />
            </IconButton>
          </Box>
        )}

        {/* Content */}
        <Box>
          {/* Loading State */}
          {loading && (
            <Box sx={{ display: 'flex', justifyContent: 'center', my: 8 }}>
              <CircularProgress size={40} sx={{ color: '#3776AB' }} />
            </Box>
          )}

          {/* Images */}
          {!loading && selectedSpec && (
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
              <Grid container spacing={3} justifyContent="center">
                {images.map((img, index) => (
                  <Grid size={{ xs: 12, sm: 6, lg: 4 }} key={img.library}>
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
                        onClick={() => setModalImage(img)}
                        onKeyDown={(e) => {
                          if (e.key === 'Enter' || e.key === ' ') {
                            e.preventDefault();
                            setModalImage(img);
                          }
                        }}
                        tabIndex={0}
                        role="button"
                        aria-label={`View ${img.library} plot in fullscreen`}
                        sx={{
                          borderRadius: 3,
                          overflow: 'hidden',
                          border: '1px solid #f3f4f6',
                          transition: 'all 0.3s ease',
                          cursor: 'pointer',
                          '&:hover': {
                            borderColor: '#e5e7eb',
                            boxShadow: '0 8px 30px rgba(0,0,0,0.12)',
                            transform: 'scale(1.03)',
                          },
                          '&:focus': {
                            outline: '2px solid #3776AB',
                            outlineOffset: '2px',
                          },
                        }}
                      >
                        <CardMedia
                          component="img"
                          image={img.url}
                          alt={`${selectedSpec} - ${img.library}`}
                          sx={{
                            width: '100%',
                            aspectRatio: '4 / 3',
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
        onClose={() => setModalImage(null)}
        aria-labelledby="plot-modal-title"
        sx={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        <Box
          sx={{
            position: 'relative',
            maxWidth: '90vw',
            maxHeight: '90vh',
            outline: 'none',
          }}
          role="dialog"
        >
          <IconButton
            onClick={() => setModalImage(null)}
            aria-label="Close fullscreen image"
            sx={{
              position: 'absolute',
              top: -40,
              right: 0,
              color: '#fff',
              '&:hover': { bgcolor: 'rgba(255,255,255,0.1)' },
            }}
          >
            <CloseIcon />
          </IconButton>
          {modalImage && (
            <Box>
              <img
                src={modalImage.url}
                alt={`${selectedSpec} - ${modalImage.library}`}
                style={{
                  maxWidth: '90vw',
                  maxHeight: '85vh',
                  objectFit: 'contain',
                  borderRadius: 8,
                  backgroundColor: '#fff',
                }}
              />
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
