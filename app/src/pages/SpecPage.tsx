import { useState, useEffect, useMemo, useCallback } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { Helmet } from 'react-helmet-async';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import Tooltip from '@mui/material/Tooltip';
import Skeleton from '@mui/material/Skeleton';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import DownloadIcon from '@mui/icons-material/Download';
import OpenInNewIcon from '@mui/icons-material/OpenInNew';

import { API_URL } from '../constants';
import { useAnalytics } from '../hooks';
import { LibraryPills } from '../components/LibraryPills';
import { SpecTabs } from '../components/SpecTabs';
import { Footer } from '../components';

interface Implementation {
  library_id: string;
  library_name: string;
  preview_url: string;
  preview_thumb?: string;
  preview_html?: string;
  quality_score: number | null;
  code: string | null;
  generated_at?: string;
  library_version?: string;
}

interface SpecDetail {
  id: string;
  title: string;
  description: string;
  applications?: string[];
  data?: string[];
  notes?: string[];
  tags?: Record<string, string[]>;
  implementations: Implementation[];
}

export function SpecPage() {
  const { specId, library: urlLibrary } = useParams();
  const navigate = useNavigate();
  const { trackEvent } = useAnalytics();

  const [specData, setSpecData] = useState<SpecDetail | null>(null);
  const [selectedLibrary, setSelectedLibrary] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [imageLoaded, setImageLoaded] = useState(false);

  // Fetch spec data
  useEffect(() => {
    if (!specId) return;

    const fetchSpec = async () => {
      setLoading(true);
      setError(null);
      setImageLoaded(false);

      try {
        const res = await fetch(`${API_URL}/specs/${specId}`);
        if (!res.ok) {
          if (res.status === 404) {
            setError('Spec not found');
          } else {
            setError('Failed to load spec');
          }
          return;
        }

        const data: SpecDetail = await res.json();
        setSpecData(data);

        // Set selected library
        if (urlLibrary && data.implementations.some((impl) => impl.library_id === urlLibrary)) {
          setSelectedLibrary(urlLibrary);
        } else if (data.implementations.length > 0) {
          // Pick random implementation
          const randomIdx = Math.floor(Math.random() * data.implementations.length);
          const randomLib = data.implementations[randomIdx].library_id;
          setSelectedLibrary(randomLib);

          // Update URL to include the library (without adding to history)
          if (!urlLibrary) {
            navigate(`/${specId}/${randomLib}`, { replace: true });
          }
        }
      } catch (err) {
        console.error('Error fetching spec:', err);
        setError('Failed to load spec');
      } finally {
        setLoading(false);
      }
    };

    fetchSpec();
  }, [specId, urlLibrary, navigate]);

  // Get sorted implementations (alphabetical)
  const sortedImpls = useMemo(() => {
    if (!specData) return [];
    return [...specData.implementations].sort((a, b) => a.library_id.localeCompare(b.library_id));
  }, [specData]);

  // Get current implementation and index
  const currentImpl = useMemo(() => {
    if (!specData || !selectedLibrary) return null;
    return specData.implementations.find((impl) => impl.library_id === selectedLibrary) || null;
  }, [specData, selectedLibrary]);

  const currentIndex = useMemo(() => {
    if (!selectedLibrary) return 0;
    return sortedImpls.findIndex((impl) => impl.library_id === selectedLibrary);
  }, [sortedImpls, selectedLibrary]);

  // Handle library switch
  const handleLibrarySelect = useCallback(
    (libraryId: string) => {
      setSelectedLibrary(libraryId);
      setImageLoaded(false);
      navigate(`/${specId}/${libraryId}`, { replace: true });
      trackEvent('switch_library', { spec: specId, library: libraryId });
    },
    [specId, navigate, trackEvent]
  );

  // Navigate to prev/next library
  const handlePrevLibrary = useCallback(() => {
    if (sortedImpls.length === 0) return;
    const newIndex = currentIndex <= 0 ? sortedImpls.length - 1 : currentIndex - 1;
    handleLibrarySelect(sortedImpls[newIndex].library_id);
  }, [sortedImpls, currentIndex, handleLibrarySelect]);

  const handleNextLibrary = useCallback(() => {
    if (sortedImpls.length === 0) return;
    const newIndex = currentIndex >= sortedImpls.length - 1 ? 0 : currentIndex + 1;
    handleLibrarySelect(sortedImpls[newIndex].library_id);
  }, [sortedImpls, currentIndex, handleLibrarySelect]);

  // Handle download
  const handleDownload = useCallback(() => {
    if (!currentImpl?.preview_url) return;
    const link = document.createElement('a');
    link.href = currentImpl.preview_url;
    link.download = `${specId}-${selectedLibrary}.png`;
    link.click();
    trackEvent('download_image', { spec: specId, library: selectedLibrary || undefined });
  }, [currentImpl, specId, selectedLibrary, trackEvent]);

  // Track page view
  useEffect(() => {
    if (specData && selectedLibrary) {
      trackEvent('view_spec', { spec: specId, library: selectedLibrary });
    }
  }, [specData, selectedLibrary, specId, trackEvent]);

  if (loading) {
    return (
      <Box sx={{ textAlign: 'center', py: 8 }}>
        <Skeleton variant="rectangular" width="100%" height={400} sx={{ maxWidth: 800, mx: 'auto', borderRadius: 2 }} />
        <Box sx={{ display: 'flex', gap: 1, justifyContent: 'center', mt: 2 }}>
          {[1, 2, 3, 4].map((i) => (
            <Skeleton key={i} variant="rounded" width={80} height={32} />
          ))}
        </Box>
      </Box>
    );
  }

  if (error || !specData) {
    return (
      <Box sx={{ textAlign: 'center', py: 8 }}>
        <Typography variant="h5" sx={{ mb: 2, color: '#6b7280' }}>
          {error || 'Spec not found'}
        </Typography>
        <Button component={Link} to="/" startIcon={<ArrowBackIcon />} sx={{ color: '#3776AB' }}>
          Back to Home
        </Button>
      </Box>
    );
  }

  return (
    <>
      <Helmet>
        <title>{`${specData.title} - ${selectedLibrary} | pyplots.ai`}</title>
        <meta name="description" content={specData.description} />
        <meta property="og:title" content={`${specData.title} - ${selectedLibrary} | pyplots.ai`} />
        <meta property="og:description" content={specData.description} />
        {currentImpl?.preview_url && <meta property="og:image" content={currentImpl.preview_url} />}
        <meta property="og:url" content={`https://pyplots.ai/${specId}/${selectedLibrary}`} />
      </Helmet>

      <Box sx={{ pb: 4 }}>
        {/* Back Button */}
        <Button
          component={Link}
          to="/"
          startIcon={<ArrowBackIcon />}
          sx={{
            color: '#6b7280',
            mb: 2,
            fontFamily: '"MonoLisa", monospace',
            textTransform: 'none',
            '&:hover': { color: '#3776AB', bgcolor: 'transparent' },
          }}
        >
          Back
        </Button>

        {/* Title */}
        <Typography
          variant="h4"
          component="h1"
          sx={{
            textAlign: 'center',
            fontFamily: '"MonoLisa", monospace',
            fontWeight: 600,
            mb: 1,
            color: '#1f2937',
          }}
        >
          {specData.title}
        </Typography>

        {/* Description */}
        <Typography
          sx={{
            textAlign: 'center',
            fontFamily: '"MonoLisa", monospace',
            fontSize: '0.9rem',
            color: '#6b7280',
            maxWidth: 700,
            mx: 'auto',
            mb: 2,
            lineHeight: 1.6,
          }}
        >
          {specData.description}
        </Typography>

        {/* Library Carousel */}
        <LibraryPills
          implementations={specData.implementations}
          selectedLibrary={selectedLibrary || ''}
          onSelect={handleLibrarySelect}
        />

        {/* Main Image with Navigation */}
        <Box
          sx={{
            display: 'flex',
            alignItems: 'center',
            gap: { xs: 1, sm: 2 },
            maxWidth: 1000,
            mx: 'auto',
          }}
        >
          {/* Left Arrow */}
          <IconButton
            onClick={handlePrevLibrary}
            sx={{
              bgcolor: '#f3f4f6',
              '&:hover': { bgcolor: '#e5e7eb' },
              flexShrink: 0,
            }}
            size="large"
          >
            <ChevronLeftIcon />
          </IconButton>

          {/* Image Container */}
          <Box
            sx={{
              position: 'relative',
              flex: 1,
              borderRadius: 2,
              overflow: 'hidden',
              bgcolor: '#f3f4f6',
              aspectRatio: '16/9',
            }}
          >
            {!imageLoaded && (
              <Skeleton
                variant="rectangular"
                sx={{
                  position: 'absolute',
                  inset: 0,
                  width: '100%',
                  height: '100%',
                }}
              />
            )}
            {currentImpl?.preview_url && (
              <Box
                component="img"
                src={currentImpl.preview_url}
                alt={`${specData.title} - ${selectedLibrary}`}
                onLoad={() => setImageLoaded(true)}
                sx={{
                  width: '100%',
                  height: '100%',
                  objectFit: 'contain',
                  display: imageLoaded ? 'block' : 'none',
                }}
              />
            )}

            {/* Library Badge (top-left) */}
            <Box
              sx={{
                position: 'absolute',
                top: 8,
                left: 8,
                display: 'flex',
                gap: 1,
                alignItems: 'center',
              }}
            >
              <Box
                sx={{
                  px: 1,
                  py: 0.25,
                  bgcolor: 'rgba(0,0,0,0.6)',
                  borderRadius: 1,
                  fontSize: '0.75rem',
                  fontFamily: '"MonoLisa", monospace',
                  color: '#fff',
                }}
              >
                {selectedLibrary}
              </Box>
              <Box
                sx={{
                  px: 0.75,
                  py: 0.25,
                  bgcolor: 'rgba(0,0,0,0.6)',
                  borderRadius: 1,
                  fontSize: '0.7rem',
                  fontFamily: '"MonoLisa", monospace',
                  color: '#fff',
                }}
              >
                {currentIndex + 1}/{sortedImpls.length}
              </Box>
            </Box>

            {/* Action Buttons (top-right) */}
            <Box
              sx={{
                position: 'absolute',
                top: 8,
                right: 8,
                display: 'flex',
                gap: 0.5,
              }}
            >
              <Tooltip title="Download PNG">
                <IconButton
                  onClick={handleDownload}
                  sx={{
                    bgcolor: 'rgba(255,255,255,0.9)',
                    '&:hover': { bgcolor: '#fff' },
                  }}
                  size="small"
                >
                  <DownloadIcon fontSize="small" />
                </IconButton>
              </Tooltip>
              {currentImpl?.preview_html && (
                <Tooltip title="Open Interactive">
                  <IconButton
                    component="a"
                    href={currentImpl.preview_html}
                    target="_blank"
                    rel="noopener noreferrer"
                    onClick={() => trackEvent('open_interactive', { spec: specId, library: selectedLibrary || undefined })}
                    sx={{
                      bgcolor: 'rgba(255,255,255,0.9)',
                      '&:hover': { bgcolor: '#fff' },
                    }}
                    size="small"
                  >
                    <OpenInNewIcon fontSize="small" />
                  </IconButton>
                </Tooltip>
              )}
            </Box>
          </Box>

          {/* Right Arrow */}
          <IconButton
            onClick={handleNextLibrary}
            sx={{
              bgcolor: '#f3f4f6',
              '&:hover': { bgcolor: '#e5e7eb' },
              flexShrink: 0,
            }}
            size="large"
          >
            <ChevronRightIcon />
          </IconButton>
        </Box>

        {/* Tabs */}
        <SpecTabs
          code={currentImpl?.code || null}
          description={specData.description}
          applications={specData.applications}
          notes={specData.notes}
          qualityScore={currentImpl?.quality_score || null}
          libraryId={selectedLibrary || ''}
          onTrackEvent={trackEvent}
        />

        {/* Footer */}
        <Footer onTrackEvent={trackEvent} selectedSpec={specId} selectedLibrary={selectedLibrary || ''} />
      </Box>
    </>
  );
}
