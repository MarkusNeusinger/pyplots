import { useState, useMemo, useCallback, useEffect } from 'react';
import Box from '@mui/material/Box';
import Modal from '@mui/material/Modal';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import CircularProgress from '@mui/material/CircularProgress';
import CloseIcon from '@mui/icons-material/Close';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import DownloadIcon from '@mui/icons-material/Download';
import CodeIcon from '@mui/icons-material/Code';
import ImageIcon from '@mui/icons-material/Image';
import CheckIcon from '@mui/icons-material/Check';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { oneLight } from 'react-syntax-highlighter/dist/esm/styles/prism';
import type { PlotImage } from '../types';
import { API_URL } from '../constants';
import { useCopyCode, useCodeFetch } from '../hooks';

interface FullscreenModalProps {
  image: PlotImage | null;
  selectedSpec: string;
  onClose: () => void;
  onTrackEvent?: (name: string, props?: Record<string, string | undefined>) => void;
}

export function FullscreenModal({ image, selectedSpec, onClose, onTrackEvent }: FullscreenModalProps) {
  const [showCode, setShowCode] = useState(false);
  const [blinkCodeButton, setBlinkCodeButton] = useState(false);
  const [downloaded, setDownloaded] = useState(false);
  const [fetchedCode, setFetchedCode] = useState<string | null>(null);
  const [codeLoading, setCodeLoading] = useState(false);

  const { fetchCode } = useCodeFetch();
  const { copied, copyToClipboard, reset: resetCopied } = useCopyCode({
    onCopy: () => {
      const specId = selectedSpec || image?.spec_id;
      onTrackEvent?.('copy_code', { spec: specId, library: image?.library, method: 'button' });
    },
  });

  // Code to display - prefer image.code if available, otherwise fetched
  const displayCode = image?.code ?? fetchedCode;

  // Fetch code when modal opens (if not already present in image)
  useEffect(() => {
    if (image && !image.code && image.spec_id) {
      setCodeLoading(true);
      fetchCode(image.spec_id, image.library).then((code) => {
        setFetchedCode(code);
        setCodeLoading(false);
      });
    } else {
      setFetchedCode(null);
    }
  }, [image, fetchCode]);

  // Reset state when modal opens
  const handleOpen = useCallback(() => {
    setShowCode(false);
    setBlinkCodeButton(true);
    resetCopied();
    setDownloaded(false);
    setTimeout(() => setBlinkCodeButton(false), 1000);
  }, [resetCopied]);

  // Memoize syntax-highlighted code to avoid expensive re-renders
  const highlightedCode = useMemo(() => {
    if (!displayCode) return null;
    return (
      <SyntaxHighlighter
        language="python"
        style={oneLight}
        customStyle={{
          margin: 0,
          fontSize: '0.85rem',
          fontFamily: '"MonoLisa", "MonoLisa Fallback", monospace',
          background: 'transparent',
        }}
      >
        {displayCode}
      </SyntaxHighlighter>
    );
  }, [displayCode]);

  // Copy code to clipboard
  const handleCopyCode = useCallback(() => {
    if (displayCode) {
      copyToClipboard(displayCode);
    }
  }, [displayCode, copyToClipboard]);

  // Track native copy events (Ctrl+C, Cmd+C)
  const handleNativeCopy = useCallback(() => {
    const specId = selectedSpec || image?.spec_id;
    onTrackEvent?.('copy_code', { spec: specId, library: image?.library, method: 'keyboard' });
  }, [onTrackEvent, selectedSpec, image?.library, image?.spec_id]);

  // Track contextmenu (right-click) - user may copy from context menu
  const handleContextMenu = useCallback(() => {
    const specId = selectedSpec || image?.spec_id;
    onTrackEvent?.('copy_code', { spec: specId, library: image?.library, method: 'keyboard' });
  }, [onTrackEvent, selectedSpec, image?.library, image?.spec_id]);

  // Download image via backend proxy
  const downloadImage = useCallback(() => {
    const specId = selectedSpec || image?.spec_id;
    if (image?.library && specId) {
      const link = document.createElement('a');
      link.href = `${API_URL}/download/${specId}/${image.library}`;
      link.download = `${specId}-${image.library}.png`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      setDownloaded(true);
      onTrackEvent?.('download_image', { spec: specId, library: image.library });
      setTimeout(() => setDownloaded(false), 2000);
    }
  }, [image?.library, image?.spec_id, selectedSpec, onTrackEvent]);

  const handleClose = useCallback(() => {
    setShowCode(false);
    onClose();
  }, [onClose]);

  return (
    <Modal
      open={!!image}
      onClose={handleClose}
      aria-labelledby="plot-modal-title"
      disableRestoreFocus
      onTransitionEnter={handleOpen}
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
            onClick={handleClose}
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
        {image && (
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
                    onClick={() => {
                      setShowCode(false);
                      onTrackEvent?.('view_image', { spec: selectedSpec || image?.spec_id, library: image?.library });
                    }}
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
                      fontFamily: '"MonoLisa", "MonoLisa Fallback", monospace',
                      '&:hover': { color: '#3776AB', bgcolor: '#fff' },
                    }}
                  >
                    <ImageIcon sx={{ fontSize: 20 }} />
                    plot
                  </Box>
                  <Box
                    onClick={handleCopyCode}
                    sx={{
                      display: 'flex',
                      alignItems: 'center',
                      px: 1,
                      py: 0.5,
                      borderRadius: 1,
                      cursor: 'pointer',
                      color: copied ? '#22c55e' : '#6b7280',
                      bgcolor: 'rgba(255,255,255,0.9)',
                      transition: 'color 0.2s ease',
                      '&:hover': { color: copied ? '#22c55e' : '#1f2937', bgcolor: '#fff' },
                    }}
                  >
                    {copied ? <CheckIcon sx={{ fontSize: 20 }} /> : <ContentCopyIcon sx={{ fontSize: 20 }} />}
                  </Box>
                </Box>
                <Box
                  onCopy={handleNativeCopy}
                  onContextMenu={handleContextMenu}
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
                {(displayCode || codeLoading) && (
                  <Box
                    onClick={() => {
                      if (displayCode) {
                        setShowCode(true);
                        onTrackEvent?.('view_code', { spec: selectedSpec || image?.spec_id, library: image?.library });
                      }
                    }}
                    sx={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: 0.5,
                      px: 1,
                      py: 0.5,
                      borderRadius: 1,
                      cursor: displayCode ? 'pointer' : 'default',
                      color: '#6b7280',
                      bgcolor: 'rgba(255,255,255,0.9)',
                      fontSize: '0.85rem',
                      fontFamily: '"MonoLisa", "MonoLisa Fallback", monospace',
                      '&:hover': displayCode ? { color: '#3776AB', bgcolor: '#fff' } : {},
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
                    {codeLoading ? (
                      <CircularProgress size={16} sx={{ color: '#6b7280' }} />
                    ) : (
                      <CodeIcon sx={{ fontSize: 20 }} />
                    )}
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
                    color: downloaded ? '#22c55e' : '#6b7280',
                    bgcolor: 'rgba(255,255,255,0.9)',
                    transition: 'color 0.2s ease',
                    '&:hover': { color: downloaded ? '#22c55e' : '#1f2937', bgcolor: '#fff' },
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
                  {downloaded ? <CheckIcon sx={{ fontSize: 20 }} /> : <DownloadIcon sx={{ fontSize: 20 }} />}
                </Box>
              </Box>
              <img
                src={image.url}
                alt={`${selectedSpec} - ${image.library}`}
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
                fontFamily: '"MonoLisa", "MonoLisa Fallback", monospace',
                fontSize: '1rem',
              }}
            >
              {image.library}
            </Typography>
          </Box>
        )}
      </Box>
    </Modal>
  );
}
