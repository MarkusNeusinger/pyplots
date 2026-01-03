import { useState, useCallback } from 'react';
import Box from '@mui/material/Box';
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import Tooltip from '@mui/material/Tooltip';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import CodeIcon from '@mui/icons-material/Code';
import DescriptionIcon from '@mui/icons-material/Description';
import StarIcon from '@mui/icons-material/Star';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import CheckIcon from '@mui/icons-material/Check';

// Import Prism for syntax highlighting (same as FullscreenModal)
import Prism from 'prismjs';
import 'prismjs/components/prism-python';
import 'prismjs/themes/prism.css';

interface SpecAccordionsProps {
  code: string | null;
  description: string;
  applications?: string[];
  notes?: string[];
  qualityScore: number | null;
  libraryId: string;
  onTrackEvent?: (name: string, props?: Record<string, string | undefined>) => void;
}

export function SpecAccordions({
  code,
  description,
  applications,
  notes,
  qualityScore,
  libraryId,
  onTrackEvent,
}: SpecAccordionsProps) {
  const [copied, setCopied] = useState(false);
  const [expanded, setExpanded] = useState<string | false>(false);

  const handleCopy = useCallback(async () => {
    if (!code) return;
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      onTrackEvent?.('copy_code', { library: libraryId, method: 'accordion' });
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Copy failed:', err);
    }
  }, [code, libraryId, onTrackEvent]);

  const handleChange = (panel: string) => (_: React.SyntheticEvent, isExpanded: boolean) => {
    setExpanded(isExpanded ? panel : false);
    if (isExpanded) {
      onTrackEvent?.(`expand_${panel}`, { library: libraryId });
    }
  };

  // Highlight code with Prism
  const highlightedCode = code
    ? Prism.highlight(code, Prism.languages.python, 'python')
    : '';

  return (
    <Box sx={{ mt: 3, maxWidth: 900, mx: 'auto' }}>
      {/* Code Accordion */}
      <Accordion
        expanded={expanded === 'code'}
        onChange={handleChange('code')}
        sx={{
          bgcolor: '#fafafa',
          boxShadow: 'none',
          '&:before': { display: 'none' },
          borderRadius: '8px !important',
          mb: 1,
        }}
      >
        <AccordionSummary
          expandIcon={<ExpandMoreIcon />}
          sx={{
            '& .MuiAccordionSummary-content': {
              alignItems: 'center',
              gap: 1,
            },
          }}
        >
          <CodeIcon sx={{ color: '#3776AB', fontSize: '1.25rem' }} />
          <Typography sx={{ fontFamily: '"MonoLisa", monospace', fontWeight: 500 }}>
            Code
          </Typography>
        </AccordionSummary>
        <AccordionDetails sx={{ pt: 0 }}>
          <Box sx={{ position: 'relative' }}>
            <Tooltip title={copied ? 'Copied!' : 'Copy code'}>
              <IconButton
                onClick={handleCopy}
                sx={{
                  position: 'absolute',
                  top: 8,
                  right: 8,
                  bgcolor: '#fff',
                  boxShadow: 1,
                  '&:hover': { bgcolor: '#f3f4f6' },
                }}
                size="small"
              >
                {copied ? <CheckIcon color="success" /> : <ContentCopyIcon fontSize="small" />}
              </IconButton>
            </Tooltip>
            <Box
              component="pre"
              sx={{
                bgcolor: '#1e1e1e',
                color: '#d4d4d4',
                p: 2,
                borderRadius: 1,
                overflow: 'auto',
                maxHeight: 400,
                fontSize: '0.8rem',
                fontFamily: '"MonoLisa", monospace',
                lineHeight: 1.5,
                '& .token.comment': { color: '#6a9955' },
                '& .token.string': { color: '#ce9178' },
                '& .token.keyword': { color: '#569cd6' },
                '& .token.function': { color: '#dcdcaa' },
                '& .token.number': { color: '#b5cea8' },
                '& .token.operator': { color: '#d4d4d4' },
                '& .token.builtin': { color: '#4ec9b0' },
              }}
            >
              <code dangerouslySetInnerHTML={{ __html: highlightedCode }} />
            </Box>
          </Box>
        </AccordionDetails>
      </Accordion>

      {/* Description Accordion */}
      <Accordion
        expanded={expanded === 'description'}
        onChange={handleChange('description')}
        sx={{
          bgcolor: '#fafafa',
          boxShadow: 'none',
          '&:before': { display: 'none' },
          borderRadius: '8px !important',
          mb: 1,
        }}
      >
        <AccordionSummary
          expandIcon={<ExpandMoreIcon />}
          sx={{
            '& .MuiAccordionSummary-content': {
              alignItems: 'center',
              gap: 1,
            },
          }}
        >
          <DescriptionIcon sx={{ color: '#FFD43B', fontSize: '1.25rem' }} />
          <Typography sx={{ fontFamily: '"MonoLisa", monospace', fontWeight: 500 }}>
            Description
          </Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Typography
            sx={{
              fontFamily: '"MonoLisa", monospace',
              fontSize: '0.9rem',
              lineHeight: 1.7,
              color: '#374151',
              mb: 2,
            }}
          >
            {description}
          </Typography>

          {applications && applications.length > 0 && (
            <Box sx={{ mb: 2 }}>
              <Typography
                sx={{
                  fontFamily: '"MonoLisa", monospace',
                  fontSize: '0.8rem',
                  fontWeight: 600,
                  color: '#6b7280',
                  mb: 1,
                }}
              >
                Applications
              </Typography>
              <Box component="ul" sx={{ m: 0, pl: 2 }}>
                {applications.map((app, i) => (
                  <Typography
                    key={i}
                    component="li"
                    sx={{
                      fontFamily: '"MonoLisa", monospace',
                      fontSize: '0.85rem',
                      color: '#4b5563',
                      mb: 0.5,
                    }}
                  >
                    {app}
                  </Typography>
                ))}
              </Box>
            </Box>
          )}

          {notes && notes.length > 0 && (
            <Box>
              <Typography
                sx={{
                  fontFamily: '"MonoLisa", monospace',
                  fontSize: '0.8rem',
                  fontWeight: 600,
                  color: '#6b7280',
                  mb: 1,
                }}
              >
                Notes
              </Typography>
              <Box component="ul" sx={{ m: 0, pl: 2 }}>
                {notes.map((note, i) => (
                  <Typography
                    key={i}
                    component="li"
                    sx={{
                      fontFamily: '"MonoLisa", monospace',
                      fontSize: '0.85rem',
                      color: '#4b5563',
                      mb: 0.5,
                    }}
                  >
                    {note}
                  </Typography>
                ))}
              </Box>
            </Box>
          )}
        </AccordionDetails>
      </Accordion>

      {/* Quality Accordion */}
      <Accordion
        expanded={expanded === 'quality'}
        onChange={handleChange('quality')}
        sx={{
          bgcolor: '#fafafa',
          boxShadow: 'none',
          '&:before': { display: 'none' },
          borderRadius: '8px !important',
        }}
      >
        <AccordionSummary
          expandIcon={<ExpandMoreIcon />}
          sx={{
            '& .MuiAccordionSummary-content': {
              alignItems: 'center',
              gap: 1,
            },
          }}
        >
          <StarIcon sx={{ color: '#f59e0b', fontSize: '1.25rem' }} />
          <Typography sx={{ fontFamily: '"MonoLisa", monospace', fontWeight: 500 }}>
            Quality: {qualityScore ? `${Math.round(qualityScore)}/100` : 'N/A'}
          </Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Typography
            sx={{
              fontFamily: '"MonoLisa", monospace',
              fontSize: '0.9rem',
              color: '#6b7280',
            }}
          >
            {qualityScore && qualityScore >= 90 ? (
              <>This implementation scored <strong>{Math.round(qualityScore)}/100</strong> in AI quality review.</>
            ) : qualityScore ? (
              <>Quality score: <strong>{Math.round(qualityScore)}/100</strong></>
            ) : (
              'Quality score not available.'
            )}
          </Typography>
        </AccordionDetails>
      </Accordion>
    </Box>
  );
}
