import { useEffect } from 'react';
import { Helmet } from 'react-helmet-async';
import Box from '@mui/material/Box';
import { Breadcrumb } from '../components/Breadcrumb';
import { Footer } from '../components/Footer';
import { PaletteStrip } from '../components/PaletteStrip';
import { useAnalytics } from '../hooks';
import { colors, typography, headingStyle, textStyle } from '../theme';

const SWATCHES = [
  { name: 'brand (bluish green)', hex: '#009E73', role: 'First series, primary CTAs, brand anchor' },
  { name: 'vermillion', hex: '#D55E00', role: 'Second series, error states, warm contrast' },
  { name: 'blue', hex: '#0072B2', role: 'Third series, informational links, cool anchor' },
  { name: 'reddish purple', hex: '#CC79A7', role: 'Fourth series, distinctive accent' },
  { name: 'orange', hex: '#E69F00', role: 'Fifth series, highlights, hover states' },
  { name: 'sky blue', hex: '#56B4E9', role: 'Sixth series, info states' },
  { name: 'yellow', hex: '#F0E442', role: 'Seventh series — poor on white, use sparingly' },
  { name: 'neutral (adaptive)', hex: '#1A1A1A / #E8E8E0', role: 'Text, gridlines, totals — adapts to theme' },
];

export function PalettePage() {
  const { trackPageview } = useAnalytics();

  useEffect(() => {
    trackPageview('/palette');
  }, [trackPageview]);

  return (
    <>
      <Helmet>
        <title>palette | anyplot.ai</title>
        <meta name="description" content="The Okabe-Ito colorblind-safe palette used across all anyplot.ai visualizations. 8 colors, validated for deuteranopia, protanopia, and tritanopia." />
      </Helmet>

      <Breadcrumb items={[{ label: 'anyplot.ai', shortLabel: 'ap', to: '/' }, { label: 'palette' }]} />

      <Box sx={{ maxWidth: 800, mx: 'auto' }}>
        <Box component="h1" sx={{ ...headingStyle, fontFamily: typography.serif, fontSize: '1.5rem' }}>
          The Okabe-Ito Palette
        </Box>

        <Box sx={textStyle}>
          Every plot on anyplot.ai uses the Okabe-Ito palette, a set of 8 colors peer-reviewed for colorblind safety.
          Published in 2008 by Masataka Okabe and Kei Ito, it was optimized for three types of color vision deficiency —
          deuteranopia, protanopia, and tritanopia — which together affect roughly 8% of men.
        </Box>

        <Box sx={{ ...textStyle, fontStyle: 'italic', borderLeft: `3px solid ${colors.primary}`, pl: 3, my: 4 }}>
          "We proposed a set of colors optimized for colorblind and colorweak individuals,
          with the expectation that their use will broaden the accessibility
          of figures in scientific papers."
          <Box component="span" sx={{ display: 'block', mt: 1, fontStyle: 'normal', fontFamily: typography.mono, fontSize: '11px', color: 'var(--ink-muted)', letterSpacing: '0.1em' }}>
            — Okabe & Ito, 2008
          </Box>
        </Box>

        <PaletteStrip />

        <Box component="h2" sx={{ ...headingStyle, mt: 6 }}>Color Reference</Box>

        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1.5, mb: 6 }}>
          {SWATCHES.map((swatch, i) => (
            <Box key={i} sx={{ display: 'flex', alignItems: 'center', gap: 2, py: 1 }}>
              <Box sx={{
                width: 40, height: 40, borderRadius: '8px',
                bgcolor: swatch.hex.includes('/') ? colors.gray[800] : swatch.hex,
                flexShrink: 0,
                border: '1px solid var(--rule)',
              }} />
              <Box>
                <Box sx={{ fontFamily: typography.mono, fontSize: '13px', color: 'var(--ink)', fontWeight: 600 }}>
                  {swatch.hex}
                </Box>
                <Box sx={{ fontFamily: typography.mono, fontSize: '11px', color: 'var(--ink-muted)' }}>
                  {swatch.name} — {swatch.role}
                </Box>
              </Box>
            </Box>
          ))}
        </Box>

        <Box component="h2" sx={{ ...headingStyle, mt: 4 }}>Usage Rules</Box>

        <Box sx={textStyle}>
          The first series in every plot is always the brand color (#009E73). The neutral (position 8) is reserved for
          aggregates and reference lines. Yellow (#F0E442) has poor contrast on white backgrounds — use it only for
          position 7 or later.
        </Box>

        <Box sx={textStyle}>
          For sequential data, use viridis or cividis. For diverging data, use BrBG from ColorBrewer.
          Don't use Okabe-Ito for continuous data — a categorical palette on continuous data produces misleading banding.
        </Box>
      </Box>

      <Footer />
    </>
  );
}
