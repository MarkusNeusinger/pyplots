import { useState, useEffect, useRef, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Helmet } from 'react-helmet-async';
import Box from '@mui/material/Box';
import IconButton from '@mui/material/IconButton';
import Tooltip from '@mui/material/Tooltip';
import CircularProgress from '@mui/material/CircularProgress';
import CloseIcon from '@mui/icons-material/Close';
import OpenInNewIcon from '@mui/icons-material/OpenInNew';

import { API_URL } from '../constants';

// Initial dimensions - will be updated via postMessage from iframe
const INITIAL_WIDTH = 1600;
const INITIAL_HEIGHT = 900;

interface Implementation {
  library_id: string;
  preview_html?: string;
}

interface SpecDetail {
  id: string;
  title: string;
  implementations: Implementation[];
}

export function InteractivePage() {
  const { specId, library } = useParams();
  const navigate = useNavigate();
  const containerRef = useRef<HTMLDivElement>(null);

  const [htmlUrl, setHtmlUrl] = useState<string | null>(null);
  const [title, setTitle] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [scale, setScale] = useState(1);
  const [contentWidth, setContentWidth] = useState(INITIAL_WIDTH);
  const [contentHeight, setContentHeight] = useState(INITIAL_HEIGHT);

  // Calculate scale to fit container based on current content dimensions
  const updateScale = useCallback(() => {
    if (containerRef.current) {
      const containerWidth = containerRef.current.clientWidth;
      const containerHeight = containerRef.current.clientHeight;
      const scaleX = containerWidth / contentWidth;
      const scaleY = containerHeight / contentHeight;
      // Use 0.98 safety margin to prevent scrollbars from rounding errors
      setScale(Math.min(scaleX, scaleY) * 0.98);
    }
  }, [contentWidth, contentHeight]);

  // Listen for size reports from iframe
  useEffect(() => {
    const handleMessage = (event: MessageEvent) => {
      if (event.data?.type === 'pyplots-size') {
        const { width, height } = event.data;
        if (width > 0 && height > 0) {
          setContentWidth(width);
          setContentHeight(height);
        }
      }
    };

    window.addEventListener('message', handleMessage);
    return () => window.removeEventListener('message', handleMessage);
  }, []);

  // Update scale on mount, resize, and when content dimensions change
  useEffect(() => {
    const timer = setTimeout(updateScale, 100);
    window.addEventListener('resize', updateScale);
    return () => {
      clearTimeout(timer);
      window.removeEventListener('resize', updateScale);
    };
  }, [updateScale]);

  // Fetch spec data to get preview_html URL
  useEffect(() => {
    if (!specId || !library) return;

    const fetchSpec = async () => {
      setLoading(true);
      setError(null);

      try {
        const res = await fetch(`${API_URL}/specs/${specId}`);
        if (!res.ok) {
          setError('Failed to load interactive plot');
          return;
        }

        const data: SpecDetail = await res.json();
        setTitle(data.title);

        const impl = data.implementations.find((i) => i.library_id === library);
        if (impl?.preview_html) {
          setHtmlUrl(impl.preview_html);
        } else {
          setError('No interactive version available for this library');
        }
      } catch (err) {
        console.error('Error fetching spec:', err);
        setError('Failed to load interactive plot');
      } finally {
        setLoading(false);
      }
    };

    fetchSpec();
  }, [specId, library]);

  const handleClose = () => {
    navigate(`/${specId}/${library}`);
  };

  // Open original (unmodified) HTML in new tab
  const handleOpenExternal = () => {
    if (htmlUrl) {
      window.open(htmlUrl, '_blank', 'noopener,noreferrer');
    }
  };

  // Build proxy URL for iframe (injects size reporter script)
  const getProxyUrl = (url: string) => {
    return `${API_URL}/proxy/html?url=${encodeURIComponent(url)}`;
  };

  if (loading) {
    return (
      <Box
        sx={{
          position: 'fixed',
          inset: 0,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          bgcolor: '#fafafa',
        }}
      >
        <CircularProgress />
      </Box>
    );
  }

  if (error || !htmlUrl) {
    return (
      <Box
        sx={{
          position: 'fixed',
          inset: 0,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          bgcolor: '#fafafa',
          fontFamily: '"MonoLisa", monospace',
          color: '#6b7280',
        }}
      >
        <Box sx={{ mb: 2 }}>{error || 'Interactive plot not available'}</Box>
        <IconButton onClick={handleClose} sx={{ color: '#3776AB' }}>
          <CloseIcon />
        </IconButton>
      </Box>
    );
  }

  return (
    <>
      <Helmet>
        <title>{`${title} - ${library} (Interactive) | pyplots.ai`}</title>
      </Helmet>

      <Box
        sx={{
          position: 'fixed',
          inset: 0,
          bgcolor: '#fff',
          display: 'flex',
          flexDirection: 'column',
        }}
      >
        {/* Top bar with controls */}
        <Box
          sx={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            px: 2,
            py: 1,
            bgcolor: '#f3f4f6',
            borderBottom: '1px solid #e5e7eb',
          }}
        >
          <Box
            sx={{
              fontFamily: '"MonoLisa", monospace',
              fontSize: '0.85rem',
              color: '#4b5563',
            }}
          >
            {specId} · {library}
          </Box>
          <Box sx={{ display: 'flex', gap: 0.5 }}>
            <Tooltip title="View Raw HTML">
              <IconButton onClick={handleOpenExternal} size="small">
                <OpenInNewIcon fontSize="small" />
              </IconButton>
            </Tooltip>
            <Tooltip title="Close">
              <IconButton onClick={handleClose} size="small">
                <CloseIcon fontSize="small" />
              </IconButton>
            </Tooltip>
          </Box>
        </Box>

        {/* Fullscreen iframe - scaled to fit container */}
        <Box
          ref={containerRef}
          sx={{
            flex: 1,
            position: 'relative',
            overflow: 'hidden',
            bgcolor: '#f9fafb',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          <iframe
            src={getProxyUrl(htmlUrl)}
            width={contentWidth}
            height={contentHeight}
            style={{
              width: contentWidth,
              height: contentHeight,
              minWidth: contentWidth,
              maxWidth: contentWidth,
              border: 'none',
              transform: `scale(${scale})`,
              transformOrigin: 'center center',
            }}
            title={`${title} - ${library} interactive`}
          />
        </Box>
      </Box>
    </>
  );
}
