import { useEffect, useState } from 'react';
import { Link as RouterLink } from 'react-router-dom';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Link from '@mui/material/Link';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';

import { API_URL } from '../constants';
import { buildSrcSet, getFallbackSrc } from '../utils/responsiveImage';
import { fontSize, semanticColors } from '../theme';

interface RelatedSpec {
  id: string;
  title: string;
  preview_url: string | null;
  library_id: string | null;
  similarity: number;
  shared_tags: string[];
}

const mono = '"MonoLisa", "MonoLisa Fallback", monospace';

const LIB_ABBREV: Record<string, string> = {
  matplotlib: 'mpl',
  seaborn: 'sns',
  plotly: 'ply',
  bokeh: 'bok',
  altair: 'alt',
  plotnine: 'p9',
  pygal: 'pyg',
  highcharts: 'hc',
  letsplot: 'lp',
};

// 6 columns max at md+, ~160px each → 400w is plenty
const SIZES = '(max-width: 599px) 50vw, (max-width: 899px) 33vw, 17vw';

interface RelatedSpecsProps {
  specId: string;
  /** "spec" = spec tags only (overview), "full" = spec + impl tags (detail) */
  mode?: 'spec' | 'full';
  /** Current library — in full mode, matches tags against this library's impl_tags */
  library?: string;
  /** Called when hovering a related spec card — passes shared tag values */
  onHoverTags?: (tags: string[]) => void;
}

export function RelatedSpecs({ specId, mode = 'spec', library, onHoverTags }: RelatedSpecsProps) {
  const [related, setRelated] = useState<RelatedSpec[]>([]);
  const [expanded, setExpanded] = useState(false);

  useEffect(() => {
    let cancelled = false;
    const params = new URLSearchParams({ limit: '24', mode });
    if (library && mode === 'full') params.set('library', library);
    fetch(`${API_URL}/insights/related/${specId}?${params}`)
      .then(r => { if (!r.ok) throw new Error(); return r.json(); })
      .then(data => { if (!cancelled) setRelated(data.related ?? []); })
      .catch(() => { if (!cancelled) setRelated([]); });
    return () => { cancelled = true; };
  }, [specId, mode, library]);

  useEffect(() => {
    setExpanded(false);
  }, [specId]);

  if (related.length === 0) return null;

  // Collapsed: CSS hides extra rows via gridAutoRows:0 + overflow:hidden

  return (
    <Box sx={{ mt: 3, maxWidth: { xs: '100%', md: 1200, lg: 1400, xl: 1600 }, mx: 'auto' }}>
      <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
        <Tabs
          value={expanded ? 0 : false}
          onChange={() => setExpanded((e) => !e)}
          variant="fullWidth"
          sx={{
            '& .MuiTab-root': {
              fontFamily: '"MonoLisa", monospace',
              textTransform: 'none',
              fontSize: '0.875rem',
              minHeight: 48,
              transition: 'background-color 0.15s ease, color 0.15s ease',
              borderRadius: '4px 4px 0 0',
              '&:hover': { backgroundColor: '#f3f4f6', color: '#3776AB' },
            },
            '& .Mui-selected': { color: '#3776AB' },
            '& .MuiTabs-indicator': { backgroundColor: '#3776AB' },
          }}
        >
          <Tab
            onClick={() => expanded && setExpanded(false)}
            icon={<AutoAwesomeIcon sx={{ fontSize: '1.1rem' }} />}
            iconPosition="start"
            label="Similar"
          />
        </Tabs>
      </Box>
      <Box sx={{
        display: 'grid',
        gridTemplateColumns: { xs: 'repeat(2, 1fr)', sm: 'repeat(3, 1fr)', md: 'repeat(6, 1fr)' },
        columnGap: 2,
        rowGap: expanded ? 2 : 0,
        pt: 2,
        ...(!expanded && { gridTemplateRows: 'auto', gridAutoRows: 0, overflow: 'hidden' }),
      }}>
        {related.map(spec => (
          <Link
            key={spec.id}
            component={RouterLink}
            to={mode === 'full' && spec.library_id ? `/${spec.id}/${spec.library_id}` : `/${spec.id}`}
            onMouseEnter={() => onHoverTags?.(spec.shared_tags)}
            onMouseLeave={() => onHoverTags?.([])}
            sx={{
              textDecoration: 'none',
              color: 'inherit',
              border: '1px solid #e5e7eb',
              borderRadius: 1,
              overflow: 'hidden',
              transition: 'transform 0.15s ease',
              '&:hover': { transform: 'scale(1.02)', borderColor: '#e5e7eb' },
            }}
          >
            {spec.preview_url ? (
              <Box component="picture" sx={{ display: 'block' }}>
                <source type="image/webp" srcSet={buildSrcSet(spec.preview_url, 'webp')} sizes={SIZES} />
                <source type="image/png" srcSet={buildSrcSet(spec.preview_url, 'png')} sizes={SIZES} />
                <Box component="img" src={getFallbackSrc(spec.preview_url)} alt={spec.title}
                  sizes={SIZES} loading="lazy"
                  sx={{ width: '100%', aspectRatio: '16/9', objectFit: 'cover', display: 'block' }}
                />
              </Box>
            ) : (
              <Box sx={{ width: '100%', aspectRatio: '16/9', bgcolor: '#f9fafb', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <Typography sx={{ fontFamily: mono, fontSize: '0.7rem', color: '#d1d5db' }}>no preview</Typography>
              </Box>
            )}
            <Box sx={{ p: 1.5 }}>
              <Typography title={spec.title} sx={{ fontFamily: mono, fontSize: fontSize.sm, color: '#374151', lineHeight: 1.3 }} noWrap>
                {spec.title}
              </Typography>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mt: 0.25, gap: 0.5 }}>
                <Typography title={`${spec.shared_tags.length} tags in common: ${spec.shared_tags.join(', ')}`} sx={{ fontFamily: mono, fontSize: fontSize.xs, color: semanticColors.mutedText, whiteSpace: 'nowrap' }}>
                  {spec.shared_tags.length} common
                </Typography>
                {mode === 'full' && spec.library_id && (
                  <Typography title={spec.library_id} sx={{ fontFamily: mono, fontSize: fontSize.xs, color: semanticColors.mutedText, whiteSpace: 'nowrap' }}>
                    {LIB_ABBREV[spec.library_id] || spec.library_id}
                  </Typography>
                )}
              </Box>
            </Box>
          </Link>
        ))}
      </Box>
    </Box>
  );
}
