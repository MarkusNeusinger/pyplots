import { useState, useCallback, useMemo } from 'react';
import Box from '@mui/material/Box';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import Tooltip from '@mui/material/Tooltip';
import Chip from '@mui/material/Chip';
import Collapse from '@mui/material/Collapse';
import CodeIcon from '@mui/icons-material/Code';
import DescriptionIcon from '@mui/icons-material/Description';
import ImageIcon from '@mui/icons-material/Image';
import StarIcon from '@mui/icons-material/Star';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import CheckIcon from '@mui/icons-material/Check';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ExpandLessIcon from '@mui/icons-material/ExpandLess';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { oneLight } from 'react-syntax-highlighter/dist/esm/styles/prism';

interface SpecTabsProps {
  // Code tab
  code: string | null;
  // Specification tab
  specId: string;
  title: string;
  description: string;
  applications?: string[];
  data?: string[];
  notes?: string[];
  tags?: Record<string, string[]>;
  created?: string;
  // Implementation tab
  imageDescription?: string;
  strengths?: string[];
  weaknesses?: string[];
  // Quality tab
  qualityScore: number | null;
  criteriaChecklist?: Record<string, unknown>;
  // Common
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
    <Box role="tabpanel" hidden={value !== index} sx={{ py: 2 }}>
      {value === index && children}
    </Box>
  );
}

function SectionTitle({ children }: { children: React.ReactNode }) {
  return (
    <Typography
      sx={{
        fontFamily: '"MonoLisa", monospace',
        fontSize: '0.75rem',
        fontWeight: 600,
        color: '#9ca3af',
        textTransform: 'uppercase',
        letterSpacing: '0.05em',
        mb: 0.5,
      }}
    >
      {children}
    </Typography>
  );
}

function SectionContent({ children }: { children: React.ReactNode }) {
  return (
    <Typography
      sx={{
        fontFamily: '"MonoLisa", monospace',
        fontSize: '0.85rem',
        color: '#374151',
        lineHeight: 1.6,
      }}
    >
      {children}
    </Typography>
  );
}

