import { useState, useCallback } from 'react';
import Box from '@mui/material/Box';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import Tooltip from '@mui/material/Tooltip';
import CodeIcon from '@mui/icons-material/Code';
import DescriptionIcon from '@mui/icons-material/Description';
import StarIcon from '@mui/icons-material/Star';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import CheckIcon from '@mui/icons-material/Check';

// Import Prism for syntax highlighting
import Prism from 'prismjs';
import 'prismjs/components/prism-python';
import 'prismjs/themes/prism.css';

interface SpecTabsProps {
  code: string | null;
  description: string;
  applications?: string[];
  notes?: string[];
  qualityScore: number | null;
  libraryId: string;
  onTrackEvent?: (name: string, props?: Record<string, string | undefined>) => void;
}

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel({ children, value, index }: TabPanelProps) {
  return (
    <Box
      role="tabpanel"
      hidden={value !== index}
      sx={{ py: 2 }}
    >
      {value === index && children}
    </Box>
  );
}

export function SpecTabs({
  code,
  description,
  applications,
  notes,
  qualityScore,
  libraryId,
  onTrackEvent,
}: SpecTabsProps) {
  const [copied, setCopied] = useState(false);
  const [tabIndex, setTabIndex] = useState(0);

  const handleCopy = useCallback(async () => {
    if (!code) return;
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      onTrackEvent?.('copy_code', { library: libraryId, method: 'tab' });
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Copy failed:', err);
    }
  }, [code, libraryId, onTrackEvent]);

  const handleTabChange = (_: React.SyntheticEvent, newValue: number) => {
    setTabIndex(newValue);
    const tabNames = ['code', 'description', 'quality'];
    onTrackEvent?.(`view_${tabNames[newValue]}`, { library: libraryId });
  };

  // Highlight code with Prism
  const highlightedCode = code
    ? Prism.highlight(code, Prism.languages.python, 'python')
    : '';

  return (
    <Box sx={{ mt: 3, maxWidth: 900, mx: 'auto' }}>
      <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
        <Tabs
          value={tabIndex}
          onChange={handleTabChange}
          variant="fullWidth"
          sx={{
            '& .MuiTab-root': {
              fontFamily: '"MonoLisa", monospace',
              textTransform: 'none',
              fontSize: '0.875rem',
              minHeight: 48,
            },
            '& .Mui-selected': {
              color: '#3776AB',
            },
            '& .MuiTabs-indicator': {
              backgroundColor: '#3776AB',
            },
          }}
        >
          <Tab
            icon={<CodeIcon sx={{ fontSize: '1.1rem' }} />}
            iconPosition="start"
            label="Code"
          />
          <Tab
            icon={<DescriptionIcon sx={{ fontSize: '1.1rem' }} />}
            iconPosition="start"
            label="Info"
          />
          <Tab
            icon={<StarIcon sx={{ fontSize: '1.1rem', color: tabIndex === 2 ? '#3776AB' : '#f59e0b' }} />}
            iconPosition="start"
            label={qualityScore ? `${Math.round(qualityScore)}` : 'N/A'}
          />
        </Tabs>
      </Box>

      {/* Code Tab */}
      <TabPanel value={tabIndex} index={0}>
        <Box sx={{ position: 'relative' }}>
          <Tooltip title={copied ? 'Copied!' : 'Copy code'}>
            <IconButton
              onClick={handleCopy}
              sx={{
                position: 'absolute',
                top: 8,
                right: 8,
                bgcolor: 'rgba(255,255,255,0.9)',
                zIndex: 1,
                '&:hover': { bgcolor: '#fff' },
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
              m: 0,
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
      </TabPanel>

      {/* Description Tab */}
      <TabPanel value={tabIndex} index={1}>
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
      </TabPanel>

      {/* Quality Tab */}
      <TabPanel value={tabIndex} index={2}>
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
      </TabPanel>
    </Box>
  );
}
