import { useState, useEffect, useMemo, useCallback, useRef } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { Helmet } from 'react-helmet-async';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import Tooltip from '@mui/material/Tooltip';
import Skeleton from '@mui/material/Skeleton';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import CloseIcon from '@mui/icons-material/Close';
import DownloadIcon from '@mui/icons-material/Download';
import OpenInNewIcon from '@mui/icons-material/OpenInNew';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import CheckIcon from '@mui/icons-material/Check';

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
  // Review fields
  review_strengths?: string[];
  review_weaknesses?: string[];
  review_image_description?: string;
  review_criteria_checklist?: Record<string, unknown>;
  review_verdict?: string;
}

interface SpecDetail {
  id: string;
  title: string;
  description: string;
  applications?: string[];
  data?: string[];
  notes?: string[];
  tags?: Record<string, string[]>;
  created?: string;
  updated?: string;
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
  const [descExpanded, setDescExpanded] = useState(false);
  const [codeCopied, setCodeCopied] = useState(false);

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

  // Get current implementation
  const currentImpl = useMemo(() => {
    if (!specData || !selectedLibrary) return null;
    return specData.implementations.find((impl) => impl.library_id === selectedLibrary) || null;
  }, [specData, selectedLibrary]);

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

  // Handle download
  const handleDownload = useCallback(() => {
    if (!currentImpl?.preview_url) return;
    const link = document.createElement('a');
    link.href = currentImpl.preview_url;
    link.download = `${specId}-${selectedLibrary}.png`;
    link.click();
    trackEvent('download_image', { spec: specId, library: selectedLibrary || undefined });
  }, [currentImpl, specId, selectedLibrary, trackEvent]);

  // Handle copy code
  const handleCopyCode = useCallback(async () => {
    if (!currentImpl?.code) return;
    try {
      await navigator.clipboard.writeText(currentImpl.code);
      setCodeCopied(true);
      trackEvent('copy_code', { spec: specId, library: selectedLibrary || undefined, method: 'image' });
      setTimeout(() => setCodeCopied(false), 2000);
    } catch (err) {
      console.error('Copy failed:', err);
    }
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
        {/* Breadcrumb navigation */}
        <Box
          sx={{
            display: 'flex',
            alignItems: 'center',
            mx: { xs: -2, sm: -4, md: -8, lg: -12 },
            mt: -5, // Compensate for Layout padding
            px: 2,
            py: 1,
            mb: 2,
            bgcolor: '#f3f4f6',
            borderBottom: '1px solid #e5e7eb',
            fontFamily: '"MonoLisa", monospace',
            fontSize: '0.85rem',
          }}
        >
          <Box
            component={Link}
            to="/"
            sx={{
              color: '#3776AB',
              textDecoration: 'none',
              '&:hover': { textDecoration: 'underline' },
            }}
          >
            pyplots.ai
          </Box>
          <Box component="span" sx={{ mx: 1, color: '#9ca3af' }}>›</Box>
          <Box
            component={Link}
            to={`/${specId}`}
            sx={{
              color: '#3776AB',
              textDecoration: 'none',
              '&:hover': { textDecoration: 'underline' },
            }}
          >
            {specId}
          </Box>
          <Box component="span" sx={{ mx: 1, color: '#9ca3af' }}>›</Box>
          <Box component="span" sx={{ color: '#4b5563' }}>
            {selectedLibrary}
          </Box>
        </Box>

        {/* Title */}
        <Typography
          variant="h4"
          component="h1"
          sx={{
            textAlign: 'center',
            fontFamily: '"MonoLisa", monospace',
            fontWeight: 600,
            fontSize: { xs: '1.25rem', sm: '1.5rem', md: '2rem' },
            mb: 1,
            color: '#1f2937',
          }}
        >
          {specData.title}
        </Typography>

        {/* Description */}
        <Typography
          onClick={() => !descExpanded && setDescExpanded(true)}
          sx={{
            textAlign: 'center',
            fontFamily: '"MonoLisa", monospace',
            fontSize: { xs: '0.8rem', sm: '0.9rem' },
            color: '#6b7280',
            maxWidth: 700,
            mx: 'auto',
            mb: 2,
            lineHeight: 1.6,
            cursor: descExpanded ? 'default' : 'pointer',
            ...(!descExpanded && {
              display: '-webkit-box',
              WebkitLineClamp: 5,
              WebkitBoxOrient: 'vertical',
              overflow: 'hidden',
            }),
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

        {/* Main Image (full width) */}
        <Box
          sx={{
            maxWidth: { xs: '100%', md: 1200, lg: 1400, xl: 1600 },
            mx: 'auto',
          }}
        >
          <Box
            sx={{
              position: 'relative',
              borderRadius: 2,
              overflow: 'hidden',
              bgcolor: '#fff',
              boxShadow: '0 2px 8px rgba(0,0,0,0.08)',
              aspectRatio: '16/9',
              '&:hover .impl-counter': {
                opacity: 1,
              },
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
            {currentImpl?.code && (
              <Tooltip title={codeCopied ? 'Copied!' : 'Copy Code'}>
                <IconButton
                  onClick={handleCopyCode}
                  sx={{
                    bgcolor: 'rgba(255,255,255,0.9)',
                    '&:hover': { bgcolor: '#fff' },
                  }}
                  size="small"
                >
                  {codeCopied ? <CheckIcon fontSize="small" color="success" /> : <ContentCopyIcon fontSize="small" />}
                </IconButton>
              </Tooltip>
            )}
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
                  component={Link}
                  to={`/interactive/${specId}/${selectedLibrary}`}
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

          {/* Implementation counter (hover) */}
          {specData.implementations.length > 1 && (
            <Box
              className="impl-counter"
              sx={{
                position: 'absolute',
                bottom: 8,
                right: 8,
                px: 1,
                py: 0.25,
                bgcolor: 'rgba(0,0,0,0.6)',
                borderRadius: 1,
                fontSize: '0.75rem',
                fontFamily: '"MonoLisa", monospace',
                color: '#fff',
                opacity: 0,
                transition: 'opacity 0.2s',
              }}
            >
              {[...specData.implementations]
                .sort((a, b) => a.library_id.localeCompare(b.library_id))
                .findIndex((impl) => impl.library_id === selectedLibrary) + 1}
              /{specData.implementations.length}
            </Box>
          )}
          </Box>
        </Box>

        {/* Tabs */}
        <SpecTabs
          // Code tab
          code={currentImpl?.code || null}
          // Specification tab
          specId={specData.id}
          title={specData.title}
          description={specData.description}
          applications={specData.applications}
          data={specData.data}
          notes={specData.notes}
          tags={specData.tags}
          created={specData.created}
          // Implementation tab
          imageDescription={currentImpl?.review_image_description}
          strengths={currentImpl?.review_strengths}
          weaknesses={currentImpl?.review_weaknesses}
          // Quality tab
          qualityScore={currentImpl?.quality_score || null}
          criteriaChecklist={currentImpl?.review_criteria_checklist}
          // Common
          libraryId={selectedLibrary || ''}
          onTrackEvent={trackEvent}
        />

        {/* Footer */}
        <Footer onTrackEvent={trackEvent} selectedSpec={specId} selectedLibrary={selectedLibrary || ''} />
      </Box>
    </>
  );
}