export function SpecTabs({
  code,
  specId,
  title,
  description,
  applications,
  data,
  notes,
  tags,
  created,
  imageDescription,
  strengths,
  weaknesses,
  qualityScore,
  criteriaChecklist,
  libraryId,
  onTrackEvent,
}: SpecTabsProps) {
  const [copied, setCopied] = useState(false);
  const [tabIndex, setTabIndex] = useState(0); // Code is default (index 0)
  const [expandedCategories, setExpandedCategories] = useState<Record<string, boolean>>({});

  const toggleCategory = (category: string) => {
    setExpandedCategories((prev) => ({ ...prev, [category]: !prev[category] }));
  };

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
    const tabNames = ['code', 'specification', 'implementation', 'quality'];
    onTrackEvent?.(`view_${tabNames[newValue]}`, { library: libraryId });
  };

  // Memoize syntax-highlighted code
  const highlightedCode = useMemo(() => {
    if (!code) return null;
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
        {code}
      </SyntaxHighlighter>
    );
  }, [code]);

  // Format date
  const formatDate = (dateStr?: string) => {
    if (!dateStr) return null;
    try {
      return new Date(dateStr).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
      });
    } catch {
      return dateStr;
    }
  };

  // Flatten tags for display
  const allTags = useMemo(() => {
    if (!tags) return [];
    return Object.entries(tags).flatMap(([category, values]) =>
      values.map((v) => ({ category, value: v }))
    );
  }, [tags]);

  return (
    <Box sx={{ mt: 3, maxWidth: { xs: '100%', md: 1200, lg: 1400, xl: 1600 }, mx: 'auto' }}>
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
          <Tab icon={<CodeIcon sx={{ fontSize: '1.1rem' }} />} iconPosition="start" label="Code" />
          <Tab icon={<DescriptionIcon sx={{ fontSize: '1.1rem' }} />} iconPosition="start" label="Spec" />
          <Tab icon={<ImageIcon sx={{ fontSize: '1.1rem' }} />} iconPosition="start" label="Impl" />
          <Tab
            icon={<StarIcon sx={{ fontSize: '1.1rem', color: tabIndex === 3 ? '#3776AB' : '#f59e0b' }} />}
            iconPosition="start"
            label={qualityScore ? `${Math.round(qualityScore)}` : 'Quality'}
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
            sx={{
              bgcolor: '#fafafa',
              p: 3,
              borderRadius: 1,
              overflow: 'auto',
              maxHeight: 400,
            }}
          >
            {highlightedCode}
          </Box>
        </Box>
      </TabPanel>

      {/* Specification Tab */}
      <TabPanel value={tabIndex} index={1}>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          {/* ID */}
          <Box>
            <SectionTitle>ID</SectionTitle>
            <SectionContent>{specId}</SectionContent>
          </Box>

          {/* Title */}
          <Box>
            <SectionTitle>Title</SectionTitle>
            <SectionContent>{title}</SectionContent>
          </Box>

          {/* Description */}
          <Box>
            <SectionTitle>Description</SectionTitle>
            <SectionContent>{description}</SectionContent>
          </Box>

          {/* Applications */}
          {applications && applications.length > 0 && (
            <Box>
              <SectionTitle>Applications</SectionTitle>
              <Box component="ul" sx={{ m: 0, pl: 2 }}>
                {applications.map((app, i) => (
                  <Typography
                    key={i}
                    component="li"
                    sx={{ fontFamily: '"MonoLisa", monospace', fontSize: '0.85rem', color: '#4b5563', mb: 0.5 }}
                  >
                    {app}
                  </Typography>
                ))}
              </Box>
            </Box>
          )}

          {/* Data */}
          {data && data.length > 0 && (
            <Box>
              <SectionTitle>Data</SectionTitle>
              <Box component="ul" sx={{ m: 0, pl: 2 }}>
                {data.map((d, i) => (
                  <Typography
                    key={i}
                    component="li"
                    sx={{ fontFamily: '"MonoLisa", monospace', fontSize: '0.85rem', color: '#4b5563', mb: 0.5 }}
                  >
                    {d}
                  </Typography>
                ))}
              </Box>
            </Box>
          )}

          {/* Notes */}
          {notes && notes.length > 0 && (
            <Box>
              <SectionTitle>Notes</SectionTitle>
              <Box component="ul" sx={{ m: 0, pl: 2 }}>
                {notes.map((note, i) => (
                  <Typography
                    key={i}
                    component="li"
                    sx={{ fontFamily: '"MonoLisa", monospace', fontSize: '0.85rem', color: '#4b5563', mb: 0.5 }}
                  >
                    {note}
                  </Typography>
                ))}
              </Box>
            </Box>
          )}

          {/* Tags */}
          {allTags.length > 0 && (
            <Box>
              <SectionTitle>Tags</SectionTitle>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5, mt: 0.5 }}>
                {allTags.map(({ category, value }, i) => (
                  <Chip
                    key={i}
                    label={value}
                    size="small"
                    sx={{
                      fontFamily: '"MonoLisa", monospace',
                      fontSize: '0.7rem',
                      bgcolor: '#f3f4f6',
                      color: '#6b7280',
                    }}
                  />
                ))}
              </Box>
            </Box>
          )}

          {/* Created */}
          {created && (
            <Box>
              <SectionTitle>Created</SectionTitle>
              <SectionContent>{formatDate(created)}</SectionContent>
            </Box>
          )}
        </Box>
      </TabPanel>

      {/* Implementation Tab */}
      <TabPanel value={tabIndex} index={2}>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          {/* Image Description */}
          {imageDescription && (
            <Box>
              <SectionTitle>AI Description</SectionTitle>
              <SectionContent>{imageDescription}</SectionContent>
            </Box>
          )}

          {/* Strengths */}
          {strengths && strengths.length > 0 && (
            <Box>
              <SectionTitle>Strengths</SectionTitle>
              <Box component="ul" sx={{ m: 0, pl: 2 }}>
                {strengths.map((s, i) => (
                  <Typography
                    key={i}
                    component="li"
                    sx={{ fontFamily: '"MonoLisa", monospace', fontSize: '0.85rem', color: '#22c55e', mb: 0.5 }}
                  >
                    {s}
                  </Typography>
                ))}
              </Box>
            </Box>
          )}

          {/* Weaknesses */}
          {weaknesses && weaknesses.length > 0 && (
            <Box>
              <SectionTitle>Weaknesses</SectionTitle>
              <Box component="ul" sx={{ m: 0, pl: 2 }}>
                {weaknesses.map((w, i) => (
                  <Typography
                    key={i}
                    component="li"
                    sx={{ fontFamily: '"MonoLisa", monospace', fontSize: '0.85rem', color: '#ef4444', mb: 0.5 }}
                  >
                    {w}
                  </Typography>
                ))}
              </Box>
            </Box>
          )}

          {/* No data message */}
          {!imageDescription && (!strengths || strengths.length === 0) && (!weaknesses || weaknesses.length === 0) && (
            <Typography sx={{ fontFamily: '"MonoLisa", monospace', fontSize: '0.9rem', color: '#9ca3af' }}>
              No implementation review data available.
            </Typography>
          )}
        </Box>
      </TabPanel>

      {/* Quality Tab */}
      <TabPanel value={tabIndex} index={3}>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          {/* Score */}
          <Box>
            <SectionTitle>Quality Score</SectionTitle>
            <Typography
              sx={{
                fontFamily: '"MonoLisa", monospace',
                fontSize: '2rem',
                fontWeight: 700,
                color: qualityScore && qualityScore >= 90 ? '#22c55e' : qualityScore && qualityScore >= 70 ? '#f59e0b' : '#ef4444',
              }}
            >
              {qualityScore ? `${Math.round(qualityScore)}/100` : 'N/A'}
            </Typography>
          </Box>

          {/* Criteria Checklist */}
          {criteriaChecklist && Object.keys(criteriaChecklist).length > 0 && (
            <Box>
              <SectionTitle>Criteria Breakdown</SectionTitle>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1.5, mt: 1 }}>
                {Object.entries(criteriaChecklist).map(([category, data]) => {
                  const catData = data as { score?: number; max?: number; items?: Array<{ id: string; name: string; score: number; max: number; passed: boolean; comment?: string }> };
                  const score = catData.score ?? 0;
                  const max = catData.max ?? 0;
                  const pct = max > 0 ? (score / max) * 100 : 0;
                  const items = catData.items || [];
                  const isExpanded = expandedCategories[category] ?? false;

                  return (
                    <Box key={category}>
                      {/* Category header - clickable */}
                      <Box
                        onClick={() => items.length > 0 && toggleCategory(category)}
                        sx={{
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'space-between',
                          mb: 0.5,
                          cursor: items.length > 0 ? 'pointer' : 'default',
                          '&:hover': items.length > 0 ? { opacity: 0.8 } : {},
                        }}
                      >
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                          {items.length > 0 && (
                            isExpanded ? (
                              <ExpandLessIcon sx={{ fontSize: '1rem', color: '#9ca3af' }} />
                            ) : (
                              <ExpandMoreIcon sx={{ fontSize: '1rem', color: '#9ca3af' }} />
                            )
                          )}
                          <Typography sx={{ fontFamily: '"MonoLisa", monospace', fontSize: '0.8rem', color: '#4b5563' }}>
                            {category.replace(/_/g, ' ')}
                          </Typography>
                        </Box>
                        <Typography sx={{ fontFamily: '"MonoLisa", monospace', fontSize: '0.8rem', color: '#6b7280' }}>
                          {score}/{max}
                        </Typography>
                      </Box>
                      {/* Progress bar */}
                      <Box sx={{ height: 4, bgcolor: '#e5e7eb', borderRadius: 2, overflow: 'hidden' }}>
                        <Box
                          sx={{
                            height: '100%',
                            width: `${pct}%`,
                            bgcolor: pct >= 90 ? '#22c55e' : pct >= 70 ? '#f59e0b' : '#ef4444',
                            borderRadius: 2,
                          }}
                        />
                      </Box>
                      {/* Expandable items */}
                      <Collapse in={isExpanded}>
                        <Box sx={{ mt: 1, ml: 2, display: 'flex', flexDirection: 'column', gap: 0.75 }}>
                          {items.map((item) => (
                            <Box key={item.id} sx={{ display: 'flex', flexDirection: 'column', gap: 0.25 }}>
                              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                                <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                                  <Box
                                    sx={{
                                      width: 6,
                                      height: 6,
                                      borderRadius: '50%',
                                      bgcolor:
                                        item.score === 0
                                          ? '#ef4444' // red for 0
                                          : item.score === item.max
                                            ? '#22c55e' // green for full
                                            : '#f59e0b', // yellow for partial
                                    }}
                                  />
                                  <Typography sx={{ fontFamily: '"MonoLisa", monospace', fontSize: '0.75rem', color: '#4b5563' }}>
                                    {item.name}
                                  </Typography>
                                </Box>
                                <Typography sx={{ fontFamily: '"MonoLisa", monospace', fontSize: '0.7rem', color: '#9ca3af' }}>
                                  {item.score}/{item.max}
                                </Typography>
                              </Box>
                              {item.comment && (
                                <Typography
                                  sx={{
                                    fontFamily: '"MonoLisa", monospace',
                                    fontSize: '0.7rem',
                                    color: '#6b7280',
                                    ml: 1.5,
                                    fontStyle: 'italic',
                                  }}
                                >
                                  {item.comment}
                                </Typography>
                              )}
                            </Box>
                          ))}
                        </Box>
                      </Collapse>
                    </Box>
                  );
                })}
              </Box>
            </Box>
          )}

          {/* No data message */}
          {!qualityScore && (!criteriaChecklist || Object.keys(criteriaChecklist).length === 0) && (
            <Typography sx={{ fontFamily: '"MonoLisa", monospace', fontSize: '0.9rem', color: '#9ca3af' }}>
              No quality data available.
            </Typography>
          )}
        </Box>
      </TabPanel>
    </Box>
  );
}
