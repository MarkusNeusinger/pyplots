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
import DownloadIcon from '@mui/icons-material/Download';
import OpenInNewIcon from '@mui/icons-material/OpenInNew';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import CheckIcon from '@mui/icons-material/Check';

import MuiLink from '@mui/material/Link';
import ClickAwayListener from '@mui/material/ClickAwayListener';

import { API_URL } from '../constants';
import { useAnalytics } from '../hooks';
import { useAppData } from '../components/Layout';
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
  const { librariesData } = useAppData();

  const [specData, setSpecData] = useState<SpecDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [imageLoaded, setImageLoaded] = useState(false);
  const [descExpanded, setDescExpanded] = useState(false);
  const [codeCopied, setCodeCopied] = useState<string | null>(null); // library_id or null
  const [openTooltip, setOpenTooltip] = useState<string | null>(null);

  // Get library metadata by ID
  const getLibraryMeta = useCallback(
    (libraryId: string) => librariesData.find((lib) => lib.id === libraryId),
    [librariesData]
  );

  // Mode: overview (no library) vs detail (with library)
  const isOverviewMode = !urlLibrary;
  const selectedLibrary = urlLibrary || null;

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

        // Validate library if provided
        if (urlLibrary && !data.implementations.some((impl) => impl.library_id === urlLibrary)) {
          // Invalid library, redirect to overview
          navigate(`/${specId}`, { replace: true });
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

  // Get current implementation (only in detail mode)
  const currentImpl = useMemo(() => {
    if (!specData || !selectedLibrary) return null;
    return specData.implementations.find((impl) => impl.library_id === selectedLibrary) || null;
  }, [specData, selectedLibrary]);

  // Handle library switch (in detail mode)
  const handleLibrarySelect = useCallback(
    (libraryId: string) => {
      setImageLoaded(false);
      navigate(`/${specId}/${libraryId}`, { replace: true });
      trackEvent('switch_library', { spec: specId, library: libraryId });
    },
    [specId, navigate, trackEvent]
  );

  // Handle implementation click (in overview mode)
  const handleImplClick = useCallback(
    (libraryId: string) => {
      navigate(`/${specId}/${libraryId}`);
      trackEvent('select_implementation', { spec: specId, library: libraryId });
    },
    [specId, navigate, trackEvent]
  );

  // Handle image click (in detail mode - go back to overview)
  const handleImageClick = useCallback(() => {
    navigate(`/${specId}`);
    trackEvent('back_to_overview', { spec: specId, library: selectedLibrary || undefined });
  }, [specId, selectedLibrary, navigate, trackEvent]);

  // Handle download (works for both overview and detail mode)
  const handleDownload = useCallback(
    (impl: Implementation) => {
      if (!impl?.preview_url) return;
      const link = document.createElement('a');
      link.href = impl.preview_url;
      link.download = `${specId}-${impl.library_id}.png`;
      link.click();
      trackEvent('download_image', { spec: specId, library: impl.library_id, page: isOverviewMode ? 'spec_overview' : 'spec_detail' });
    },
    [specId, trackEvent, isOverviewMode]
  );

  // Handle copy code (works for both overview and detail mode)
  const handleCopyCode = useCallback(
    async (impl: Implementation) => {
      if (!impl?.code) return;
      try {
        await navigator.clipboard.writeText(impl.code);
        setCodeCopied(impl.library_id);
        trackEvent('copy_code', { spec: specId, library: impl.library_id, method: 'image', page: isOverviewMode ? 'spec_overview' : 'spec_detail' });
        setTimeout(() => setCodeCopied(null), 2000);
      } catch (err) {
        console.error('Copy failed:', err);
      }
    },
    [specId, trackEvent, isOverviewMode]
  );

  // Track page view
  useEffect(() => {
    if (specData) {
      if (isOverviewMode) {
        trackEvent('view_spec_overview', { spec: specId });
      } else if (selectedLibrary) {
        trackEvent('view_spec', { spec: specId, library: selectedLibrary });
      }
    }
  }, [specData, isOverviewMode, selectedLibrary, specId, trackEvent]);

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

  // Sort implementations alphabetically
  const sortedImpls = [...specData.implementations].sort((a, b) => a.library_id.localeCompare(b.library_id));

  return (
    <>
      <Helmet>
        <title>{isOverviewMode ? `${specData.title} | pyplots.ai` : `${specData.title} - ${selectedLibrary} | pyplots.ai`}</title>
        <meta name="description" content={specData.description} />
        <meta property="og:title" content={isOverviewMode ? `${specData.title} | pyplots.ai` : `${specData.title} - ${selectedLibrary} | pyplots.ai`} />
        <meta property="og:description" content={specData.description} />
        {currentImpl?.preview_url && <meta property="og:image" content={currentImpl.preview_url} />}
        <meta property="og:url" content={isOverviewMode ? `https://pyplots.ai/${specId}` : `https://pyplots.ai/${specId}/${selectedLibrary}`} />
      </Helmet>

      <Box sx={{ pb: 4 }}>
        {/* Breadcrumb navigation */}
        <Box
          sx={{
            display: 'flex',
            alignItems: 'center',
            mx: { xs: -2, sm: -4, md: -8, lg: -12 },
            mt: -5,
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
            to="/catalog"
            sx={{
              color: '#3776AB',
              textDecoration: 'none',
              '&:hover': { textDecoration: 'underline' },
            }}
          >
            catalog
          </Box>
          <Box component="span" sx={{ mx: 1, color: '#9ca3af' }}>›</Box>
          {isOverviewMode ? (
            <Box component="span" sx={{ color: '#4b5563' }}>
              {specId}
            </Box>
          ) : (
            <>
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
            </>
          )}
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
            maxWidth: { xs: '100%', md: 800, lg: 950, xl: 1100 },
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

        {isOverviewMode ? (
          /* OVERVIEW MODE: Grid of implementations */
          <>
            {/* Implementation Grid - same style as home page */}
            <Box
              sx={{
                maxWidth: { xs: '100%', md: 1200, lg: 1400, xl: 1600 },
                mx: 'auto',
                mt: 4,
                display: 'grid',
                gridTemplateColumns: 'repeat(3, 1fr)',
                gap: 3,
              }}
            >
              {sortedImpls.map((impl) => (
                <Box key={impl.library_id}>
                  {/* Card */}
                  <Box
                    onClick={() => handleImplClick(impl.library_id)}
                    sx={{
                      position: 'relative',
                      borderRadius: 3,
                      overflow: 'hidden',
                      border: '2px solid rgba(55, 118, 171, 0.2)',
                      boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
                      cursor: 'pointer',
                      transition: 'all 0.3s ease',
                      '&:hover': {
                        border: '2px solid rgba(55, 118, 171, 0.4)',
                        boxShadow: '0 8px 30px rgba(0,0,0,0.15)',
                        transform: 'scale(1.03)',
                      },
                      '&:hover .action-buttons': {
                        opacity: 1,
                      },
                    }}
                  >
                    {impl.preview_thumb || impl.preview_url ? (
                      <Box
                        component="img"
                        src={impl.preview_thumb || impl.preview_url}
                        alt={`${specData.title} - ${impl.library_id}`}
                        sx={{
                          width: '100%',
                          aspectRatio: '16/10',
                          objectFit: 'contain',
                          bgcolor: '#fff',
                        }}
                      />
                    ) : (
                      <Skeleton variant="rectangular" sx={{ width: '100%', aspectRatio: '16/10' }} />
                    )}

                    {/* Action Buttons (top-right) */}
                    <Box
                      className="action-buttons"
                      onClick={(e) => e.stopPropagation()}
                      sx={{
                        position: 'absolute',
                        top: 8,
                        right: 8,
                        display: 'flex',
                        gap: 0.5,
                        opacity: 0,
                        transition: 'opacity 0.2s',
                      }}
                    >
                      {impl.code && (
                        <Tooltip title={codeCopied === impl.library_id ? 'Copied!' : 'Copy Code'}>
                          <IconButton
                            onClick={() => handleCopyCode(impl)}
                            sx={{
                              bgcolor: 'rgba(255,255,255,0.9)',
                              '&:hover': { bgcolor: '#fff' },
                            }}
                            size="small"
                          >
                            {codeCopied === impl.library_id ? (
                              <CheckIcon fontSize="small" color="success" />
                            ) : (
                              <ContentCopyIcon fontSize="small" />
                            )}
                          </IconButton>
                        </Tooltip>
                      )}
                      <Tooltip title="Download PNG">
                        <IconButton
                          onClick={() => handleDownload(impl)}
                          sx={{
                            bgcolor: 'rgba(255,255,255,0.9)',
                            '&:hover': { bgcolor: '#fff' },
                          }}
                          size="small"
                        >
                          <DownloadIcon fontSize="small" />
                        </IconButton>
                      </Tooltip>
                      {impl.preview_html && (
                        <Tooltip title="Open Interactive">
                          <IconButton
                            component={Link}
                            to={`/interactive/${specId}/${impl.library_id}`}
                            onClick={(e: React.MouseEvent) => {
                              e.stopPropagation();
                              trackEvent('open_interactive', { spec: specId, library: impl.library_id });
                            }}
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
                  {/* Label below card with library tooltip */}
                  {(() => {
                    const libMeta = getLibraryMeta(impl.library_id);
                    const tooltipId = `lib-${impl.library_id}`;
                    const isTooltipOpen = openTooltip === tooltipId;

                    return (
                      <Box
                        sx={{
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          mt: 1.5,
                          gap: 0.5,
                        }}
                      >
                        <ClickAwayListener onClickAway={() => isTooltipOpen && setOpenTooltip(null)}>
                          <Box component="span">
                            <Tooltip
                              title={
                                <Box>
                                  <Typography sx={{ fontSize: '0.8rem', mb: libMeta?.documentation_url ? 1 : 0 }}>
                                    {libMeta?.description || 'No description available'}
                                  </Typography>
                                  {libMeta?.documentation_url && (
                                    <MuiLink
                                      href={libMeta.documentation_url}
                                      target="_blank"
                                      rel="noopener noreferrer"
                                      onClick={(e) => e.stopPropagation()}
                                      sx={{
                                        display: 'inline-flex',
                                        alignItems: 'center',
                                        gap: 0.5,
                                        fontSize: '0.75rem',
                                        color: '#90caf9',
                                        textDecoration: 'underline',
                                        '&:hover': { color: '#fff' },
                                      }}
                                    >
                                      {libMeta.documentation_url.replace(/^https?:\/\//, '')}
                                      <OpenInNewIcon sx={{ fontSize: 12 }} />
                                    </MuiLink>
                                  )}
                                </Box>
                              }
                              arrow
                              placement="bottom"
                              open={isTooltipOpen}
                              disableFocusListener
                              disableHoverListener
                              disableTouchListener
                              slotProps={{
                                tooltip: {
                                  sx: {
                                    maxWidth: { xs: '80vw', sm: 400 },
                                    fontFamily: '"MonoLisa", monospace',
                                    fontSize: '0.8rem',
                                  },
                                },
                              }}
                            >
                              <Typography
                                onClick={(e) => {
                                  e.stopPropagation();
                                  setOpenTooltip(isTooltipOpen ? null : tooltipId);
                                }}
                                sx={{
                                  fontSize: '0.8rem',
                                  fontWeight: 600,
                                  fontFamily: '"MonoLisa", monospace',
                                  color: isTooltipOpen ? '#3776AB' : '#9ca3af',
                                  textTransform: 'lowercase',
                                  cursor: 'pointer',
                                  '&:hover': { color: '#3776AB' },
                                }}
                              >
                                {impl.library_id}
                              </Typography>
                            </Tooltip>
                          </Box>
                        </ClickAwayListener>
                        {impl.quality_score && (
                          <>
                            <Typography sx={{ color: '#d1d5db', fontSize: '0.8rem' }}>·</Typography>
                            <Typography
                              sx={{
                                fontSize: '0.8rem',
                                fontWeight: 600,
                                fontFamily: '"MonoLisa", monospace',
                                color: '#9ca3af',
                              }}
                            >
                              {Math.round(impl.quality_score)}
                            </Typography>
                          </>
                        )}
                      </Box>
                    );
                  })()}
                </Box>
              ))}
            </Box>

            {/* Spec Tabs (without Code/Impl/Quality - just Spec info) */}
            <SpecTabs
              code={null}
              specId={specData.id}
              title={specData.title}
              description={specData.description}
              applications={specData.applications}
              data={specData.data}
              notes={specData.notes}
              tags={specData.tags}
              created={specData.created}
              imageDescription={undefined}
              strengths={undefined}
              weaknesses={undefined}
              qualityScore={null}
              criteriaChecklist={undefined}
              libraryId=""
              onTrackEvent={trackEvent}
              overviewMode={true}
            />
          </>
        ) : (
          /* DETAIL MODE: Single implementation view */
          <>
            {/* Library Carousel */}
            <LibraryPills
              implementations={specData.implementations}
              selectedLibrary={selectedLibrary || ''}
              onSelect={handleLibrarySelect}
            />

            {/* Main Image (clickable to go back to overview) */}
            <Box
              sx={{
                maxWidth: { xs: '100%', md: 1200, lg: 1400, xl: 1600 },
                mx: 'auto',
              }}
            >
              <Box
                onClick={handleImageClick}
                sx={{
                  position: 'relative',
                  borderRadius: 2,
                  overflow: 'hidden',
                  bgcolor: '#fff',
                  boxShadow: '0 2px 8px rgba(0,0,0,0.08)',
                  aspectRatio: '16/9',
                  cursor: 'pointer',
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

                {/* Action Buttons (top-right) - stop propagation */}
                <Box
                  onClick={(e) => e.stopPropagation()}
                  sx={{
                    position: 'absolute',
                    top: 8,
                    right: 8,
                    display: 'flex',
                    gap: 0.5,
                  }}
                >
                  {currentImpl?.code && (
                    <Tooltip title={codeCopied === currentImpl.library_id ? 'Copied!' : 'Copy Code'}>
                      <IconButton
                        onClick={() => handleCopyCode(currentImpl)}
                        sx={{
                          bgcolor: 'rgba(255,255,255,0.9)',
                          '&:hover': { bgcolor: '#fff' },
                        }}
                        size="small"
                      >
                        {codeCopied === currentImpl.library_id ? <CheckIcon fontSize="small" color="success" /> : <ContentCopyIcon fontSize="small" />}
                      </IconButton>
                    </Tooltip>
                  )}
                  {currentImpl && (
                    <Tooltip title="Download PNG">
                      <IconButton
                        onClick={() => handleDownload(currentImpl)}
                        sx={{
                          bgcolor: 'rgba(255,255,255,0.9)',
                          '&:hover': { bgcolor: '#fff' },
                        }}
                        size="small"
                      >
                        <DownloadIcon fontSize="small" />
                      </IconButton>
                    </Tooltip>
                  )}
                  {currentImpl?.preview_html && (
                    <Tooltip title="Open Interactive">
                      <IconButton
                        component={Link}
                        to={`/interactive/${specId}/${selectedLibrary}`}
                        onClick={(e: React.MouseEvent) => {
                          e.stopPropagation();
                          trackEvent('open_interactive', { spec: specId, library: selectedLibrary || undefined });
                        }}
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
                    {sortedImpls.findIndex((impl) => impl.library_id === selectedLibrary) + 1}
                    /{specData.implementations.length}
                  </Box>
                )}
              </Box>
            </Box>

            {/* Tabs */}
            <SpecTabs
              code={currentImpl?.code || null}
              specId={specData.id}
              title={specData.title}
              description={specData.description}
              applications={specData.applications}
              data={specData.data}
              notes={specData.notes}
              tags={specData.tags}
              created={specData.created}
              imageDescription={currentImpl?.review_image_description}
              strengths={currentImpl?.review_strengths}
              weaknesses={currentImpl?.review_weaknesses}
              qualityScore={currentImpl?.quality_score || null}
              criteriaChecklist={currentImpl?.review_criteria_checklist}
              libraryId={selectedLibrary || ''}
              onTrackEvent={trackEvent}
            />
          </>
        )}

        {/* Footer */}
        <Footer onTrackEvent={trackEvent} selectedSpec={specId} selectedLibrary={selectedLibrary || ''} />
      </Box>
    </>
  );
}
